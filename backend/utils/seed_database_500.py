"""
COMPREHENSIVE SCHOOL DATABASE POPULATION - 1,016 USERS & 100,000+ RECORDS
Generates realistic sample data for a full-scale school system with 500 students
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Student, Teacher, Attendance, Marks, Assignment, Prediction, Resource, Alert, Achievement, Recommendation, CareerSuggestion
from datetime import datetime, timedelta
import random
import json

# Indian boy names (for 28 boys per section)
BOY_NAMES = ['Aarav', 'Aditya', 'Arjun', 'Ayaan', 'Dhruv', 'Ishaan', 'Kabir', 'Krishna',
             'Pranav', 'Reyansh', 'Rohan', 'Shaurya', 'Vihaan', 'Vivaan', 'Advait', 'Arnav',
             'Atharv', 'Sai', 'Shivansh', 'Virat', 'Aryan', 'Dev', 'Rudra', 'Yash',
             'Aaditya', 'Kian', 'Aarush', 'Advik', 'Ansh', 'Darsh']

# Indian girl names (for 22 girls per section)
GIRL_NAMES = ['Aadhya', 'Ananya', 'Anika', 'Diya', 'Kiara', 'Navya', 'Pari', 'Saanvi',
              'Sara', 'Angel', 'Aarohi', 'Aanya', 'Myra', 'Riya', 'Shanaya', 'Siya',
              'Aditi', 'Ishita', 'Jiya', 'Kavya', 'Pihu', 'Tara', 'Avni', 'Ira']

# Indian last names
LAST_NAMES = ['Sharma', 'Patel', 'Kumar', 'Singh', 'Gupta', 'Reddy', 'Iyer', 'Malhotra',
              'Kapoor', 'Verma', 'Agarwal', 'Joshi', 'Nair', 'Mehta', 'Chopra', 'Desai',
              'Rao', 'Bhatia', 'Bansal', 'Shah', 'Khanna', 'Sethi', 'Arora', 'Saxena']

# Parent first names
PARENT_NAMES = ['Rajesh', 'Sunita', 'Amit', 'Priya', 'Vikram', 'Kavita', 'Suresh', 'Anjali',
                'Arun', 'Deepa', 'Ramesh', 'Neeta', 'Sanjay', 'Meera', 'Ashok', 'Pooja',
                'Manoj', 'Rekha', 'Vinod', 'Geeta', 'Ravi', 'Shobha', 'Prakash', 'Usha']

# 11 Subjects
SUBJECTS = ['Science', 'Mathematics', 'History', 'Social Science', 'Geography', 
            'Hindi', 'English', 'Sports', 'Music', 'Additional Language', 'Arts/Drawing']

# 10 sections (5 classes × 2 sections)
CLASSES = ['6', '7', '8', '9', '10']
SECTIONS = ['A', 'B']
STUDENTS_PER_SECTION = 50  # 28 boys + 22 girls
TOTAL_STUDENTS = 500  # 5 classes × 2 sections × 50 students


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
    print("✅ Admin created: admin@school.edu / Admin@123")
    return admin


def create_teachers():
    """Create 15 teachers covering all 11 subjects"""
    print("Creating 15 teachers...")
    teachers = []
    
    teachers_data = [
        # SCIENCE (2 teachers)
        ('Dr. Rajesh Kumar', 'rajesh.kumar@school.com', 'Science', 'TCH001', 35, 'Male', 'PhD in Physics', 10),
        ('Dr. Priya Malhotra', 'priya.malhotra@school.com', 'Science', 'TCH002', 28, 'Female', 'MSc in Chemistry', 5),
        
        # MATHEMATICS (2 teachers)
        ('Prof. Amit Sharma', 'amit.sharma@school.com', 'Mathematics', 'TCH003', 32, 'Male', 'MSc in Mathematics', 8),
        ('Mrs. Sneha Kapoor', 'sneha.kapoor@school.com', 'Mathematics', 'TCH004', 29, 'Female', 'MSc in Applied Mathematics', 6),
        
        # HISTORY (1 teacher)
        ('Mr. Vikram Patel', 'vikram.patel@school.com', 'History', 'TCH005', 38, 'Male', 'MA in History', 12),
        
        # SOCIAL SCIENCE (2 teachers)
        ('Ms. Anjali Reddy', 'anjali.reddy@school.com', 'Social Science', 'TCH006', 30, 'Female', 'MA in Sociology', 7),
        ('Dr. Nikhil Desai', 'nikhil.desai@school.com', 'Social Science', 'TCH007', 42, 'Male', 'PhD in Political Science', 15),
        
        # GEOGRAPHY (1 teacher)
        ('Mr. Suresh Iyer', 'suresh.iyer@school.com', 'Geography', 'TCH008', 40, 'Male', 'MA in Geography', 14),
        
        # HINDI (1 teacher)
        ('Mrs. Kavita Singh', 'kavita.singh@school.com', 'Hindi', 'TCH009', 34, 'Female', 'MA in Hindi Literature', 9),
        
        # ENGLISH (2 teachers)
        ('Mr. Arjun Nair', 'arjun.nair@school.com', 'English', 'TCH010', 36, 'Male', 'MA in English Literature', 11),
        ('Mrs. Deepa Rao', 'deepa.rao@school.com', 'English', 'TCH011', 33, 'Female', 'MA in English', 8),
        
        # SPORTS (1 teacher - MUST BE MALE, AGE 31-35)
        ('Mr. Rohit Verma', 'rohit.verma@school.com', 'Sports', 'TCH012', 33, 'Male', 'BPEd, MPEd', 7),
        
        # MUSIC (1 teacher)
        ('Ms. Pooja Mehta', 'pooja.mehta@school.com', 'Music', 'TCH013', 29, 'Female', 'MA in Music', 5),
        
        # ADDITIONAL LANGUAGE (1 teacher)
        ('Dr. Meera Gupta', 'meera.gupta@school.com', 'Additional Language', 'TCH014', 37, 'Female', 'MA in Sanskrit', 10),
        
        # ARTS/DRAWING (1 teacher)
        ('Prof. Karan Joshi', 'karan.joshi@school.com', 'Arts/Drawing', 'TCH015', 31, 'Male', 'BFA, MFA', 6)
    ]
    
    for name, email, subject, emp_id, age, gender, qualification, experience in teachers_data:
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
            employee_id=emp_id,
            subject=subject,
            department="Academic",
            is_class_teacher=False,
            assigned_class=None,
            assigned_section=None
        )
        db.session.add(teacher)
        teachers.append((user, teacher))
    
    print(f"✅ Created 15 teachers (all passwords: Teacher@123)")
    return teachers



def create_students_and_parents():
    """Create 500 students and 500 parents (1:1 relationship)"""
    print("Creating 500 students and 500 parents...")
    
    # Performance distribution: 150 high (30%), 250 average (50%), 100 at-risk (20%)
    performance_categories = (['high'] * 150 + ['average'] * 250 + ['at_risk'] * 100)
    random.shuffle(performance_categories)
    
    all_students = []
    student_counter = 0
    batch_size = 50
    
    # Loop through classes and sections
    for class_num in CLASSES:
        for section in SECTIONS:
            print(f"  Creating Class {class_num}{section}...", end='', flush=True)
            
            # Create 28 boys
            for i in range(28):
                student_counter += 1
                roll_number = f"{class_num}{section}{str(i+1).zfill(2)}"
                
                # Generate unique names
                first_name = random.choice(BOY_NAMES)
                last_name = random.choice(LAST_NAMES)
                student_email = f"{first_name.lower()}.{last_name.lower()}{student_counter}@gmail.com"
                
                # Create parent first
                parent_first = random.choice(PARENT_NAMES)
                parent_email = f"parent.{last_name.lower()}{student_counter}@gmail.com"
                
                parent_user = User(
                    name=f"{parent_first} {last_name}",
                    email=parent_email,
                    role="parent",
                    is_active=True
                )
                parent_user.set_password("Parent@123")
                db.session.add(parent_user)
                db.session.flush()
                
                # Create student
                student_user = User(
                    name=f"{first_name} {last_name}",
                    email=student_email,
                    role="student",
                    is_active=True
                )
                student_user.set_password("Student@123")
                db.session.add(student_user)
                db.session.flush()
                
                # Performance category
                category = performance_categories[student_counter - 1]
                
                # Determine marks and attendance based on performance
                if category == 'high':
                    attendance_pct = random.uniform(95, 100)
                    avg_marks = random.uniform(85, 100)
                    risk_level = 'low'
                elif category == 'average':
                    attendance_pct = random.uniform(75, 90)
                    avg_marks = random.uniform(65, 85)
                    risk_level = random.choice(['low', 'medium'])
                else:  # at_risk
                    attendance_pct = random.uniform(30, 65)
                    avg_marks = random.uniform(35, 65)
                    risk_level = random.choice(['medium', 'high'])
                
                # Calculate age based on class
                base_age = 11 + int(class_num) - 6  # Class 6 = 11 years, Class 10 = 15 years
                age = base_age + random.randint(0, 1)
                dob = datetime.now().date() - timedelta(days=age*365 + random.randint(0, 365))
                
                student = Student(
                    user_id=student_user.user_id,
                    roll_number=roll_number,
                    class_name=class_num,
                    section=section,
                    parent_id=parent_user.user_id,
                    dob=dob,
                    gender='Male'
                )
                db.session.add(student)
                all_students.append({
                    'student': student,
                    'user': student_user,
                    'category': category,
                    'risk_level': risk_level
                })
            
            # Create 22 girls
            for i in range(22):
                student_counter += 1
                roll_number = f"{class_num}{section}{str(28+i+1).zfill(2)}"
                
                first_name = random.choice(GIRL_NAMES)
                last_name = random.choice(LAST_NAMES)
                student_email = f"{first_name.lower()}.{last_name.lower()}{student_counter}@gmail.com"
                
                parent_first = random.choice(PARENT_NAMES)
                parent_email = f"parent.{last_name.lower()}{student_counter}@gmail.com"
                
                parent_user = User(
                    name=f"{parent_first} {last_name}",
                    email=parent_email,
                    role="parent",
                    is_active=True
                )
                parent_user.set_password("Parent@123")
                db.session.add(parent_user)
                db.session.flush()
                
                student_user = User(
                    name=f"{first_name} {last_name}",
                    email=student_email,
                    role="student",
                    is_active=True
                )
                student_user.set_password("Student@123")
                db.session.add(student_user)
                db.session.flush()
                
                category = performance_categories[student_counter - 1]
                
                if category == 'high':
                    attendance_pct = random.uniform(95, 100)
                    avg_marks = random.uniform(85, 100)
                    risk_level = 'low'
                elif category == 'average':
                    attendance_pct = random.uniform(75, 90)
                    avg_marks = random.uniform(65, 85)
                    risk_level = random.choice(['low', 'medium'])
                else:
                    attendance_pct = random.uniform(30, 65)
                    avg_marks = random.uniform(35, 65)
                    risk_level = random.choice(['medium', 'high'])
                
                base_age = 11 + int(class_num) - 6
                age = base_age + random.randint(0, 1)
                dob = datetime.now().date() - timedelta(days=age*365 + random.randint(0, 365))
                
                student = Student(
                    user_id=student_user.user_id,
                    roll_number=roll_number,
                    class_name=class_num,
                    section=section,
                    parent_id=parent_user.user_id,
                    dob=dob,
                    gender='Female'
                )
                db.session.add(student)
                all_students.append({
                    'student': student,
                    'user': student_user,
                    'category': category,
                    'risk_level': risk_level
                })
                
                # Batch commit every 50 students
                if student_counter % batch_size == 0:
                    db.session.flush()
                    print('.', end='', flush=True)
            
            print(' ✓')
    
    db.session.flush()
    print(f"✅ Created 500 students and 500 parents")
    print(f"   - Each section has 50 students (28 boys, 22 girls)")
    print(f"   - High performers: 150 (30%)")
    print(f"   - Average performers: 250 (50%)")
    print(f"   - At-risk students: 100 (20%)")
    
    return all_students



def create_attendance(students, teachers):
    """Create 65,000 attendance records (500 students × 130 school days)"""
    print("📊 Creating attendance records...", end='', flush=True)
    
    school_days = 130  # 6 months of school
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=180)
    
    attendance_count = 0
    current_date = start_date
    batch_size = 1000
    
    while current_date <= end_date:
        # Skip weekends
        if current_date.weekday() < 5:
            for student_data in students:
                student = student_data['student']
                category = student_data['category']
                
                # Attendance probability based on category
                if category == 'high':
                    is_present = random.random() < 0.98
                elif category == 'average':
                    is_present = random.random() < 0.82
                else:  # at_risk
                    is_present = random.random() < 0.45
                
                # Random teacher marks attendance
                _, teacher = random.choice(teachers)
                
                attendance = Attendance(
                    student_id=student.student_id,
                    date=current_date,
                    status='present' if is_present else 'absent',
                    marked_by=teacher.teacher_id
                )
                db.session.add(attendance)
                attendance_count += 1
                
                # Batch commit
                if attendance_count % batch_size == 0:
                    db.session.flush()
                    print('.', end='', flush=True)
        
        current_date += timedelta(days=1)
    
    db.session.flush()
    print(f" ✅ Created {attendance_count:,} attendance records")


def create_marks(students):
    """Create 33,000 marks records (500 students × 6 exams × 11 subjects)"""
    print("📊 Creating marks records...", end='', flush=True)
    
    exams = [
        ('Unit Test 1', 30, -150),
        ('Unit Test 2', 30, -120),
        ('Midterm', 50, -90),
        ('Unit Test 3', 30, -60),
        ('Unit Test 4', 30, -30),
        ('Final Exam', 100, -10)
    ]
    
    marks_count = 0
    batch_size = 1000
    
    for student_data in students:
        student = student_data['student']
        category = student_data['category']
        
        for subject in SUBJECTS:
            for exam_name, max_score, days_ago in exams:
                # Score based on category
                if category == 'high':
                    score = random.uniform(0.85, 1.0) * max_score
                elif category == 'average':
                    score = random.uniform(0.65, 0.85) * max_score
                else:  # at_risk
                    score = random.uniform(0.35, 0.65) * max_score
                
                # Add some randomness
                score = max(0, min(max_score, score + random.uniform(-max_score*0.05, max_score*0.05)))
                
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
                
                # Batch commit
                if marks_count % batch_size == 0:
                    db.session.flush()
                    print('.', end='', flush=True)
    
    db.session.flush()
    print(f" ✅ Created {marks_count:,} marks records")


def create_assignments(students):
    """Create ~3,750 assignments (500 students × 7-8 assignments)"""
    print("📊 Creating assignments...")
    
    assignment_titles = [
        "Chapter Summary Essay",
        "Lab Report",
        "Research Project",
        "Problem Set",
        "Case Study Analysis",
        "Group Presentation",
        "Homework Assignment"
    ]
    
    assignments_count = 0
    
    for student_data in students:
        student = student_data['student']
        category = student_data['category']
        
        num_assignments = random.randint(7, 10)
        
        for i in range(num_assignments):
            subject = random.choice(SUBJECTS)
            title = random.choice(assignment_titles)
            
            days_offset = random.randint(-60, 30)
            due_date = datetime.now().date() + timedelta(days=days_offset)
            
            if due_date < datetime.now().date():
                if category == 'high':
                    status = random.choice(['submitted', 'graded', 'graded'])
                    submission_date = datetime.now() - timedelta(days=random.randint(1, 10))
                    grade = random.uniform(85, 100) if status == 'graded' else None
                elif category == 'average':
                    status = random.choice(['submitted', 'graded', 'pending'])
                    submission_date = datetime.now() - timedelta(days=random.randint(1, 10)) if status != 'pending' else None
                    grade = random.uniform(65, 85) if status == 'graded' else None
                else:
                    status = random.choice(['pending', 'pending', 'submitted'])
                    submission_date = datetime.now() - timedelta(days=random.randint(1, 10)) if status == 'submitted' else None
                    grade = random.uniform(40, 65) if status == 'graded' else None
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
    
    print(f"✅ Created {assignments_count:,} assignments")



def create_alerts(students):
    """Create ~1,050 alerts"""
    print("📊 Creating alerts...")
    
    alert_types = ['attendance_low', 'marks_low', 'behavior_issue', 'fee_pending', 'assignment_overdue']
    
    alerts_count = 0
    
    for student_data in students:
        student = student_data['student']
        category = student_data['category']
        
        if category == 'at_risk':
            num_alerts = random.randint(4, 7)
            severity = random.choice(['high', 'critical'])
        elif category == 'average':
            num_alerts = random.randint(1, 3) if random.random() < 0.5 else 0
            severity = random.choice(['medium', 'low'])
        else:
            num_alerts = random.randint(0, 2)
            severity = 'low'
        
        for i in range(num_alerts):
            alert = Alert(
                student_id=student.student_id,
                message=f"Alert for {student_data['user'].name}",
                severity=severity,
                is_read=random.choice([True, False])
            )
            db.session.add(alert)
            alerts_count += 1
    
    print(f"✅ Created {alerts_count:,} alerts")


def create_achievements(students):
    """Create ~1,125 achievements"""
    print("📊 Creating achievements...")
    
    achievement_types = [
        ('Academic Excellence', 150),
        ('100% Attendance', 100),
        ('Sports Champion', 120),
        ('Best Student', 180),
        ('Cultural Award', 90),
        ('Science Fair Winner', 110),
        ('Math Olympiad', 130),
        ('Debate Winner', 100),
        ('Art Competition', 80)
    ]
    
    achievements_count = 0
    
    for student_data in students:
        student = student_data['student']
        category = student_data['category']
        
        if category == 'high':
            num_achievements = random.randint(3, 6)
        elif category == 'average':
            num_achievements = random.randint(1, 3) if random.random() < 0.6 else 0
        else:
            num_achievements = 0
        
        for i in range(num_achievements):
            badge_name, points = random.choice(achievement_types)
            days_ago = random.randint(1, 180)
            earned_at = datetime.now() - timedelta(days=days_ago)
            
            achievement = Achievement(
                student_id=student.student_id,
                badge_name=badge_name,
                points=points,
                description=f"Awarded for outstanding performance",
                earned_at=earned_at
            )
            db.session.add(achievement)
            achievements_count += 1
    
    print(f"✅ Created {achievements_count:,} achievements")


def create_predictions(students):
    """Create 500 ML predictions (1 per student)"""
    print("📊 Creating ML predictions...")
    
    predictions_count = 0
    
    for student_data in students:
        student = student_data['student']
        category = student_data['category']
        risk_level = student_data['risk_level']
        
        if category == 'high':
            predicted_grade = random.choice(['A+', 'A'])
            confidence = random.uniform(0.85, 0.95)
        elif category == 'average':
            predicted_grade = random.choice(['B+', 'B', 'C+'])
            confidence = random.uniform(0.70, 0.85)
        else:
            predicted_grade = random.choice(['C', 'D', 'F'])
            confidence = random.uniform(0.60, 0.75)
        
        prediction = Prediction(
            student_id=student.student_id,
            predicted_grade=predicted_grade,
            risk_level=risk_level,
            confidence_score=round(confidence, 4),
            factors={
                'attendance': 'excellent' if category == 'high' else 'good' if category == 'average' else 'poor',
                'marks_trend': 'excellent' if category == 'high' else 'good' if category == 'average' else 'poor',
                'assignment_completion': 'excellent' if category == 'high' else 'good' if category == 'average' else 'needs_improvement'
            }
        )
        db.session.add(prediction)
        predictions_count += 1
    
    print(f"✅ Created {predictions_count:,} ML predictions")


def create_career_suggestions(students):
    """Create ~2,000 career suggestions (500 students × 3-5 each)"""
    print("📊 Creating career suggestions...")
    
    careers = [
        ('Software Engineer', ['Mathematics', 'Science']),
        ('Doctor', ['Science', 'Additional Language']),
        ('Business Analyst', ['Mathematics', 'Social Science']),
        ('Teacher', ['English', 'Hindi']),
        ('Data Scientist', ['Mathematics', 'Science']),
        ('Civil Engineer', ['Mathematics', 'Geography']),
        ('Graphic Designer', ['Arts/Drawing', 'English']),
        ('Musician', ['Music', 'English']),
        ('Sports Professional', ['Sports', 'Science']),
        ('Historian', ['History', 'Social Science'])
    ]
    
    suggestions_count = 0
    
    for student_data in students:
        student = student_data['student']
        category = student_data['category']
        
        num_suggestions = random.randint(3, 5)
        
        for career, subjects in random.sample(careers, num_suggestions):
            if category == 'high':
                match_percentage = random.uniform(80, 95)
            elif category == 'average':
                match_percentage = random.uniform(60, 80)
            else:
                match_percentage = random.uniform(50, 70)
            
            suggestion = CareerSuggestion(
                student_id=student.student_id,
                career_path=career,
                match_percentage=round(match_percentage, 2),
                description=f"Based on your performance in {', '.join(subjects)}",
                required_skills=subjects
            )
            db.session.add(suggestion)
            suggestions_count += 1
    
    print(f"✅ Created {suggestions_count:,} career suggestions")



def create_recommendations(students, resources):
    """Create ~1,700 recommendations"""
    print("📊 Creating recommendations...")
    
    recommendations_count = 0
    
    for student_data in students:
        student = student_data['student']
        category = student_data['category']
        
        if category == 'at_risk':
            num_recs = random.randint(5, 8)
        elif category == 'average':
            num_recs = random.randint(2, 4)
        else:
            num_recs = random.randint(1, 3)
        
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
    
    print(f"✅ Created {recommendations_count:,} recommendations")


def create_resources():
    """Create 66 learning resources (11 subjects × 6 resources)"""
    print("📊 Creating learning resources...")
    
    resource_types = ['video', 'pdf', 'article', 'quiz', 'interactive', 'practice']
    difficulty_levels = ['beginner', 'intermediate', 'advanced']
    
    resources = []
    
    for subject in SUBJECTS:
        for i, res_type in enumerate(resource_types):
            resource = Resource(
                title=f"{subject} - {res_type.title()} {i+1}",
                subject=subject,
                resource_type=res_type,
                link=f"https://resources.school.edu/{subject.lower()}/{res_type}/{i+1}",
                description=f"Comprehensive {res_type} resource for {subject}",
                difficulty=difficulty_levels[i % 3]
            )
            db.session.add(resource)
            resources.append(resource)
    
    db.session.flush()
    print(f"✅ Created {len(resources)} learning resources")
    return resources


def seed_all_data():
    """Seed all data into the database"""
    print("\n" + "="*60)
    print("COMPREHENSIVE SCHOOL DATABASE POPULATION")
    print("1,016 USERS & 100,000+ RECORDS")
    print("="*60 + "\n")
    
    # Phase 1: Create users
    print("PHASE 1: CREATING 1,016 USERS")
    print("-" * 60)
    admin = create_admin()
    teachers = create_teachers()
    students = create_students_and_parents()
    
    print("\nCommitting users to database...")
    db.session.commit()
    print("✅ All users created\n")
    
    # Phase 2: Create records
    print("PHASE 2: CREATING 100,000+ RECORDS")
    print("-" * 60)
    create_attendance(students, teachers)
    create_marks(students)
    create_assignments(students)
    resources = create_resources()
    create_alerts(students)
    create_achievements(students)
    create_predictions(students)
    create_career_suggestions(students)
    create_recommendations(students, resources)
    
    print("\nCommitting all data to database...")
    db.session.commit()
    
    # Phase 3: Verification
    print("\n" + "="*60)
    print("DATABASE POPULATION COMPLETE!")
    print("="*60)
    
    # Count everything
    admin_count = User.query.filter_by(role='admin').count()
    teacher_count = User.query.filter_by(role='teacher').count()
    student_count = User.query.filter_by(role='student').count()
    parent_count = User.query.filter_by(role='parent').count()
    attendance_count = Attendance.query.count()
    marks_count = Marks.query.count()
    assignment_count = Assignment.query.count()
    alert_count = Alert.query.count()
    achievement_count = Achievement.query.count()
    prediction_count = Prediction.query.count()
    career_count = CareerSuggestion.query.count()
    recommendation_count = Recommendation.query.count()
    resource_count = Resource.query.count()
    
    print(f"\n📊 USERS (Total: {admin_count + teacher_count + student_count + parent_count})")
    print(f"   ├─ Admins: {admin_count}")
    print(f"   ├─ Teachers: {teacher_count}")
    print(f"   ├─ Students: {student_count}")
    print(f"   └─ Parents: {parent_count}")
    
    print(f"\n📊 STUDENTS BY CLASS:")
    for class_num in CLASSES:
        for section in SECTIONS:
            count = Student.query.filter_by(class_name=class_num, section=section).count()
            boys = Student.query.filter_by(class_name=class_num, section=section, gender='Male').count()
            girls = Student.query.filter_by(class_name=class_num, section=section, gender='Female').count()
            print(f"   Class {class_num}{section}: {count} students ({boys} boys, {girls} girls)")
    
    total_records = (attendance_count + marks_count + assignment_count + alert_count + 
                    achievement_count + prediction_count + career_count + recommendation_count + resource_count)
    
    print(f"\n📊 RECORDS (Total: {total_records:,})")
    print(f"   ├─ Attendance: {attendance_count:,}")
    print(f"   ├─ Marks: {marks_count:,}")
    print(f"   ├─ Assignments: {assignment_count:,}")
    print(f"   ├─ Alerts: {alert_count:,}")
    print(f"   ├─ Achievements: {achievement_count:,}")
    print(f"   ├─ Predictions: {prediction_count:,}")
    print(f"   ├─ Career Suggestions: {career_count:,}")
    print(f"   ├─ Recommendations: {recommendation_count:,}")
    print(f"   └─ Resources: {resource_count:,}")
    
    print(f"\n🔑 LOGIN CREDENTIALS:")
    print(f"   Admin: admin@school.edu / Admin@123")
    print(f"   Teachers: [firstname].[lastname]@school.com / Teacher@123")
    print(f"   Students: [firstname].[lastname][number]@gmail.com / Student@123")
    print(f"   Parents: parent.[lastname][number]@gmail.com / Parent@123")
    
    print(f"\n✅ Database successfully populated with 1,016 users and {total_records:,} records!")
    print("="*60 + "\n")


def main():
    """Main seeding function for CLI usage"""
    app = create_app()
    
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        print("Creating fresh tables...")
        db.create_all()
        print("✅ Database schema created\n")
        
        seed_all_data()


if __name__ == '__main__':
    main()
