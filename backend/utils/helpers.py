"""
Helper functions for advanced features:
- Early Warning System
- Recommendation Engine
- Career Guidance
"""

from datetime import datetime, timedelta
from sqlalchemy import desc, func
from models import db, Student, Attendance, Marks, Prediction, Alert, Resource, Recommendation, CareerSuggestion


def detect_at_risk_students():
    """
    OPTIMIZED: Detect students at risk based on:
    - Attendance < 75%
    - Predicted risk = high
    - Declining performance
    
    Returns: List of at-risk student IDs with reasons
    Uses database aggregation to prevent memory overflow
    """
    at_risk_students = []
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)  # Reduced from 180 to 30 days
    
    # OPTIMIZATION: Use database aggregation for attendance
    # Get students with low attendance using subquery
    low_attendance_subquery = db.session.query(
        Attendance.student_id,
        func.count(Attendance.attendance_id).label('total'),
        func.sum(func.case((Attendance.status == 'present', 1), else_=0)).label('present')
    ).filter(
        Attendance.date >= thirty_days_ago.date()
    ).group_by(Attendance.student_id).subquery()
    
    low_attendance_students = db.session.query(
        low_attendance_subquery.c.student_id,
        low_attendance_subquery.c.present,
        low_attendance_subquery.c.total
    ).filter(
        (low_attendance_subquery.c.present * 100.0 / low_attendance_subquery.c.total) < 75
    ).all()
    
    # Create dict for quick lookup
    low_attendance_dict = {
        s.student_id: (s.present * 100.0 / s.total) 
        for s in low_attendance_students
    }
    
    # Get students with high risk predictions
    high_risk_predictions = db.session.query(
        Prediction.student_id,
        Prediction.predicted_grade
    ).filter(
        Prediction.risk_level == 'high'
    ).distinct(Prediction.student_id).all()
    
    high_risk_dict = {p.student_id: p.predicted_grade for p in high_risk_predictions}
    
    # Get all at-risk student IDs
    at_risk_ids = set(low_attendance_dict.keys()) | set(high_risk_dict.keys())
    
    # Load only at-risk students with their user data
    if at_risk_ids:
        from sqlalchemy.orm import joinedload
        at_risk_student_objs = Student.query.options(
            joinedload(Student.user)
        ).filter(Student.student_id.in_(at_risk_ids)).all()
        
        for student in at_risk_student_objs:
            risk_factors = []
            
            # Check attendance
            if student.student_id in low_attendance_dict:
                attendance_pct = low_attendance_dict[student.student_id]
                risk_factors.append(f'Low attendance: {attendance_pct:.1f}%')
            
            # Check prediction risk level
            if student.student_id in high_risk_dict:
                predicted_grade = high_risk_dict[student.student_id]
                risk_factors.append(f'High risk prediction: {predicted_grade}')
            
            at_risk_students.append({
                'student_id': student.student_id,
                'name': student.user.name,
                'roll_number': student.roll_number,
                'class_name': student.class_name,
                'section': student.section,
                'risk_factors': risk_factors,
                'reason': ', '.join(risk_factors)
            })
    
    return at_risk_students


def generate_alert_for_student(student_id, message, severity='warning'):
    """
    Generate an alert for a student
    
    Args:
        student_id: Student ID
        message: Alert message
        severity: 'info', 'warning', or 'critical'
    """
    try:
        alert = Alert(
            student_id=student_id,
            message=message,
            severity=severity,
            is_read=False
        )
        db.session.add(alert)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error creating alert: {e}")
        return False


