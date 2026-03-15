"""
Gamification system for student engagement:
- Points calculation
- Badge awards
- Achievement tracking
"""

from datetime import datetime, timedelta
from sqlalchemy import desc
from models import db, Student, Attendance, Marks, Achievement


# Badge definitions
BADGES = {
    'perfect_attendance': {
        'name': 'Perfect Attendance',
        'description': '100% attendance for a month',
        'points': 50,
        'icon': '🎯'
    },
    'high_achiever': {
        'name': 'High Achiever',
        'description': 'Score above 90% in all subjects',
        'points': 100,
        'icon': '🏆'
    },
    'consistent_performer': {
        'name': 'Consistent Performer',
        'description': 'Maintain above 75% for 3 months',
        'points': 75,
        'icon': '⭐'
    },
    'improvement_star': {
        'name': 'Improvement Star',
        'description': 'Improve marks by 15% or more',
        'points': 60,
        'icon': '📈'
    },
    'subject_master': {
        'name': 'Subject Master',
        'description': 'Score 95%+ in any subject',
        'points': 40,
        'icon': '🎓'
    },
    'early_bird': {
        'name': 'Early Bird',
        'description': 'No late arrivals for a month',
        'points': 30,
        'icon': '🌅'
    }
}


def calculate_points(student_id):
    """
    Calculate total points for a student based on:
    - Attendance
    - Grades
    - Improvement
    - Consistency
    
    Returns: Total points and breakdown
    """
    points_breakdown = {
        'attendance': 0,
        'grades': 0,
        'improvement': 0,
        'consistency': 0,
        'total': 0
    }
    
    student = Student.query.get(student_id)
    if not student:
        return points_breakdown
    
    # Calculate attendance points (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    attendance_records = Attendance.query.filter(
        Attendance.student_id == student_id,
        Attendance.date >= thirty_days_ago.date()
    ).all()
    
    if attendance_records:
        present = sum(1 for a in attendance_records if a.status == 'present')
        attendance_pct = (present / len(attendance_records)) * 100
        
        # Award points based on attendance
        if attendance_pct >= 95:
            points_breakdown['attendance'] = 20
        elif attendance_pct >= 85:
            points_breakdown['attendance'] = 15
        elif attendance_pct >= 75:
            points_breakdown['attendance'] = 10
    
    # Calculate grade points (recent exams)
    recent_marks = Marks.query.filter_by(
        student_id=student_id
    ).order_by(desc(Marks.exam_date)).limit(5).all()
    
    if recent_marks:
        avg_percentage = sum((m.score / m.max_score * 100) for m in recent_marks) / len(recent_marks)
        
        # Award points based on grades
        if avg_percentage >= 90:
            points_breakdown['grades'] = 30
        elif avg_percentage >= 80:
            points_breakdown['grades'] = 20
        elif avg_percentage >= 70:
            points_breakdown['grades'] = 10
    
    # Calculate improvement points
    if len(recent_marks) >= 4:
        recent_avg = sum((m.score / m.max_score * 100) for m in recent_marks[:2]) / 2
        older_avg = sum((m.score / m.max_score * 100) for m in recent_marks[2:4]) / 2
        
        improvement = recent_avg - older_avg
        if improvement >= 10:
            points_breakdown['improvement'] = 25
        elif improvement >= 5:
            points_breakdown['improvement'] = 15
    
    # Calculate consistency points (standard deviation of marks)
    if len(recent_marks) >= 3:
        percentages = [(m.score / m.max_score * 100) for m in recent_marks]
        avg = sum(percentages) / len(percentages)
        variance = sum((x - avg) ** 2 for x in percentages) / len(percentages)
        std_dev = variance ** 0.5
        
        # Lower standard deviation = more consistent = more points
        if std_dev < 5:
            points_breakdown['consistency'] = 15
        elif std_dev < 10:
            points_breakdown['consistency'] = 10
    
    points_breakdown['total'] = sum([
        points_breakdown['attendance'],
        points_breakdown['grades'],
        points_breakdown['improvement'],
        points_breakdown['consistency']
    ])
    
    return points_breakdown


