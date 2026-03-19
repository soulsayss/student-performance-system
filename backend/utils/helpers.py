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
    SIMPLIFIED: Detect students at risk based on predictions only
    Returns: List of at-risk student IDs with reasons
    """
    try:
        at_risk_students = []
        
        # Get students with high risk predictions (simplest approach)
        high_risk_predictions = Prediction.query.filter_by(risk_level='high').all()
        
        for prediction in high_risk_predictions:
            try:
                student = Student.query.get(prediction.student_id)
                if student and student.user:
                    at_risk_students.append({
                        'student_id': student.student_id,
                        'name': student.user.name,
                        'roll_number': student.roll_number,
                        'class_name': student.class_name,
                        'section': student.section,
                        'risk_factors': [f'High risk prediction: {prediction.predicted_grade}'],
                        'reason': f'High risk prediction: {prediction.predicted_grade}'
                    })
            except Exception as e:
                print(f"Error processing student {prediction.student_id}: {e}")
                continue
        
        return at_risk_students
    except Exception as e:
        print(f"Error in detect_at_risk_students: {e}")
        return []


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