def generate_recommendations(student_id):
    """
    Generate personalized recommendations based on:
    - Weak subjects
    - Difficulty level
    - Learning style
    
    Returns: List of recommended resources
    """
    recommendations = []
    
    # Get student's marks by subject
    marks_by_subject = db.session.query(
        Marks.subject,
        func.avg((Marks.score / Marks.max_score) * 100).label('avg_percentage')
    ).filter(
        Marks.student_id == student_id
    ).group_by(Marks.subject).all()
    
    # Identify weak subjects (< 60%)
    weak_subjects = [subj for subj, avg in marks_by_subject if avg < 60]
    
    # Get resources for weak subjects
    for subject in weak_subjects:
        # Start with beginner resources
        resources = Resource.query.filter_by(
            subject=subject,
            difficulty='beginner'
        ).limit(2).all()
        
        for resource in resources:
            # Check if recommendation already exists
            existing = Recommendation.query.filter_by(
                student_id=student_id,
                resource_id=resource.resource_id
            ).first()
            
            if not existing:
                rec = Recommendation(
                    student_id=student_id,
                    resource_id=resource.resource_id,
                    reason=f'Recommended to improve {subject} performance'
                )
                db.session.add(rec)
                recommendations.append({
                    'resource': resource.to_dict(),
                    'reason': rec.reason
                })
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error saving recommendations: {e}")
    
    return recommendations


def suggest_careers(student_id):
    """
    Suggest career paths based on:
    - Strong subjects
    - Performance trends
    - Interest areas
    
    Returns: List of career suggestions with match %
    """
    # Career mapping based on strong subjects
    career_map = {
        'Mathematics': ['Data Scientist', 'Engineer', 'Actuary', 'Economist'],
        'Physics': ['Engineer', 'Physicist', 'Researcher', 'Astronomer'],
        'Chemistry': ['Chemist', 'Pharmacist', 'Chemical Engineer', 'Researcher'],
        'Biology': ['Doctor', 'Biologist', 'Pharmacist', 'Researcher'],
        'Computer Science': ['Software Engineer', 'Data Scientist', 'AI Specialist', 'Cybersecurity Expert'],
        'English': ['Writer', 'Journalist', 'Teacher', 'Content Creator'],
        'History': ['Historian', 'Archaeologist', 'Teacher', 'Museum Curator'],
        'Economics': ['Economist', 'Financial Analyst', 'Business Consultant', 'Banker']
    }
    
    # Get student's marks by subject
    marks_by_subject = db.session.query(
        Marks.subject,
        func.avg((Marks.score / Marks.max_score) * 100).label('avg_percentage')
    ).filter(
        Marks.student_id == student_id
    ).group_by(Marks.subject).order_by(desc('avg_percentage')).all()
    
    # Identify strong subjects (> 75%)
    strong_subjects = [(subj, avg) for subj, avg in marks_by_subject if avg > 75]
    
    career_suggestions = {}
    
    for subject, avg_score in strong_subjects[:3]:  # Top 3 subjects
        if subject in career_map:
            for career in career_map[subject]:
                if career not in career_suggestions:
                    career_suggestions[career] = {
                        'match_percentage': 0,
                        'subjects': []
                    }
                
                # Calculate match percentage based on score
                match_contribution = (avg_score / 100) * 33.33  # Each subject contributes up to 33.33%
                career_suggestions[career]['match_percentage'] += match_contribution
                career_suggestions[career]['subjects'].append({
                    'name': subject,
                    'score': round(avg_score, 1)
                })
    
    # Convert to list and sort by match percentage
    suggestions = []
    for career, data in career_suggestions.items():
        # Check if suggestion already exists
        existing = CareerSuggestion.query.filter_by(
            student_id=student_id,
            career_path=career
        ).first()
        
        match_pct = round(data['match_percentage'], 1)
        
        if not existing:
            suggestion = CareerSuggestion(
                student_id=student_id,
                career_path=career,
                match_percentage=match_pct,
                description=f"Based on strong performance in {', '.join([s['name'] for s in data['subjects']])}"
            )
            db.session.add(suggestion)
        
        suggestions.append({
            'career': career,
            'match_percentage': match_pct,
            'strong_subjects': data['subjects']
        })
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error saving career suggestions: {e}")
    
    # Sort by match percentage
    suggestions.sort(key=lambda x: x['match_percentage'], reverse=True)
    
    return suggestions[:5]  # Top 5 suggestions
