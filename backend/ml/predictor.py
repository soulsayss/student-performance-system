"""
ML Predictor for student performance
"""
import joblib
import numpy as np
import os
from datetime import datetime, timedelta

# Load models (lazy loading)
_models_loaded = False
_risk_model = None
_grade_model = None
_scaler = None
_risk_encoder = None
_grade_encoder = None
_feature_columns = None

def load_models():
    """Load trained models and preprocessors"""
    global _models_loaded, _risk_model, _grade_model, _scaler, _risk_encoder, _grade_encoder, _feature_columns
    
    if _models_loaded:
        return
    
    models_dir = 'ml/models'
    
    try:
        _risk_model = joblib.load(f'{models_dir}/risk_model.pkl')
        _grade_model = joblib.load(f'{models_dir}/grade_model.pkl')
        _scaler = joblib.load(f'{models_dir}/scaler.pkl')
        _risk_encoder = joblib.load(f'{models_dir}/risk_encoder.pkl')
        _grade_encoder = joblib.load(f'{models_dir}/grade_encoder.pkl')
        _feature_columns = joblib.load(f'{models_dir}/feature_columns.pkl')
        _models_loaded = True
        print("✅ ML models loaded successfully")
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        raise

def calculate_student_features(student_id):
    """
    Calculate features for a student from database
    """
    from models import Student, Attendance, Marks, Assignment
    from datetime import datetime, timedelta
    
    # Get student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with ID {student_id} not found")
    
    # Calculate attendance percentage (last 6 months)
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    attendance_records = Attendance.query.filter(
        Attendance.student_id == student_id,
        Attendance.date >= six_months_ago.date()
    ).all()
    
    if attendance_records:
        present = sum(1 for a in attendance_records if a.status == 'present')
        attendance_pct = (present / len(attendance_records)) * 100
    else:
        attendance_pct = 0
    
    # Calculate average marks
    marks_records = Marks.query.filter_by(student_id=student_id).all()
    if marks_records:
        avg_marks = sum((m.score / m.max_score * 100) for m in marks_records if m.max_score > 0) / len(marks_records)
    else:
        avg_marks = 0
    
    # Calculate quiz average
    quiz_marks = [m for m in marks_records if m.exam_type == 'quiz']
    if quiz_marks:
        quiz_avg = sum((m.score / m.max_score * 100) for m in quiz_marks if m.max_score > 0) / len(quiz_marks)
    else:
        quiz_avg = avg_marks  # Use overall average if no quizzes
    
    # Calculate assignment completion rate
    assignments = Assignment.query.filter_by(student_id=student_id).all()
    if assignments:
        completed = sum(1 for a in assignments if a.status in ['submitted', 'graded'])
        assignment_completion = (completed / len(assignments)) * 100
    else:
        assignment_completion = 100  # Assume 100% if no assignments
    
    # Calculate late submissions
    late_submissions = sum(1 for a in assignments if a.submission_date and a.submission_date > datetime.combine(a.due_date, datetime.min.time()))
    
    # Estimate participation score (based on attendance and assignment completion)
    participation_score = (attendance_pct / 10 + assignment_completion / 10) / 2
    
    # Estimate study hours (based on performance)
    study_hours = (avg_marks / 100) * 20  # Scale to 0-20 hours
    
    features = {
        'attendance_percentage': round(attendance_pct, 2),
        'average_marks': round(avg_marks, 2),
        'assignment_completion_rate': round(assignment_completion, 2),
        'quiz_average': round(quiz_avg, 2),
        'participation_score': round(participation_score, 2),
        'study_hours_per_week': round(study_hours, 2),
        'late_submissions': late_submissions
    }
    
    return features

def predict_performance(student_id):
    """
    Predict student performance
    
    Returns:
        dict: {
            'predicted_grade': str,
            'risk_level': str,
            'confidence_score': float,
            'features': dict,
            'recommendations': list
        }
    """
    # Load models if not loaded
    load_models()
    
    # Calculate features
    features = calculate_student_features(student_id)
    
    # Prepare feature vector
    feature_vector = np.array([[
        features['attendance_percentage'],
        features['average_marks'],
        features['assignment_completion_rate'],
        features['quiz_average'],
        features['participation_score'],
        features['study_hours_per_week'],
        features['late_submissions']
    ]])
    
    # Scale features
    feature_vector_scaled = _scaler.transform(feature_vector)
    
    # Predict risk level
    risk_pred = _risk_model.predict(feature_vector_scaled)[0]
    risk_proba = _risk_model.predict_proba(feature_vector_scaled)[0]
    risk_level = _risk_encoder.inverse_transform([risk_pred])[0]
    risk_confidence = float(max(risk_proba))
    
    # Predict grade
    grade_pred = _grade_model.predict(feature_vector_scaled)[0]
    grade_proba = _grade_model.predict_proba(feature_vector_scaled)[0]
    predicted_grade = _grade_encoder.inverse_transform([grade_pred])[0]
    grade_confidence = float(max(grade_proba))
    
    # Overall confidence (average of both)
    confidence_score = (risk_confidence + grade_confidence) / 2
    
    # Generate recommendations
    recommendations = generate_recommendations(features, risk_level)
    
    # Identify contributing factors
    factors = identify_factors(features)
    
    result = {
        'predicted_grade': predicted_grade,
        'risk_level': risk_level,
        'confidence_score': round(confidence_score, 4),
        'features': features,
        'factors': factors,
        'recommendations': recommendations
    }
    
    return result

def generate_recommendations(features, risk_level):
    """Generate personalized recommendations based on features"""
    recommendations = []
    
    if features['attendance_percentage'] < 75:
        recommendations.append("Improve attendance - currently below 75%")
    
    if features['average_marks'] < 60:
        recommendations.append("Focus on improving test scores through regular study")
    
    if features['assignment_completion_rate'] < 80:
        recommendations.append("Complete assignments on time to improve grades")
    
    if features['late_submissions'] > 3:
        recommendations.append("Work on time management to reduce late submissions")
    
    if features['participation_score'] < 6:
        recommendations.append("Increase class participation and engagement")
    
    if features['study_hours_per_week'] < 10:
        recommendations.append("Increase study hours to at least 10 hours per week")
    
    if risk_level == 'high':
        recommendations.append("Consider meeting with academic advisor for support")
        recommendations.append("Join study groups or tutoring sessions")
    
    if not recommendations:
        recommendations.append("Keep up the excellent work!")
        recommendations.append("Continue maintaining current performance levels")
    
    return recommendations

def identify_factors(features):
    """Identify key contributing factors"""
    factors = {}
    
    # Attendance factor
    if features['attendance_percentage'] >= 90:
        factors['attendance'] = 'excellent'
    elif features['attendance_percentage'] >= 75:
        factors['attendance'] = 'good'
    elif features['attendance_percentage'] >= 60:
        factors['attendance'] = 'needs_improvement'
    else:
        factors['attendance'] = 'poor'
    
    # Marks trend
    if features['average_marks'] >= 85:
        factors['marks_trend'] = 'excellent'
    elif features['average_marks'] >= 70:
        factors['marks_trend'] = 'good'
    elif features['average_marks'] >= 50:
        factors['marks_trend'] = 'average'
    else:
        factors['marks_trend'] = 'poor'
    
    # Assignment completion
    if features['assignment_completion_rate'] >= 90:
        factors['assignment_completion'] = 'excellent'
    elif features['assignment_completion_rate'] >= 75:
        factors['assignment_completion'] = 'good'
    else:
        factors['assignment_completion'] = 'needs_improvement'
    
    return factors
