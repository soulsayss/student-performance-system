"""
Optimization Helper Functions
Centralized functions to avoid code duplication and handle edge cases
"""

from models import db, Student, Marks, Attendance, Achievement
from sqlalchemy import func
from datetime import datetime, timedelta


def calculate_attendance_percentage(student_id, days=None):
    """
    Calculate attendance percentage for a student
    Handles edge case of zero attendance records
    
    Args:
        student_id: Student ID
        days: Number of days to look back (None for all time)
    
    Returns:
        float: Attendance percentage (0-100)
    """
    query = Attendance.query.filter_by(student_id=student_id)
    
    if days:
        start_date = datetime.utcnow().date() - timedelta(days=days)
        query = query.filter(Attendance.date >= start_date)
    
    records = query.all()
    
    if not records:
        return 0.0
    
    present_count = sum(1 for r in records if r.status == 'present')
    total_count = len(records)
    
    return round((present_count / total_count) * 100, 2) if total_count > 0 else 0.0


def calculate_average_marks(student_id, subject=None):
    """
    Calculate average marks for a student
    Handles edge case of no marks
    
    Args:
        student_id: Student ID
        subject: Optional subject filter
    
    Returns:
        float: Average percentage (0-100)
    """
    query = Marks.query.filter_by(student_id=student_id)
    
    if subject:
        query = query.filter_by(subject=subject)
    
    marks = query.all()
    
    if not marks:
        return 0.0
    
    percentages = [(m.score / m.max_score * 100) for m in marks if m.max_score > 0]
    
    return round(sum(percentages) / len(percentages), 2) if percentages else 0.0


def calculate_subject_averages(student_id):
    """
    Calculate average marks per subject
    
    Args:
        student_id: Student ID
    
    Returns:
        dict: {subject: average_percentage}
    """
    marks = Marks.query.filter_by(student_id=student_id).all()
    
    if not marks:
        return {}
    
    subject_marks = {}
    for mark in marks:
        if mark.subject not in subject_marks:
            subject_marks[mark.subject] = []
        
        if mark.max_score > 0:
            percentage = (mark.score / mark.max_score) * 100
            subject_marks[mark.subject].append(percentage)
    
    return {
        subject: round(sum(scores) / len(scores), 2) if scores else 0.0
        for subject, scores in subject_marks.items()
    }


def check_sufficient_data_for_prediction(student_id, min_marks=5, min_attendance=10):
    """
    Check if student has sufficient data for ML prediction
    
    Args:
        student_id: Student ID
        min_marks: Minimum marks records required
        min_attendance: Minimum attendance records required
    
    Returns:
        tuple: (bool: has_sufficient_data, str: message)
    """
    marks_count = Marks.query.filter_by(student_id=student_id).count()
    attendance_count = Attendance.query.filter_by(student_id=student_id).count()
    
    if marks_count < min_marks:
        return False, f"Insufficient marks data. Need at least {min_marks} records, have {marks_count}"
    
    if attendance_count < min_attendance:
        return False, f"Insufficient attendance data. Need at least {min_attendance} records, have {attendance_count}"
    
    return True, "Sufficient data available"


def award_badge_if_not_exists(student_id, badge_name, badge_type, description, points):
    """
    Award a badge to student if not already awarded
    Prevents duplicate badge awards
    
    Args:
        student_id: Student ID
        badge_name: Name of the badge
        badge_type: Type (bronze, silver, gold, platinum)
        description: Badge description
        points: Points to award
    
    Returns:
        tuple: (bool: was_awarded, Achievement: achievement or None)
    """
    # Check if badge already exists
    existing = Achievement.query.filter_by(
        student_id=student_id,
        badge_name=badge_name
    ).first()
    
    if existing:
        return False, existing
    
    # Award new badge
    achievement = Achievement(
        student_id=student_id,
        badge_name=badge_name,
        badge_type=badge_type,
        description=description,
        points_earned=points,
        earned_date=datetime.utcnow()
    )
    
    db.session.add(achievement)
    
    # Update student points
    student = Student.query.get(student_id)
    if student:
        current_points = getattr(student, 'total_points', 0) or 0
        student.total_points = max(0, current_points + points)
    
    return True, achievement


def get_career_suggestions_with_ties(subject_scores, top_n=5):
    """
    Get career suggestions handling ties in match percentage
    
    Args:
        subject_scores: Dict of subject scores
        top_n: Number of top careers to return
    
    Returns:
        list: Career suggestions with match percentages
    """
    # Career mapping (simplified - should be in database)
    career_mappings = {
        'Software Engineer': {'Mathematics': 0.3, 'Physics': 0.2, 'Computer Science': 0.5},
        'Doctor': {'Biology': 0.4, 'Chemistry': 0.3, 'Physics': 0.3},
        'Accountant': {'Mathematics': 0.5, 'Economics': 0.3, 'Business': 0.2},
        'Teacher': {'English': 0.3, 'Mathematics': 0.2, 'Science': 0.2, 'History': 0.3},
        'Engineer': {'Mathematics': 0.4, 'Physics': 0.4, 'Chemistry': 0.2},
    }
    
    career_matches = []
    
    for career, weights in career_mappings.items():
        match_score = 0
        total_weight = 0
        
        for subject, weight in weights.items():
            if subject in subject_scores:
                match_score += subject_scores[subject] * weight
                total_weight += weight
        
        if total_weight > 0:
            match_percentage = round((match_score / total_weight), 2)
            career_matches.append({
                'career': career,
                'match_percentage': match_percentage
            })
    
    # Sort by match percentage (descending)
    career_matches.sort(key=lambda x: x['match_percentage'], reverse=True)
    
    # Return top N, including ties
    if not career_matches:
        return []
    
    result = []
    last_percentage = None
    
    for match in career_matches:
        if len(result) < top_n:
            result.append(match)
            last_percentage = match['match_percentage']
        elif match['match_percentage'] == last_percentage:
            # Include tied careers
            result.append(match)
        else:
            break
    
    return result


def safe_divide(numerator, denominator, default=0.0):
    """
    Safely divide two numbers, returning default if denominator is zero
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division by zero
    
    Returns:
        float: Result of division or default
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def validate_user_role(user, required_role):
    """
    Validate that user has the required role
    Centralized role checking
    
    Args:
        user: User object
        required_role: Required role string or list of roles
    
    Returns:
        bool: True if user has required role
    """
    if not user:
        return False
    
    if isinstance(required_role, list):
        return user.role in required_role
    
    return user.role == required_role


def get_date_range(days_back):
    """
    Get date range for queries
    
    Args:
        days_back: Number of days to look back
    
    Returns:
        tuple: (start_date, end_date)
    """
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days_back)
    return start_date, end_date


def format_error_response(message, status_code=400, **kwargs):
    """
    Format consistent error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        **kwargs: Additional fields
    
    Returns:
        tuple: (dict, status_code)
    """
    response = {
        'success': False,
        'message': message,
        **kwargs
    }
    return response, status_code


def format_success_response(message=None, data=None, status_code=200, **kwargs):
    """
    Format consistent success response
    
    Args:
        message: Success message
        data: Response data
        status_code: HTTP status code
        **kwargs: Additional fields
    
    Returns:
        tuple: (dict, status_code)
    """
    response = {
        'success': True,
        **kwargs
    }
    
    if message:
        response['message'] = message
    
    if data is not None:
        response.update(data)
    
    return response, status_code
