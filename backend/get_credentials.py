"""
Script to extract all user credentials from the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, Student, Teacher

def get_all_credentials():
    """Extract all user credentials"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*80)
        print("STUDENT ACADEMIC SYSTEM - ALL LOGIN CREDENTIALS")
        print("="*80 + "\n")
        
        # Admin
        print("ADMIN ACCOUNT")
        print("-" * 80)
        admin = User.query.filter_by(role='admin').first()
        if admin:
            print(f"Email: {admin.email}")
            print(f"Password: Admin@123")
            print(f"Name: {admin.name}\n")
        
        # Teachers
        print("\nTEACHERS (11 total)")
        print("-" * 80)
        teachers = User.query.filter_by(role='teacher').all()
        print(f"\nCLASS TEACHERS (see only their 20 assigned students):")
        for user in teachers:
            teacher = Teacher.query.filter_by(user_id=user.user_id).first()
            if teacher and teacher.is_class_teacher:
                print(f"  • {user.name}")
                print(f"    Email: {user.email}")
                print(f"    Password: Teacher@123")
                print(f"    Subject: {teacher.subject}")
                print(f"    Assigned Class: {teacher.assigned_class}{teacher.assigned_section}")
                print()
        
        print(f"\nSUBJECT TEACHERS (see all 60 students):")
        for user in teachers:
            teacher = Teacher.query.filter_by(user_id=user.user_id).first()
            if teacher and not teacher.is_class_teacher:
                print(f"  • {user.name}")
                print(f"    Email: {user.email}")
                print(f"    Password: Teacher@123")
                print(f"    Subject: {teacher.subject}")
                print()
        
        # Parents and Students
        print("\nPARENTS & STUDENTS (60 pairs)")
        print("-" * 80)
        print("Format: Parent Email → Student Email (same last name)\n")
        
        students = Student.query.order_by(Student.class_name, Student.section, Student.roll_number).all()
        
        current_class = None
        for student in students:
            student_user = User.query.get(student.user_id)
            parent_user = User.query.get(student.parent_id)
            
            # Print class header
            if current_class != f"{student.class_name}{student.section}":
                current_class = f"{student.class_name}{student.section}"
                print(f"\n--- CLASS {current_class} (20 students) ---")
            
            print(f"  {student.roll_number}. Parent: {parent_user.email} → Student: {student_user.email}")
            print(f"      Parent Name: {parent_user.name} | Student Name: {student_user.name}")
        
        print("\n" + "="*80)
        print("ALL PASSWORDS:")
        print("  • Admin: Admin@123")
        print("  • Teachers: Teacher@123")
        print("  • Parents: Parent@123")
        print("  • Students: Student@123")
        print("="*80 + "\n")

if __name__ == "__main__":
    get_all_credentials()
