"""
Script to seed sample data for testing
"""
from app import create_app
from models import db, User, Student, Teacher, Attendance, Marks, Prediction, Achievement, Alert, CareerSuggestion, Resource, Recommendation, Assignment
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    print("Seeding sample data...")
    
    # Get John Doe (student_id = 1)
    student = Student.query.get(1)
    
    if not student:
        print("Student not found! Please register first.")
        exit()
    
    print(f"Adding data for student: {student.user.name}")
    
    # Add Attendance Records (last 3 months)
    print("Adding attendance records...")
    for i in range(60):  # 60 days
        date = datetime.utcnow().date() - timedelta(days=i)
        status = random.choices(['present', 'absent', 'late'], weights=[85, 10, 5])[0]
        
        attendance = Attendance(
            student_id=student.student_id,
            date=date,
            status=status,
            marked_by=1  # Teacher ID
        )
        db.session.add(attendance)
    
    # Add Marks
    print("Adding marks...")
    subjects = ['Mathematics', 'Physics', 'Chemistry', 'English', 'Computer Science']
    exam_types = ['midterm', 'final', 'quiz']
    
    for subject in subjects:
        for exam_type in exam_types:
            score = random.uniform(60, 95)
            marks = Marks(
                student_id=student.student_id,
                subject=subject,
                exam_type=exam_type,
                score=score,
                max_score=100,
                exam_date=datetime.utcnow().date() - timedelta(days=random.randint(1, 90))
            )
            db.session.add(marks)
    
    # Add Prediction
    print("Adding prediction...")
    prediction = Prediction(
        student_id=student.student_id,
        predicted_grade='A',
        risk_level='low',
        confidence_score=0.87,
        factors={
            'attendance': 'good',
            'marks_trend': 'improving',
            'assignment_completion': 'excellent'
        }
    )
    db.session.add(prediction)
    
    # Add Resources
    print("Adding resources...")
    resources_data = [
        {
            'subject': 'Mathematics',
            'title': 'Calculus Fundamentals',
            'description': 'Learn the basics of calculus',
            'link': 'https://example.com/calculus',
            'resource_type': 'video',
            'difficulty': 'intermediate'
        },
        {
            'subject': 'Physics',
            'title': 'Newton\'s Laws Explained',
            'description': 'Understanding motion and forces',
            'link': 'https://example.com/newton',
            'resource_type': 'article',
            'difficulty': 'beginner'
        },
        {
            'subject': 'Computer Science',
            'title': 'Python Programming Guide',
            'description': 'Complete Python tutorial',
            'link': 'https://example.com/python',
            'resource_type': 'pdf',
            'difficulty': 'intermediate'
        }
    ]
    
    resource_ids = []
    for res_data in resources_data:
        resource = Resource(**res_data)
        db.session.add(resource)
        db.session.flush()
        resource_ids.append(resource.resource_id)
    
    # Add Recommendations
    print("Adding recommendations...")
    for resource_id in resource_ids[:2]:
        recommendation = Recommendation(
            student_id=student.student_id,
            resource_id=resource_id,
            reason='Based on your recent performance in this subject',
            is_completed=False
        )
        db.session.add(recommendation)
    
    # Add Achievements
    print("Adding achievements...")
    achievements_data = [
        {'badge_name': 'Perfect Attendance', 'points': 100, 'description': 'No absences for a month'},
        {'badge_name': 'Top Scorer', 'points': 150, 'description': 'Scored above 90% in Mathematics'},
        {'badge_name': 'Quick Learner', 'points': 75, 'description': 'Completed 5 learning modules'}
    ]
    
    for ach_data in achievements_data:
        achievement = Achievement(
            student_id=student.student_id,
            **ach_data
        )
        db.session.add(achievement)
    
    # Add Alerts
    print("Adding alerts...")
    alerts_data = [
        {'message': 'Assignment due tomorrow: Physics Lab Report', 'severity': 'warning', 'is_read': False},
        {'message': 'Great job! You scored 95% in Mathematics', 'severity': 'info', 'is_read': True},
        {'message': 'Your attendance is below 75%. Please improve.', 'severity': 'critical', 'is_read': False}
    ]
    
    for alert_data in alerts_data:
        alert = Alert(
            student_id=student.student_id,
            **alert_data
        )
        db.session.add(alert)
    
    # Add Career Suggestions
    print("Adding career suggestions...")
    careers_data = [
        {
            'career_path': 'Software Engineer',
            'match_percentage': 92.5,
            'description': 'Build software applications and systems',
            'required_skills': ['Programming', 'Problem Solving', 'Mathematics']
        },
        {
            'career_path': 'Data Scientist',
            'match_percentage': 88.3,
            'description': 'Analyze data and build ML models',
            'required_skills': ['Statistics', 'Python', 'Machine Learning']
        },
        {
            'career_path': 'Mechanical Engineer',
            'match_percentage': 75.0,
            'description': 'Design and build mechanical systems',
            'required_skills': ['Physics', 'CAD', 'Mathematics']
        }
    ]
    
    for career_data in careers_data:
        career = CareerSuggestion(
            student_id=student.student_id,
            **career_data
        )
        db.session.add(career)
    
    # Add Assignments
    print("Adding assignments...")
    assignments_data = [
        {
            'subject': 'Physics',
            'title': 'Lab Report: Newton\'s Laws',
            'description': 'Complete the lab report',
            'due_date': datetime.utcnow().date() + timedelta(days=1),
            'status': 'pending'
        },
        {
            'subject': 'Mathematics',
            'title': 'Calculus Problem Set',
            'description': 'Solve problems 1-20',
            'due_date': datetime.utcnow().date() + timedelta(days=5),
            'status': 'pending'
        }
    ]
    
    for assign_data in assignments_data:
        assignment = Assignment(
            student_id=student.student_id,
            **assign_data
        )
        db.session.add(assignment)
    
    # Commit all changes
    db.session.commit()
    print("\n✅ Sample data seeded successfully!")
    print("You can now test all student endpoints with real data.")
