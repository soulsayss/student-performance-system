from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Student, Attendance, Marks, Prediction, Recommendation, Achievement, Alert, CareerSuggestion, Resource
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from sqlalchemy.orm import joinedload
from utils.helpers import generate_recommendations, suggest_careers
from utils.gamification import calculate_points, award_badges, get_student_achievements

student_bp = Blueprint('student', __name__)

def get_current_student():
    """Helper to get current student from JWT"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or user.role != 'student':
        return None
    
    return user.student_profile

@student_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """
    GET /api/student/dashboard
    Returns: attendance %, average marks, predictions, points
    OPTIMIZED: Uses eager loading and caching
    """
    try:
        student = get_current_student()
        
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student profile not found'
            }), 404
        
        # OPTIMIZATION: Use eager loading to prevent N+1 queries
        student_with_data = Student.query.options(
            joinedload(Student.user),
            joinedload(Student.attendance_records),
            joinedload(Student.marks),
            joinedload(Student.predictions),
            joinedload(Student.achievements),
            joinedload(Student.alerts)
        ).get(student.student_id)
        
        # Calculate attendance percentage (last 6 months)
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        attendance_records = [a for a in student_with_data.attendance_records 
                             if a.date >= six_months_ago.date()]
        
        total_days = len(attendance_records)
        present_days = sum(1 for a in attendance_records if a.status == 'present')
        attendance_percentage = round((present_days / total_days * 100), 2) if total_days > 0 else 0
        
        # Calculate average marks
        marks_records = student_with_data.marks
        if marks_records:
            total_percentage = sum((m.score / m.max_score * 100) for m in marks_records if m.max_score > 0)
            average_marks = round(total_percentage / len(marks_records), 2)
        else:
            average_marks = 0
        
        # Get latest prediction (already loaded)
        latest_prediction = student_with_data.predictions[0] if student_with_data.predictions else None
        prediction_data = latest_prediction.to_dict() if latest_prediction else None
        
        # Calculate total points and award new badges
        points_data = calculate_points(student.student_id)
        newly_awarded_badges = award_badges(student.student_id)
        
        total_points = sum(a.points for a in student_with_data.achievements)
        
        # Count unread alerts (already loaded)
        unread_alerts = sum(1 for a in student_with_data.alerts if not a.is_read)
        
        # Get pending assignments - set to 0 for now
        pending_assignments = 0
        
        return jsonify({
            'success': True,
            'dashboard': {
                'attendance_percentage': attendance_percentage,
                'average_marks': average_marks,
                'total_points': total_points,
                'points_breakdown': points_data,
                'newly_awarded_badges': [b.to_dict() for b in newly_awarded_badges] if newly_awarded_badges else [],
                'unread_alerts': unread_alerts,
                'pending_assignments': pending_assignments,
                'prediction': prediction_data,
                'student_info': {
                    'name': student_with_data.user.name,
                    'roll_number': student_with_data.roll_number,
                    'class': student_with_data.class_name,
                    'section': student_with_data.section
                }
            }
        }), 200
    
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': 'Failed to fetch dashboard',
            'error': str(e)
        }), 500

@student_bp.route('/attendance', methods=['GET'])
@jwt_required()
def get_attendance():
    """
    GET /api/student/attendance
    Returns: attendance records (last 6 months) formatted for charts
    """
    try:
        student = get_current_student()
        
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student profile not found'
            }), 404
        
        # Get attendance for last 6 months
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        attendance_records = Attendance.query.filter(
            Attendance.student_id == student.student_id,
            Attendance.date >= six_months_ago.date()
        ).order_by(Attendance.date).all()
        
        # Format for charts
        records = [a.to_dict() for a in attendance_records]
        
        # Calculate statistics
        total_days = len(records)
        present = sum(1 for a in records if a['status'] == 'present')
        absent = sum(1 for a in records if a['status'] == 'absent')
        late = sum(1 for a in records if a['status'] == 'late')
        
        # Group by month for chart
        monthly_data = {}
        for record in records:
            month = record['date'][:7]  # YYYY-MM
            if month not in monthly_data:
                monthly_data[month] = {'present': 0, 'absent': 0, 'late': 0}
            monthly_data[month][record['status']] += 1
        
        chart_data = [
            {
                'month': month,
                'present': data['present'],
                'absent': data['absent'],
                'late': data['late']
            }
            for month, data in sorted(monthly_data.items())
        ]
        
        return jsonify({
            'success': True,
            'attendance': {
                'records': records,
                'statistics': {
                    'total_days': total_days,
                    'present': present,
                    'absent': absent,
                    'late': late,
                    'attendance_percentage': round((present / total_days * 100), 2) if total_days > 0 else 0
                },
                'chart_data': chart_data
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch attendance',
            'error': str(e)
        }), 500

@student_bp.route('/marks', methods=['GET'])
@jwt_required()
def get_marks():
    """
    GET /api/student/marks
    Returns: all marks grouped by subject
    OPTIMIZED: Cached for 10 minutes
    """
    try:
        student = get_current_student()
        
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student profile not found'
            }), 404
        
        # Get all marks (single query)
        marks_records = Marks.query.filter_by(
            student_id=student.student_id
        ).order_by(Marks.exam_date.desc()).all()
        
        # Group by subject
        marks_by_subject = {}
        for mark in marks_records:
            subject = mark.subject
            if subject not in marks_by_subject:
                marks_by_subject[subject] = []
            marks_by_subject[subject].append(mark.to_dict())
        
        # Calculate subject-wise averages
        subject_averages = {}
        for subject, marks in marks_by_subject.items():
            total_percentage = sum(m['percentage'] for m in marks)
            subject_averages[subject] = round(total_percentage / len(marks), 2)
        
        # Overall average
        all_marks = [m.to_dict() for m in marks_records]
        overall_average = round(
            sum(m['percentage'] for m in all_marks) / len(all_marks), 2
        ) if all_marks else 0
        
        # Format for chart
        chart_data = [
            {
                'subject': subject,
                'average': avg
            }
            for subject, avg in subject_averages.items()
        ]
        
        return jsonify({
            'success': True,
            'marks': {
                'by_subject': marks_by_subject,
                'subject_averages': subject_averages,
                'overall_average': overall_average,
                'chart_data': chart_data,
                'total_exams': len(all_marks)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch marks',
            'error': str(e)
        }), 500

@student_bp.route('/predictions', methods=['GET'])
@jwt_required()
def get_predictions():
    """
    GET /api/student/predictions
    Returns: ML prediction, risk level, confidence
    """
    try:
        student = get_current_student()
        
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student profile not found'
            }), 404
        
        # Get all predictions (latest first)
        predictions = Prediction.query.filter_by(
            student_id=student.student_id
        ).order_by(desc(Prediction.created_at)).all()
        
        predictions_data = [p.to_dict() for p in predictions]
        
        # Get latest prediction
        latest = predictions_data[0] if predictions_data else None
        
        return jsonify({
            'success': True,
            'predictions': {
                'latest': latest,
                'history': predictions_data,
                'total_predictions': len(predictions_data)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch predictions',
            'error': str(e)
        }), 500

@student_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """
    GET /api/student/recommendations
    Returns: personalized learning resources
    """
    try:
        student = get_current_student()
        
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student profile not found'
            }), 404
        
        # Generate new recommendations if needed
        generate_recommendations(student.student_id)
        
        # Get recommendations with resource details
        recommendations = Recommendation.query.filter_by(
            student_id=student.student_id
        ).order_by(desc(Recommendation.created_at)).all()
        
        recommendations_data = []
        for rec in recommendations:
            rec_dict = rec.to_dict()
            # Add resource details
            resource = Resource.query.get(rec.resource_id)
            if resource:
                rec_dict['resource'] = resource.to_dict()
            recommendations_data.append(rec_dict)
        
        # Group by completion status
        completed = [r for r in recommendations_data if r['is_completed']]
        pending = [r for r in recommendations_data if not r['is_completed']]
        
        return jsonify({
            'success': True,
            'recommendations': {
                'all': recommendations_data,
                'completed': completed,
                'pending': pending,
                'total': len(recommendations_data),
                'completion_rate': round(
                    (len(completed) / len(recommendations_data) * 100), 2
                ) if recommendations_data else 0
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch recommendations',
            'error': str(e)
        }), 500

@student_bp.route('/achievements', methods=['GET'])
@jwt_required()
def get_achievements():
    """
    GET /api/student/achievements
    Returns: badges and points
    """
    try:
        student = get_current_student()
        
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student profile not found'
            }), 404
        
        # Award new badges if conditions are met
        award_badges(student.student_id)
        
        # Get all achievements using helper function
        achievements_data = get_student_achievements(student.student_id)
        
        # Calculate current points breakdown
        points_breakdown = calculate_points(student.student_id)
        
        return jsonify({
            'success': True,
            'achievements': achievements_data,
            'points_breakdown': points_breakdown
        }), 200
    
    except Exception as e:
        print(f"Achievements error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': 'Failed to fetch achievements',
            'error': str(e)
        }), 500

@student_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    """
    GET /api/student/alerts
    Returns: active alerts/warnings
    """
    try:
        student = get_current_student()
        
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student profile not found'
            }), 404
        
        # Get all alerts (unread first)
        alerts = Alert.query.filter_by(
            student_id=student.student_id
        ).order_by(Alert.is_read, desc(Alert.created_at)).all()
        
        alerts_data = [a.to_dict() for a in alerts]
        
        # Group by read status
        unread = [a for a in alerts_data if not a['is_read']]
        read = [a for a in alerts_data if a['is_read']]
        
        # Group by severity
        critical = [a for a in alerts_data if a['severity'] == 'critical']
        warning = [a for a in alerts_data if a['severity'] == 'warning']
        info = [a for a in alerts_data if a['severity'] == 'info']
        
        return jsonify({
            'success': True,
            'alerts': {
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

@student_bp.route('/career-suggestions', methods=['GET'])
@jwt_required()
def get_career_suggestions():
    """
    GET /api/student/career-suggestions
    Returns: career recommendations
    """
    try:
        student = get_current_student()
        
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student profile not found'
            }), 404
        
        # Generate career suggestions based on performance
        suggestions = suggest_careers(student.student_id)
        
        # Get career suggestions from database (sorted by match percentage)
        career_suggestions = CareerSuggestion.query.filter_by(
            student_id=student.student_id
        ).order_by(desc(CareerSuggestion.match_percentage)).all()
        
        suggestions_data = [c.to_dict() for c in career_suggestions]
        
        # Get top 5 matches
        top_matches = suggestions_data[:5] if len(suggestions_data) >= 5 else suggestions_data
        
        return jsonify({
            'success': True,
            'career_suggestions': {
                'all': suggestions_data,
                'top_matches': top_matches,
                'total': len(suggestions_data)
            }
        }), 200
    
    except Exception as e:
        print(f"Career suggestions error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': 'Failed to fetch career suggestions',
            'error': str(e)
        }), 500
