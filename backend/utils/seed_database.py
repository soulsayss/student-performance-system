"""
Comprehensive Database Seeding Script
Generates realistic sample data for the Student Academic Performance System
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Student, Teacher, Attendance, Marks, Assignment, Prediction, Resource, Alert, Achievement, Recommendation, CareerSuggestion
from datetime import datetime, timedelta
import random
import numpy as np

# Sample data
FIRST_NAMES = ['Aarav', 'Vivaan', 'Aditya', 'Arjun', 'Sai', 'Reyansh', 'Ayaan', 'Krishna', 'Ishaan', 'Shaurya',
               'Ananya', 'Diya', 'Aadhya', 'Saanvi', 'Kiara', 'Anika', 'Navya', 'Angel', 'Pari', 'Sara',
               'Rohan', 'Kabir', 'Atharv', 'Advait', 'Vihaan', 'Arnav', 'Dhruv', 'Pranav', 'Rudra', 'Shivansh']

LAST_NAMES = ['Sharma', 'Verma', 'Patel', 'Kumar', 'Singh', 'Gupta', 'Reddy', 'Rao', 'Nair', 'Iyer',
              'Joshi', 'Mehta', 'Desai', 'Kulkarni', 'Agarwal', 'Bansal', 'Malhotra', 'Kapoor', 'Chopra', 'Bhatia']

# 11 Subjects as per requirements
SUBJECTS = ['Science', 'Mathematics', 'History', 'Social Science', 'Geography', 'Hindi', 'English', 'Sports', 'Music', 'Additional Language', 'Arts/Drawing']

# Classes 6-10 as per requirements
CLASSES = ['6', '7', '8', '9', '10']
SECTIONS = ['A', 'B', 'C']

def create_admin():
    """Create admin user"""
    print("Creating admin user...")
    admin = User(
        name="System Administrator",
        email="admin@school.edu",
        role="admin",
        is_active=True
    )
    admin.set_password("Admin@123")
    db.session.add(admin)
    db.session.flush()
    return admin


def create_teachers():
    """Create 10 teachers covering 11 subjects (some teachers handle multiple subjects)"""
    print("Creating 10 teachers...")
    teachers = []
    
    # Teacher data: (name, subject, gender, age)
    # Reduced to 10 teachers, some will handle multiple subjects
    teacher_data = [
        ("Dr. Rajesh Kumar", "Science", "Male", 35),
        ("Prof. Priya Sharma", "Mathematics", "Female", 32),
        ("Mr. Amit Patel", "History", "Male", 38),
        ("Ms. Sneha Gupta", "Social Science", "Female", 30),
        ("Dr. Vikram Singh", "Geography", "Male", 40),
        ("Mrs. Kavita Reddy", "Hindi", "Female", 34),
        ("Mr. Arjun Nair", "English", "Male", 36),
        ("Mr. Rohit Verma", "Sports", "Male", 33),  # MUST be male, age 31-35
        ("Ms. Anjali Mehta", "Music", "Female", 29),
        ("Dr. Meera Iyer", "Additional Language", "Female", 37),
    ]
    
    for i, (name, subject, gender, age) in enumerate(teacher_data, 1):
        # Remove titles first, then convert to email format
        clean_name = name.replace("Dr. ", "").replace("Prof. ", "").replace("Mr. ", "").replace("Mrs. ", "").replace("Ms. ", "")
        email = clean_name.lower().replace(" ", ".") + "@school.com"
        
        user = User(
            name=name,
            email=email,
            role="teacher",
            is_active=True
        )
        user.set_password("Teacher@123")
        db.session.add(user)
        db.session.flush()
        
        teacher = Teacher(
            user_id=user.user_id,
            employee_id=f"TCH{i:03d}",
            subject=subject,
            department="Academic"
        )
        db.session.add(teacher)
        teachers.append((user, teacher))
    
    return teachers

def create_parents():
    """Create 75 parent users (1 per student)"""
    print("Creating 75 parents...")
    parents = []
    
    for i in range(1, 76):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        email = f"parent{i}@email.com"
        
        user = User(
            name=name,
            email=email,
            role="parent",
            is_active=True
        )
        user.set_password("Parent@123")
        db.session.add(user)
        parents.append(user)
    
    db.session.flush()
    return parents


def create_students(parents):
    """Create 75 students across classes 6-10 with performance categories"""
    print("Creating 75 students...")
    students = []
    
    # Performance categories: 23 high (30%), 37 average (50%), 15 at-risk (20%)
    high_performers = 23
    average_performers = 37
    at_risk = 15
    
    categories = ['high'] * high_performers + ['average'] * average_performers + ['at_risk'] * at_risk
    random.shuffle(categories)
    
    student_counter = 1
    
    # Create 15 students per class (6, 7, 8, 9, 10)
    for class_num in CLASSES:
        # 5 students per section (A, B, C)
        for section in SECTIONS:
            for section_student in range(1, 6):
                first_name = random.choice(FIRST_NAMES)
                last_name = random.choice(LAST_NAMES)
                name = f"{first_name} {last_name}"
                email = f"student{student_counter}@school.com"
                
                user = User(
                    name=name,
                    email=email,
                    role="student",
                    is_active=True
                )
                user.set_password("Student@123")
                db.session.add(user)
                db.session.flush()
                
                # Assign parent (each student gets exactly 1 parent)
                parent = parents[student_counter - 1]  # 1-to-1 mapping
                
                # Generate DOB based on class (class 6 = 11-12 years, class 10 = 15-16 years)
                class_int = int(class_num)
                base_age = 11 + (class_int - 6)
                age = base_age + random.randint(0, 1)
                dob = datetime.now().date() - timedelta(days=age*365 + random.randint(0, 365))
                
                student = Student(
                    user_id=user.user_id,
                    roll_number=f"{class_num}{section}{section_student:02d}",
                    class_name=class_num,
                    section=section,
                    parent_id=parent.user_id,
                    dob=dob,
                    gender=random.choice(['Male', 'Female'])
                )
                db.session.add(student)
                students.append((user, student, categories[student_counter - 1]))
                student_counter += 1
    
    db.session.flush()
    return students


def create_attendance(students, teachers):
    """Create 6 months of attendance data"""
    print("Creating 6 months of attendance data...")
    
    # Last 6 months
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=180)
    
    # School days (Monday to Friday)
    current_date = start_date
    attendance_count = 0
    
    while current_date <= end_date:
        # Skip weekends
        if current_date.weekday() < 5:
            for user, student, category in students:
                # Attendance probability based on category
                if category == 'high':
                    status_prob = [0.95, 0.03, 0.02]  # present, absent, late
                elif category == 'average':
                    status_prob = [0.85, 0.10, 0.05]
                else:  # at_risk
                    status_prob = [0.60, 0.30, 0.10]
                
                status = random.choices(['present', 'absent', 'late'], weights=status_prob)[0]
                
                # Random teacher marks attendance
                _, teacher = random.choice(teachers)
                
                attendance = Attendance(
                    student_id=student.student_id,
                    date=current_date,
                    status=status,
                    marked_by=teacher.teacher_id
                )
                db.session.add(attendance)
                attendance_count += 1
        
        current_date += timedelta(days=1)
    
    print(f"  Created {attendance_count} attendance records")


def create_marks(students):
    """Create exam records for all students across all 11 subjects"""
    print("Creating exam records...")
    
    exam_types = [
        ('Unit Test 1', 30, -150),
        ('Unit Test 2', 30, -120),
        ('Midterm', 50, -90),
        ('Unit Test 3', 30, -60),
        ('Unit Test 4', 30, -30),
        ('Final Exam', 100, -10)
    ]
    
    marks_count = 0
    
    for user, student, category in students:
        # Create marks for all 11 subjects
        for subject in SUBJECTS:
            for exam_name, max_score, days_ago in exam_types:
                # Score based on category
                if category == 'high':
                    score = np.random.uniform(0.85, 1.0) * max_score
                elif category == 'average':
                    score = np.random.uniform(0.65, 0.85) * max_score
                else:  # at_risk
                    score = np.random.uniform(0.35, 0.65) * max_score
                
                # Add some randomness
                score = max(0, min(max_score, score + np.random.normal(0, max_score * 0.05)))
                
                exam_date = datetime.now().date() + timedelta(days=days_ago)
                
                marks = Marks(
                    student_id=student.student_id,
                    subject=subject,
                    exam_type=exam_name,
                    score=round(score, 2),
                    max_score=max_score,
                    exam_date=exam_date
                )
                db.session.add(marks)
                marks_count += 1
    
    print(f"  Created {marks_count} marks records")


def create_assignments(students):
    """Create assignments for students across all 11 subjects"""
    print("Creating assignments...")
    
    assignment_titles = [
        "Chapter Summary Essay",
        "Lab Report",
        "Research Project",
        "Problem Set",
        "Case Study Analysis",
        "Group Presentation"
    ]
    
    assignments_count = 0
    
    for user, student, category in students:
        num_assignments = random.randint(5, 10)
        
        for i in range(num_assignments):
            subject = random.choice(SUBJECTS)
            title = random.choice(assignment_titles)
            
            # Due date (past or future)
            days_offset = random.randint(-60, 30)
            due_date = datetime.now().date() + timedelta(days=days_offset)
            
            # Status based on category and due date
            if due_date < datetime.now().date():
                if category == 'high':
                    status = random.choices(['submitted', 'graded'], weights=[0.3, 0.7])[0]
                    submission_date = datetime.now() - timedelta(days=random.randint(1, 10))
                    grade = random.uniform(85, 100) if status == 'graded' else None
                elif category == 'average':
                    status = random.choices(['submitted', 'graded', 'pending'], weights=[0.4, 0.5, 0.1])[0]
                    submission_date = datetime.now() - timedelta(days=random.randint(1, 10)) if status != 'pending' else None
                    grade = random.uniform(70, 85) if status == 'graded' else None
                else:  # at_risk
                    status = random.choices(['submitted', 'graded', 'pending'], weights=[0.2, 0.3, 0.5])[0]
                    submission_date = datetime.now() - timedelta(days=random.randint(1, 10)) if status != 'pending' else None
                    grade = random.uniform(50, 70) if status == 'graded' else None
            else:
                status = 'pending'
                submission_date = None
                grade = None
            
            assignment = Assignment(
                student_id=student.student_id,
                subject=subject,
                title=f"{subject} - {title}",
                description=f"Complete the {title.lower()} for {subject}",
                due_date=due_date,
                status=status,
                submission_date=submission_date,
                grade=grade
            )
            db.session.add(assignment)
            assignments_count += 1
    
    print(f"  Created {assignments_count} assignments")


def create_resources():
    """Create ~66 learning resources across all 11 subjects"""
    print("Creating learning resources...")
    
    resources_data = [
        # Science (6 resources)
        ("Science", "Physics Fundamentals", "Learn the basics of physics", "https://example.com/physics-basics", "video", "beginner"),
        ("Science", "Chemistry Essentials", "Master chemical reactions", "https://example.com/chemistry", "article", "intermediate"),
        ("Science", "Biology Guide", "Understanding living organisms", "https://example.com/biology", "pdf", "beginner"),
        ("Science", "Advanced Science", "Deep dive into scientific concepts", "https://example.com/science-advanced", "video", "advanced"),
        ("Science", "Lab Experiments", "Hands-on science experiments", "https://example.com/lab", "article", "intermediate"),
        ("Science", "Science Quiz", "Test your science knowledge", "https://example.com/science-quiz", "quiz", "beginner"),
        
        # Mathematics (6 resources)
        ("Mathematics", "Calculus Fundamentals", "Learn differential and integral calculus", "https://example.com/calculus", "video", "beginner"),
        ("Mathematics", "Algebra Mastery", "Master algebraic equations", "https://example.com/algebra", "article", "intermediate"),
        ("Mathematics", "Geometry Guide", "Understanding shapes and theorems", "https://example.com/geometry", "pdf", "intermediate"),
        ("Mathematics", "Statistics Basics", "Data analysis and probability", "https://example.com/statistics", "video", "beginner"),
        ("Mathematics", "Advanced Math", "Complex mathematical concepts", "https://example.com/math-advanced", "article", "advanced"),
        ("Mathematics", "Math Quiz", "Test your math skills", "https://example.com/math-quiz", "quiz", "beginner"),
        
        # History (6 resources)
        ("History", "Ancient History", "Learn about ancient civilizations", "https://example.com/ancient-history", "video", "beginner"),
        ("History", "Medieval Period", "Understanding the medieval era", "https://example.com/medieval", "article", "intermediate"),
        ("History", "Modern History", "Recent historical events", "https://example.com/modern-history", "pdf", "intermediate"),
        ("History", "World Wars", "Comprehensive guide to world wars", "https://example.com/world-wars", "video", "advanced"),
        ("History", "Historical Analysis", "Analyzing historical events", "https://example.com/history-analysis", "article", "advanced"),
        ("History", "History Quiz", "Test your history knowledge", "https://example.com/history-quiz", "quiz", "beginner"),
        
        # Social Science (6 resources)
        ("Social Science", "Sociology Basics", "Understanding society", "https://example.com/sociology", "video", "beginner"),
        ("Social Science", "Political Systems", "Government and politics", "https://example.com/politics", "article", "intermediate"),
        ("Social Science", "Economics Intro", "Basic economic concepts", "https://example.com/economics", "pdf", "beginner"),
        ("Social Science", "Social Issues", "Contemporary social problems", "https://example.com/social-issues", "video", "intermediate"),
        ("Social Science", "Cultural Studies", "Understanding cultures", "https://example.com/culture", "article", "intermediate"),
        ("Social Science", "Social Science Quiz", "Test your social science knowledge", "https://example.com/social-quiz", "quiz", "beginner"),
        
        # Geography (6 resources)
        ("Geography", "World Geography", "Learn about world geography", "https://example.com/world-geo", "video", "beginner"),
        ("Geography", "Physical Geography", "Understanding landforms", "https://example.com/physical-geo", "article", "intermediate"),
        ("Geography", "Climate Zones", "Learning about climate patterns", "https://example.com/climate", "pdf", "beginner"),
        ("Geography", "Human Geography", "Understanding human populations", "https://example.com/human-geo", "video", "intermediate"),
        ("Geography", "Map Reading", "How to read and interpret maps", "https://example.com/maps", "article", "beginner"),
        ("Geography", "Geography Quiz", "Test your geography knowledge", "https://example.com/geo-quiz", "quiz", "beginner"),
        
        # Hindi (6 resources)
        ("Hindi", "Hindi Grammar", "Learn Hindi grammar rules", "https://example.com/hindi-grammar", "video", "beginner"),
        ("Hindi", "Hindi Literature", "Understanding Hindi literature", "https://example.com/hindi-lit", "article", "intermediate"),
        ("Hindi", "Hindi Vocabulary", "Expand your Hindi vocabulary", "https://example.com/hindi-vocab", "pdf", "beginner"),
        ("Hindi", "Hindi Poetry", "Appreciating Hindi poetry", "https://example.com/hindi-poetry", "video", "intermediate"),
        ("Hindi", "Hindi Writing", "Improve your Hindi writing", "https://example.com/hindi-writing", "article", "intermediate"),
        ("Hindi", "Hindi Quiz", "Test your Hindi knowledge", "https://example.com/hindi-quiz", "quiz", "beginner"),
        
        # English (6 resources)
        ("English", "English Grammar", "Master English grammar", "https://example.com/english-grammar", "video", "beginner"),
        ("English", "English Literature", "Understanding English literature", "https://example.com/english-lit", "article", "intermediate"),
        ("English", "Vocabulary Building", "Expand your English vocabulary", "https://example.com/vocab", "pdf", "beginner"),
        ("English", "Essay Writing", "Learn to write effective essays", "https://example.com/essays", "video", "intermediate"),
        ("English", "Reading Comprehension", "Improve reading skills", "https://example.com/reading", "article", "intermediate"),
        ("English", "English Quiz", "Test your English knowledge", "https://example.com/english-quiz", "quiz", "beginner"),
        
        # Sports (6 resources)
        ("Sports", "Physical Fitness", "Learn about physical fitness", "https://example.com/fitness", "video", "beginner"),
        ("Sports", "Sports Techniques", "Master sports techniques", "https://example.com/techniques", "article", "intermediate"),
        ("Sports", "Team Sports", "Understanding team sports", "https://example.com/team-sports", "pdf", "beginner"),
        ("Sports", "Sports Nutrition", "Nutrition for athletes", "https://example.com/nutrition", "video", "intermediate"),
        ("Sports", "Sports Psychology", "Mental aspects of sports", "https://example.com/sports-psych", "article", "advanced"),
        ("Sports", "Sports Quiz", "Test your sports knowledge", "https://example.com/sports-quiz", "quiz", "beginner"),
        
        # Music (6 resources)
        ("Music", "Music Theory", "Learn music theory basics", "https://example.com/music-theory", "video", "beginner"),
        ("Music", "Instrument Guide", "Guide to musical instruments", "https://example.com/instruments", "article", "beginner"),
        ("Music", "Classical Music", "Understanding classical music", "https://example.com/classical", "pdf", "intermediate"),
        ("Music", "Music Composition", "Learn to compose music", "https://example.com/composition", "video", "intermediate"),
        ("Music", "Music History", "History of music", "https://example.com/music-history", "article", "intermediate"),
        ("Music", "Music Quiz", "Test your music knowledge", "https://example.com/music-quiz", "quiz", "beginner"),
        
        # Additional Language (6 resources)
        ("Additional Language", "Language Basics", "Learn language fundamentals", "https://example.com/lang-basics", "video", "beginner"),
        ("Additional Language", "Language Grammar", "Master language grammar", "https://example.com/lang-grammar", "article", "intermediate"),
        ("Additional Language", "Vocabulary", "Build language vocabulary", "https://example.com/lang-vocab", "pdf", "beginner"),
        ("Additional Language", "Conversation", "Practice language conversation", "https://example.com/conversation", "video", "intermediate"),
        ("Additional Language", "Language Culture", "Understanding language culture", "https://example.com/lang-culture", "article", "intermediate"),
        ("Additional Language", "Language Quiz", "Test your language knowledge", "https://example.com/lang-quiz", "quiz", "beginner"),
        
        # Arts/Drawing (6 resources)
        ("Arts/Drawing", "Drawing Basics", "Learn basic drawing techniques", "https://example.com/drawing-basics", "video", "beginner"),
        ("Arts/Drawing", "Color Theory", "Understanding color theory", "https://example.com/color", "article", "intermediate"),
        ("Arts/Drawing", "Perspective Drawing", "Master perspective drawing", "https://example.com/perspective", "pdf", "intermediate"),
        ("Arts/Drawing", "Portrait Drawing", "Learn portrait drawing", "https://example.com/portraits", "video", "intermediate"),
        ("Arts/Drawing", "Art History", "Understanding art history", "https://example.com/art-history", "article", "advanced"),
        ("Arts/Drawing", "Art Quiz", "Test your art knowledge", "https://example.com/art-quiz", "quiz", "beginner"),
    ]
    
    for subject, title, desc, link, res_type, difficulty in resources_data:
        resource = Resource(
            subject=subject,
            title=title,
            description=desc,
            link=link,
            resource_type=res_type,
            difficulty=difficulty
        )
        db.session.add(resource)
    
    print(f"  Created {len(resources_data)} learning resources")
    return resources_data


def create_alerts(students):
    """Create alerts for students based on performance category"""
    print("Creating alerts...")
    
    alert_messages = {
        'critical': [
            "Your attendance has dropped below 60%. Immediate action required.",
            "Multiple assignments are overdue. Please submit them urgently.",
            "Your performance in recent exams is concerning. Please meet with your teacher.",
            "Risk of failing in {subject}. Extra classes recommended."
        ],
        'warning': [
            "Your attendance is below 75%. Please improve.",
            "Assignment due tomorrow: {subject}",
            "Your marks in {subject} need improvement.",
            "You have 3 pending assignments. Please complete them soon."
        ],
        'info': [
            "Great job on your recent {subject} exam!",
            "Keep up the excellent attendance record!",
            "You've earned a new achievement badge!",
            "New learning resources available for {subject}."
        ]
    }
    
    alerts_count = 0
    
    for user, student, category in students:
        if category == 'at_risk':
            # Critical alerts for at-risk students
            num_alerts = random.randint(3, 6)
            for _ in range(num_alerts):
                severity = random.choices(['critical', 'warning'], weights=[0.6, 0.4])[0]
                message = random.choice(alert_messages[severity])
                if '{subject}' in message:
                    message = message.format(subject=random.choice(SUBJECTS))
                
                alert = Alert(
                    student_id=student.student_id,
                    message=message,
                    severity=severity,
                    is_read=random.choice([True, False])
                )
                db.session.add(alert)
                alerts_count += 1
        
        elif category == 'average':
            # Some warnings for average students
            if random.random() > 0.5:
                num_alerts = random.randint(1, 3)
                for _ in range(num_alerts):
                    severity = random.choices(['warning', 'info'], weights=[0.6, 0.4])[0]
                    message = random.choice(alert_messages[severity])
                    if '{subject}' in message:
                        message = message.format(subject=random.choice(SUBJECTS))
                    
                    alert = Alert(
                        student_id=student.student_id,
                        message=message,
                        severity=severity,
                        is_read=random.choice([True, False])
                    )
                    db.session.add(alert)
                    alerts_count += 1
        
        else:  # high performers
            # Positive info alerts
            if random.random() > 0.3:
                num_alerts = random.randint(1, 2)
                for _ in range(num_alerts):
                    message = random.choice(alert_messages['info'])
                    if '{subject}' in message:
                        message = message.format(subject=random.choice(SUBJECTS))
                    
                    alert = Alert(
                        student_id=student.student_id,
                        message=message,
                        severity='info',
                        is_read=random.choice([True, False])
                    )
                    db.session.add(alert)
                    alerts_count += 1
    
    print(f"  Created {alerts_count} alerts")


def create_achievements(students):
    """Create achievements for top performers"""
    print("Creating achievements...")
    
    achievement_badges = [
        ("Perfect Attendance", 100, "No absences for a month"),
        ("Top Scorer", 150, "Scored above 95% in any subject"),
        ("Consistent Performer", 120, "Maintained above 85% for 3 months"),
        ("Quick Learner", 75, "Completed 5 learning modules"),
        ("Assignment Master", 80, "Submitted all assignments on time"),
        ("Quiz Champion", 90, "Scored 100% in 3 quizzes"),
        ("Subject Expert", 110, "Scored above 90% in all exams of a subject"),
        ("Improvement Star", 85, "Improved marks by 20% or more"),
        ("Participation Pro", 70, "Active class participation"),
        ("Study Streak", 95, "Maintained study routine for 30 days")
    ]
    
    achievements_count = 0
    
    for user, student, category in students:
        if category == 'high':
            # High performers get multiple achievements
            num_achievements = random.randint(3, 6)
            selected_badges = random.sample(achievement_badges, num_achievements)
            
            for badge_name, points, description in selected_badges:
                days_ago = random.randint(1, 150)
                earned_at = datetime.now() - timedelta(days=days_ago)
                
                achievement = Achievement(
                    student_id=student.student_id,
                    badge_name=badge_name,
                    points=points,
                    description=description,
                    earned_at=earned_at
                )
                db.session.add(achievement)
                achievements_count += 1
        
        elif category == 'average':
            # Average students get some achievements
            if random.random() > 0.4:
                num_achievements = random.randint(1, 3)
                selected_badges = random.sample(achievement_badges, num_achievements)
                
                for badge_name, points, description in selected_badges:
                    days_ago = random.randint(1, 150)
                    earned_at = datetime.now() - timedelta(days=days_ago)
                    
                    achievement = Achievement(
                        student_id=student.student_id,
                        badge_name=badge_name,
                        points=points,
                        description=description,
                        earned_at=earned_at
                    )
                    db.session.add(achievement)
                    achievements_count += 1
    
    print(f"  Created {achievements_count} achievements")


def create_predictions(students):
    """Create ML predictions for students"""
    print("Creating predictions...")
    
    predictions_count = 0
    
    for user, student, category in students:
        # Generate prediction based on category
        if category == 'high':
            predicted_grade = random.choice(['A+', 'A'])
            risk_level = 'low'
            confidence = random.uniform(0.85, 0.95)
            factors = {
                'attendance': 'excellent',
                'marks_trend': 'excellent',
                'assignment_completion': 'excellent'
            }
        elif category == 'average':
            predicted_grade = random.choice(['B+', 'B', 'C+'])
            risk_level = 'low'
            confidence = random.uniform(0.70, 0.85)
            factors = {
                'attendance': 'good',
                'marks_trend': 'good',
                'assignment_completion': 'good'
            }
        else:  # at_risk
            predicted_grade = random.choice(['C', 'D', 'F'])
            risk_level = random.choice(['medium', 'high'])
            confidence = random.uniform(0.60, 0.75)
            factors = {
                'attendance': 'poor',
                'marks_trend': 'poor',
                'assignment_completion': 'needs_improvement'
            }
        
        prediction = Prediction(
            student_id=student.student_id,
            predicted_grade=predicted_grade,
            risk_level=risk_level,
            confidence_score=round(confidence, 4),
            factors=factors
        )
        db.session.add(prediction)
        predictions_count += 1
    
    print(f"  Created {predictions_count} predictions")

def create_recommendations(students):
    """Create personalized recommendations"""
    print("Creating recommendations...")
    
    db.session.flush()  # Ensure resources are available
    
    resources = Resource.query.all()
    recommendations_count = 0
    
    for user, student, category in students:
        # Number of recommendations based on category
        if category == 'at_risk':
            num_recs = random.randint(5, 8)
        elif category == 'average':
            num_recs = random.randint(2, 4)
        else:
            num_recs = random.randint(1, 3)
        
        # Select random resources
        selected_resources = random.sample(resources, min(num_recs, len(resources)))
        
        for resource in selected_resources:
            reason = f"Based on your performance in {resource.subject}"
            is_completed = random.choice([True, False]) if category == 'high' else False
            
            recommendation = Recommendation(
                student_id=student.student_id,
                resource_id=resource.resource_id,
                reason=reason,
                is_completed=is_completed
            )
            db.session.add(recommendation)
            recommendations_count += 1
    
    print(f"  Created {recommendations_count} recommendations")


def create_career_suggestions(students):
    """Create career suggestions for students"""
    print("Creating career suggestions...")
    
    career_paths = [
        ("Software Engineer", ["Programming", "Problem Solving", "Mathematics"], "Develop software applications and systems"),
        ("Data Scientist", ["Statistics", "Python", "Machine Learning"], "Analyze data and build predictive models"),
        ("Doctor", ["Biology", "Chemistry", "Empathy"], "Provide medical care and treatment"),
        ("Mechanical Engineer", ["Physics", "Mathematics", "CAD"], "Design and build mechanical systems"),
        ("Teacher", ["Communication", "Subject Knowledge", "Patience"], "Educate and inspire students"),
        ("Business Analyst", ["Economics", "Analytics", "Communication"], "Analyze business processes and data"),
        ("Architect", ["Mathematics", "Creativity", "Design"], "Design buildings and structures"),
        ("Lawyer", ["English", "Critical Thinking", "Research"], "Provide legal counsel and representation"),
        ("Chartered Accountant", ["Mathematics", "Accounting", "Attention to Detail"], "Manage financial records and audits"),
        ("Civil Engineer", ["Physics", "Mathematics", "Planning"], "Design infrastructure and construction projects")
    ]
    
    suggestions_count = 0
    
    for user, student, category in students:
        # Number of suggestions
        num_suggestions = random.randint(3, 5)
        selected_careers = random.sample(career_paths, num_suggestions)
        
        for i, (career, skills, desc) in enumerate(selected_careers):
            # Match percentage based on category and rank
            if category == 'high':
                base_match = random.uniform(80, 95)
            elif category == 'average':
                base_match = random.uniform(65, 80)
            else:
                base_match = random.uniform(50, 65)
            
            # Decrease match for lower ranked suggestions
            match_percentage = base_match - (i * 5)
            
            suggestion = CareerSuggestion(
                student_id=student.student_id,
                career_path=career,
                match_percentage=round(match_percentage, 2),
                description=desc,
                required_skills=skills
            )
            db.session.add(suggestion)
            suggestions_count += 1
    
    print(f"  Created {suggestions_count} career suggestions")

def seed_all_data():
    """Seed all data into the database (called from app.py)"""
    print("\n" + "="*60)
    print("STUDENT ACADEMIC PERFORMANCE SYSTEM - DATABASE SEEDING")
    print("="*60 + "\n")
    
    # Create data
    admin = create_admin()
    teachers = create_teachers()
    parents = create_parents()
    students = create_students(parents)
    
    print("\nCommitting users to database...")
    db.session.commit()
    print("✅ Users created\n")
    
    # Create related data
    create_attendance(students, teachers)
    create_marks(students)
    create_assignments(students)
    create_resources()
    create_alerts(students)
    create_achievements(students)
    create_predictions(students)
    create_recommendations(students)
    create_career_suggestions(students)
    
    print("\nCommitting all data to database...")
    db.session.commit()
    
    print("\n" + "="*60)
    print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"  • 1 Admin user")
    print(f"  • 15 Teachers (11 subjects)")
    print(f"  • 150 Parents")
    print(f"  • 150 Students (45 high, 75 average, 30 at-risk)")
    print(f"  • Classes 6-10 (30 students per class, 10 per section)")
    print(f"  • ~19,500 Attendance records (6 months)")
    print(f"  • ~9,900 Marks records (6 exams × 11 subjects × 150 students)")
    print(f"  • ~1,125 Assignments")
    print(f"  • 66 Learning resources (6 per subject)")
    print(f"  • ~270 Alerts")
    print(f"  • ~400 Achievements")
    print(f"  • 150 Predictions")
    print(f"  • ~600 Recommendations")
    print(f"  • ~600 Career suggestions")
    print(f"  • Total Users: 161 (1 admin + 10 teachers + 75 students + 75 parents)")
    
    print(f"\n🔑 Login Credentials:")
    print(f"  Admin:   admin@school.edu / Admin@123")
    print(f"  Teacher: rajesh.kumar@school.com / Teacher@123")
    print(f"  Parent:  parent1@email.com / Parent@123")
    print(f"  Student: student1@school.com / Student@123")
    
    print(f"\n✅ Database ready for use!")
    print("="*60 + "\n")

def main():
    """Main seeding function for CLI usage"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate
        print("Dropping existing tables...")
        db.drop_all()
        print("Creating fresh tables...")
        db.create_all()
        print("✅ Database schema created\n")
        
        seed_all_data()
