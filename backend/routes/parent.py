from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Student, Attendance, Marks, Prediction, Alert
from datetime import datetime, timedelta
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from app import cache

parent_bp = Blueprint('parent', __name__)

def get_current_parent():
    """Helper to get current parent from JWT"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or user.role != 'parent':
        return None
    
    return user

@parent_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, key_prefix=lambda: f'parent_dashboard_{get_jwt_identity()}')  # Cache for 5 minutes
def get_dashboard():
    """
    GET /api/parent/dashboard
    Returns: overview of all children
    OPTIMIZED: Uses eager loading to prevent N+1 queries
    """
    try:
        parent = get_current_parent()
        
        if not parent:
            return jsonify({
                'success': False,
                'message': 'Parent profile not found'
            }), 404
        
        # OPTIMIZATION: Use eager loading to load all related data
        children = Student.query.options(
            joinedload(Student.user),
            joinedload(Student.attendance_records),
            joinedload(Student.marks_records),
            joinedload(Student.predictions),
            joinedload(Student.alerts)
        ).filter_by(parent_id=parent.user_id).all()
        
        children_data = []
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        
        for child in children:
            # Calculate attendance (data already loaded)
            attendance_records = [a for a in child.attendance_records 
                                 if a.date >= six_months_ago.date()]
            
            if attendance_records:
                present = sum(1 for a in attendance_records if a.status == 'present')
                attendance_pct = round((present / len(attendance_records)) * 100, 2)
            else:
                attendance_pct = 0
            
            # Calculate average marks (data already loaded)
            marks = child.marks_records
            if marks:
                avg_marks = round(sum((m.score / m.max_score * 100) for m in marks if m.max_score > 0) / len(marks), 2)
            else:
                avg_marks = 0
            
            # Get latest prediction (data already loaded)
            prediction = child.predictions[0] if child.predictions else None
            
            # Count unread alerts (data already loaded)
            unread_alerts = sum(1 for a in child.alerts if not a.is_read)
            
            children_data.append({
                'student_id': child.student_id,
                'name': child.user.name,
                'roll_number': child.roll_number,
                'class': child.class_name,
                'section': child.section,
                'attendance_percentage': attendance_pct,
                'average_marks': avg_marks,
                'predicted_grade': prediction.predicted_grade if prediction else 'N/A',
                'risk_level': prediction.risk_level if prediction else 'unknown',
                'unread_alerts': unread_alerts
            })
        
        return jsonify({
            'success': True,
            'dashboard': {
                'parent_info': {
                    'name': parent.name,
                    'email': parent.email
                },
                'children': children_data,
                'total_children': len(children_data)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch dashboard',
            'error': str(e)
        }), 500

@parent_bp.route('/child/<int:child_id>/performance', methods=['GET'])
@jwt_required()
def get_child_performance(child_id):
    """
    GET /api/parent/child/:id/performance
    Returns: detailed performance data for specific child
    """
    try:
        parent = get_current_parent()
        
        if not parent:
            return jsonify({
                'success': False,
                'message': 'Parent profile not found'
            }), 404
        
        # Get child and verify parent relationship
        child = Student.query.get(child_id)
        
        if not child:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
        
        if child.parent_id != parent.user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied. This is not your child.'
            }), 403
        
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        
        # Get attendance records
        attendance_records = Attendance.query.filter(
            Attendance.student_id == child_id,
            Attendance.date >= six_months_ago.date()
        ).order_by(Attendance.date.desc()).all()
        
        attendance_data = [a.to_dict() for a in attendance_records]
        
        # Calculate attendance stats
        total_days = len(attendance_data)
        present = sum(1 for a in attendance_data if a['status'] == 'present')
        absent = sum(1 for a in attendance_data if a['status'] == 'absent')
        late = sum(1 for a in attendance_data if a['status'] == 'late')
        attendance_pct = round((present / total_days * 100), 2) if total_days > 0 else 0
        
        # Get marks records
        marks_records = Marks.query.filter_by(
            student_id=child_id
        ).order_by(Marks.exam_date.desc()).all()
        
        marks_data = [m.to_dict() for m in marks_records]
        
        # Group marks by subject
        marks_by_subject = {}
        for mark in marks_data:
            subject = mark['subject']
            if subject not in marks_by_subject:
                marks_by_subject[subject] = []
            marks_by_subject[subject].append(mark)
        
        # Calculate subject averages
        subject_averages = {}
        for subject, marks in marks_by_subject.items():
            avg = sum(m['percentage'] for m in marks) / len(marks)
            subject_averages[subject] = round(avg, 2)
        
        overall_average = round(
            sum(m['percentage'] for m in marks_data) / len(marks_data), 2
        ) if marks_data else 0
        
        # Get predictions
        predictions = Prediction.query.filter_by(
            student_id=child_id
        ).order_by(desc(Prediction.created_at)).all()
        
        predictions_data = [p.to_dict() for p in predictions]
        
        return jsonify({
            'success': True,
            'performance': {
                'student_info': {
                    'name': child.user.name,
                    'roll_number': child.roll_number,
                    'class': child.class_name,
                    'section': child.section
                },
                'attendance': {
                    'records': attendance_data[:30],  # Last 30 days
                    'statistics': {
                        'total_days': total_days,
                        'present': present,
                        'absent': absent,
                        'late': late,
                        'attendance_percentage': attendance_pct
                    }
                },
                'marks': {
                    'recent_marks': marks_data[:10],  # Last 10 exams
                    'by_subject': marks_by_subject,
                    'subject_averages': subject_averages,
                    'overall_average': overall_average
                },
                'predictions': {
                    'latest': predictions_data[0] if predictions_data else None,
                    'history': predictions_data
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch performance data',
            'error': str(e)
        }), 500

@parent_bp.route('/child/<int:child_id>/alerts', methods=['GET'])
@jwt_required()
def get_child_alerts(child_id):
    """
    GET /api/parent/child/:id/alerts
    Returns: all alerts for specific child
    """
    try:
        parent = get_current_parent()
        
        if not parent:
            return jsonify({
                'success': False,
                'message': 'Parent profile not found'
            }), 404
        
        # Get child and verify parent relationship
        child = Student.query.get(child_id)
        
        if not child:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
        
        if child.parent_id != parent.user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied. This is not your child.'
            }), 403
        
        # Get all alerts
        alerts = Alert.query.filter_by(
            student_id=child_id
        ).order_by(Alert.is_read, desc(Alert.created_at)).all()
        
        alerts_data = [a.to_dict() for a in alerts]
        
        # Group by status and severity
        unread = [a for a in alerts_data if not a['is_read']]
        read = [a for a in alerts_data if a['is_read']]
        
        critical = [a for a in alerts_data if a['severity'] == 'critical']
        warning = [a for a in alerts_data if a['severity'] == 'warning']
        info = [a for a in alerts_data if a['severity'] == 'info']
        
        return jsonify({
            'success': True,
            'alerts': {
                'student_info': {
                    'name': child.user.name,
                    'roll_number': child.roll_number
                },
                'all': alerts_data,
                'unread': unread,
                'read': read,
                'by_severity': {
                    'critical': critical,
                    'warning': warning,
                    'info': info
                },
                'counts': {
                    'total': len(alerts_data),
                    'unread': len(unread),
                    'critical': len(critical)
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch alerts',
            'error': str(e)
        }), 500


@parent_bp.route('/child/<int:child_id>/recommendations', methods=['GET'])
@jwt_required()
def get_child_recommendations(child_id):
    """
    GET /api/parent/child/:id/recommendations
    Returns: recommendations for specific child
    """
    try:
        from models import Recommendation
        
        parent = get_current_parent()
        
        if not parent:
            return jsonify({
                'success': False,
                'message': 'Parent profile not found'
            }), 404
        
        # Get child and verify parent relationship
        child = Student.query.get(child_id)
        
        if not child:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
        
        if child.parent_id != parent.user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied. This is not your child.'
            }), 403
        
        # Get recommendations
        recommendations = Recommendation.query.filter_by(
            student_id=child_id
        ).order_by(desc(Recommendation.created_at)).all()
        
        recommendations_data = [r.to_dict() for r in recommendations]
        
        return jsonify({
            'success': True,
            'recommendations': {
                'student_info': {
                    'name': child.user.name,
                    'roll_number': child.roll_number
                },
                'all': recommendations_data,
                'count': len(recommendations_data)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch recommendations',
            'error': str(e)
        }), 500