def award_badges(student_id):
    """
    Check badge conditions and award if met
    
    Returns: List of newly awarded badges
    """
    newly_awarded = []
    student = Student.query.get(student_id)
    
    if not student:
        return newly_awarded
    
    # Check Perfect Attendance
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    attendance_records = Attendance.query.filter(
        Attendance.student_id == student_id,
        Attendance.date >= thirty_days_ago.date()
    ).all()
    
    if attendance_records and len(attendance_records) >= 20:  # At least 20 school days
        present = sum(1 for a in attendance_records if a.status == 'present')
        if present == len(attendance_records):
            badge = award_badge_if_not_exists(student_id, 'perfect_attendance')
            if badge:
                newly_awarded.append(badge)
    
    # Check High Achiever
    recent_marks = Marks.query.filter_by(
        student_id=student_id
    ).order_by(desc(Marks.exam_date)).limit(10).all()
    
    if recent_marks and len(recent_marks) >= 5:
        all_above_90 = all((m.score / m.max_score * 100) >= 90 for m in recent_marks[:5])
        if all_above_90:
            badge = award_badge_if_not_exists(student_id, 'high_achiever')
            if badge:
                newly_awarded.append(badge)
    
    # Check Subject Master
    if recent_marks:
        for mark in recent_marks[:5]:
            percentage = (mark.score / mark.max_score * 100)
            if percentage >= 95:
                badge = award_badge_if_not_exists(student_id, 'subject_master')
                if badge:
                    newly_awarded.append(badge)
                break
    
    # Check Improvement Star
    if len(recent_marks) >= 6:
        recent_avg = sum((m.score / m.max_score * 100) for m in recent_marks[:3]) / 3
        older_avg = sum((m.score / m.max_score * 100) for m in recent_marks[3:6]) / 3
        
        if recent_avg - older_avg >= 15:
            badge = award_badge_if_not_exists(student_id, 'improvement_star')
            if badge:
                newly_awarded.append(badge)
    
    # Check Consistent Performer (3 months of 75%+)
    ninety_days_ago = datetime.utcnow() - timedelta(days=90)
    old_marks = Marks.query.filter(
        Marks.student_id == student_id,
        Marks.exam_date >= ninety_days_ago.date()
    ).all()
    
    if old_marks and len(old_marks) >= 6:
        all_above_75 = all((m.score / m.max_score * 100) >= 75 for m in old_marks)
        if all_above_75:
            badge = award_badge_if_not_exists(student_id, 'consistent_performer')
            if badge:
                newly_awarded.append(badge)
    
    # Check Early Bird (no late arrivals)
    if attendance_records:
        no_late = all(a.status != 'late' for a in attendance_records)
        if no_late and len(attendance_records) >= 20:
            badge = award_badge_if_not_exists(student_id, 'early_bird')
            if badge:
                newly_awarded.append(badge)
    
    return newly_awarded


def award_badge_if_not_exists(student_id, badge_key):
    """
    Award a badge if it hasn't been awarded yet
    
    Returns: Achievement object if newly awarded, None otherwise
    """
    badge_info = BADGES.get(badge_key)
    if not badge_info:
        return None
    
    # Check if already awarded
    existing = Achievement.query.filter_by(
        student_id=student_id,
        badge_name=badge_info['name']
    ).first()
    
    if existing:
        return None
    
    # Award new badge
    achievement = Achievement(
        student_id=student_id,
        badge_name=badge_info['name'],
        description=badge_info['description'],
        points=badge_info['points']
    )
    
    try:
        db.session.add(achievement)
        db.session.commit()
        return achievement
    except Exception as e:
        db.session.rollback()
        print(f"Error awarding badge: {e}")
        return None


def get_student_achievements(student_id):
    """
    Get all achievements for a student
    
    Returns: List of achievements with progress
    """
    achievements = Achievement.query.filter_by(
        student_id=student_id
    ).order_by(desc(Achievement.earned_at)).all()
    
    total_points = sum(a.points for a in achievements)
    
    return {
        'achievements': [a.to_dict() for a in achievements],
        'total_points': total_points,
        'badge_count': len(achievements),
        'available_badges': len(BADGES)
    }
