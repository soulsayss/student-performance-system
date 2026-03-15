from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Prediction
from ml.predictor import predict_performance
from datetime import datetime
import os

ml_bp = Blueprint('ml', __name__)

def get_current_user():
    """Helper to get current user from JWT"""
    user_id = int(get_jwt_identity())
    return User.query.get(user_id)

@ml_bp.route('/predict', methods=['POST'])
@jwt_required()
def make_prediction():
    """
    POST /api/ml/predict
    Make performance prediction for a student
    """
    try:
        user = get_current_user()
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        student_id = data.get('student_id')
        
        if not student_id:
            return jsonify({
                'success': False,
                'message': 'student_id is required'
            }), 400
        
        # Check permissions
        if user.role == 'student':
            # Students can only predict for themselves
            if user.student_profile and user.student_profile.student_id != student_id:
                return jsonify({
                    'success': False,
                    'message': 'You can only predict your own performance'
                }), 403
        elif user.role == 'parent':
            # Parents can only predict for their children
            from models import Student
            student = Student.query.get(student_id)
            if not student or student.parent_id != user.user_id:
                return jsonify({
                    'success': False,
                    'message': 'You can only predict for your children'
                }), 403
        elif user.role not in ['teacher', 'admin']:
            return jsonify({
                'success': False,
                'message': 'Insufficient permissions'
            }), 403
        
        # Make prediction
        result = predict_performance(student_id)
        
        # Save prediction to database
        prediction = Prediction(
            student_id=student_id,
            predicted_grade=result['predicted_grade'],
            risk_level=result['risk_level'],
            confidence_score=result['confidence_score'],
            factors=result['factors']
        )
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'prediction': {
                'prediction_id': prediction.prediction_id,
                'student_id': student_id,
                'predicted_grade': result['predicted_grade'],
                'risk_level': result['risk_level'],
                'confidence_score': result['confidence_score'],
                'factors': result['factors'],
                'recommendations': result['recommendations'],
                'features': result['features'],
                'created_at': prediction.created_at.isoformat()
            }
        }), 200
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Prediction failed',
            'error': str(e)
        }), 500

@ml_bp.route('/train', methods=['POST'])
@jwt_required()
def train_model():
    """
    POST /api/ml/train
    Retrain ML model with latest data (admin only)
    """
    try:
        user = get_current_user()
        
        if not user or user.role != 'admin':
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        # Import training modules
        from ml.dataset_generator import generate_student_dataset
        from ml.model_trainer import main as train_main
        
        # Generate fresh dataset
        print("Generating new dataset...")
        df = generate_student_dataset(150)
        df.to_csv('ml/student_performance_dataset.csv', index=False)
        
        # Train models
        print("Training models...")
        train_main()
        
        return jsonify({
            'success': True,
            'message': 'Models retrained successfully',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Training failed',
            'error': str(e)
        }), 500

@ml_bp.route('/model-info', methods=['GET'])
@jwt_required()
def get_model_info():
    """
    GET /api/ml/model-info
    Get information about loaded ML models
    """
    try:
        user = get_current_user()
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        models_dir = 'ml/models'
        
        # Check if models exist
        risk_model_exists = os.path.exists(f'{models_dir}/risk_model.pkl')
        grade_model_exists = os.path.exists(f'{models_dir}/grade_model.pkl')
        
        if not (risk_model_exists and grade_model_exists):
            return jsonify({
                'success': False,
                'message': 'Models not found. Please train models first.',
                'models_exist': False
            }), 404
        
        # Get model file info
        risk_model_time = os.path.getmtime(f'{models_dir}/risk_model.pkl')
        grade_model_time = os.path.getmtime(f'{models_dir}/grade_model.pkl')
        
        return jsonify({
            'success': True,
            'models_exist': True,
            'risk_model': {
                'path': f'{models_dir}/risk_model.pkl',
                'last_trained': datetime.fromtimestamp(risk_model_time).isoformat()
            },
            'grade_model': {
                'path': f'{models_dir}/grade_model.pkl',
                'last_trained': datetime.fromtimestamp(grade_model_time).isoformat()
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get model info',
            'error': str(e)
        }), 500
