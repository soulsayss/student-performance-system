"""
CSV Import Utilities for Student Academic System
Handles bulk data import from CSV files with validation
"""

import csv
import io
from datetime import datetime
from werkzeug.security import generate_password_hash
from models import db, User, Student, Teacher, Marks, Attendance
from utils.validators import validate_email


class CSVImportError(Exception):
    """Custom exception for CSV import errors"""
    pass


def validate_csv_headers(headers, expected_headers):
    """Validate that CSV has correct headers (case-insensitive and flexible)"""
    headers = [h.strip().lower().replace(' ', '_') for h in headers]
    expected = [h.lower() for h in expected_headers]
    
    # Check if all required headers are present
    missing_headers = [h for h in expected if h not in headers]
    
    if missing_headers:
        raise CSVImportError(
            f"Missing required CSV headers: {', '.join(missing_headers)}. "
            f"Expected headers: {', '.join(expected_headers)}. "
            f"Got headers: {', '.join(headers)}"
        )
    
    return headers  # Return normalized headers


def import_students_from_csv(file_content, clear_existing=False):
    """
    Import students from CSV file
    Expected format: name,email,password,roll_number,class,section
    Optional fields: gender, date_of_birth, performance_level, parent_contact
    """
    results = {
        'success': True,
        'imported_count': 0,
        'errors': [],
        'skipped': []
    }
    
    try:
        # Handle UTF-8 BOM if present
        if file_content.startswith(b'\xef\xbb\xbf'):
            file_content = file_content[3:]
        
        # Parse CSV
        csv_file = io.StringIO(file_content.decode('utf-8'))
        reader = csv.DictReader(csv_file)
        
        # Normalize headers (lowercase, replace spaces with underscores)
        if reader.fieldnames:
            normalized_fieldnames = [h.strip().lower().replace(' ', '_') for h in reader.fieldnames]
            reader.fieldnames = normalized_fieldnames
        
        # Validate required headers
        required_headers = ['name', 'email', 'password', 'roll_number', 'class', 'section']
        validate_csv_headers(reader.fieldnames, required_headers)
        
        # Clear existing data if requested
        if clear_existing:
            Student.query.delete()
            User.query.filter_by(role='student').delete()
            db.session.commit()
        
        # Process each row
        row_number = 1
        for row in reader:
            row_number += 1
            try:
                # Validate required fields
                name = row.get('name', '').strip()
                email = row.get('email', '').strip().lower()
                password = row.get('password', '').strip()
                roll_number = row.get('roll_number', '').strip()
                class_name = row.get('class', '').strip()
                section = row.get('section', '').strip()
                
                # Optional fields
                gender = row.get('gender', '').strip() if 'gender' in row else None
                dob_str = row.get('date_of_birth', '').strip() if 'date_of_birth' in row else None
                
                if not all([name, email, password, roll_number, class_name, section]):
                    results['errors'].append(f"Row {row_number}: Missing required fields")
                    continue
                
                # Validate email format
                if not validate_email(email):
                    results['errors'].append(f"Row {row_number}: Invalid email format: {email}")
                    continue
                
                # Check for duplicate email
                if User.query.filter_by(email=email).first():
                    results['skipped'].append(f"Row {row_number}: Email already exists: {email}")
                    continue
                
                # Check for duplicate roll number
                if Student.query.filter_by(roll_number=roll_number).first():
                    results['skipped'].append(f"Row {row_number}: Roll number already exists: {roll_number}")
                    continue
                
                # Parse date of birth if provided
                dob = None
                if dob_str:
                    # Try multiple date formats
                    date_formats = [
                        '%d-%m-%Y',    # DD-MM-YYYY (13-08-2013) - Indian format
                        '%Y-%m-%d',    # YYYY-MM-DD (2013-08-13) - ISO format
                        '%m/%d/%Y',    # MM/DD/YYYY (08/13/2013) - US format
                        '%d/%m/%Y',    # DD/MM/YYYY (13/08/2013) - European format
                        '%d.%m.%Y',    # DD.MM.YYYY (13.08.2013) - German format
                        '%Y/%m/%d',    # YYYY/MM/DD (2013/08/13)
                    ]
                    
                    parsed = False
                    for date_format in date_formats:
                        try:
                            dob = datetime.strptime(dob_str, date_format).date()
                            parsed = True
                            break
                        except ValueError:
                            continue
                    
                    if not parsed:
                        # Skip this row but don't fail entire import
                        results['errors'].append(f"Row {row_number}: Invalid date format '{dob_str}'. Supported formats: DD-MM-YYYY, YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY")
                        continue
                
                # Create user
                user = User(
                    name=name,
                    email=email,
                    password_hash=generate_password_hash(password),
                    role='student',
                    is_active=True
                )
                db.session.add(user)
                db.session.flush()
                
                # Create student
                student = Student(
                    user_id=user.user_id,
                    roll_number=roll_number,
                    class_name=class_name,
                    section=section,
                    dob=dob,
                    gender=gender
                )
                db.session.add(student)
                
                results['imported_count'] += 1
                
            except Exception as e:
                results['errors'].append(f"Row {row_number}: {str(e)}")
                db.session.rollback()
                continue
        
        # Commit all changes
        db.session.commit()
        
    except CSVImportError as e:
        results['success'] = False
        results['errors'].append(str(e))
    except Exception as e:
        results['success'] = False
        results['errors'].append(f"Failed to parse CSV: {str(e)}")
        db.session.rollback()
    
    return results


def import_teachers_from_csv(file_content, clear_existing=False):
    """
    Import teachers from CSV file
    Expected format: name,email,password,employee_id,subject,department
    Optional fields: phone, experience, class_assigned
    """
    results = {
        'success': True,
        'imported_count': 0,
        'errors': [],
        'skipped': []
    }
    
    try:
        # Handle UTF-8 BOM if present
        if file_content.startswith(b'\xef\xbb\xbf'):
            file_content = file_content[3:]
        
        # Parse CSV
        csv_file = io.StringIO(file_content.decode('utf-8'))
        reader = csv.DictReader(csv_file)
        
        # Normalize headers (lowercase, replace spaces with underscores, handle variations)
        if reader.fieldnames:
            normalized_fieldnames = []
            for h in reader.fieldnames:
                # Normalize: lowercase, replace spaces/special chars with underscore
                normalized = h.strip().lower().replace(' ', '_').replace('(', '').replace(')', '')
                # Handle common variations
                if normalized == 'employee' or normalized == 'emp_id' or normalized == 'employee_no':
                    normalized = 'employee_id'
                elif normalized == 'class_assigned' or normalized == 'classes' or normalized == 'class':
                    normalized = 'department'  # Map to department field
                elif normalized == 'experience_years' or normalized == 'experience':
                    normalized = 'experience'
                normalized_fieldnames.append(normalized)
            reader.fieldnames = normalized_fieldnames
        
        # Validate required headers
        required_headers = ['name', 'email', 'password', 'employee_id', 'subject']
        validate_csv_headers(reader.fieldnames, required_headers)
        
        # Clear existing data if requested
        if clear_existing:
            Teacher.query.delete()
            User.query.filter_by(role='teacher').delete()
            db.session.commit()
        
        # Process each row
        row_number = 1
        for row in reader:
            row_number += 1
            try:
                # Validate required fields
                name = row.get('name', '').strip()
                email = row.get('email', '').strip().lower()
                password = row.get('password', '').strip()
                employee_id = row.get('employee_id', '').strip()
                subject = row.get('subject', '').strip()
                
                # Optional fields
                department = row.get('department', '').strip() if 'department' in row else None
                phone = row.get('phone', '').strip() if 'phone' in row else None
                experience = row.get('experience', '').strip() if 'experience' in row else None
                
                if not all([name, email, password, employee_id, subject]):
                    results['errors'].append(f"Row {row_number}: Missing required fields (name, email, password, employee_id, subject)")
                    continue
                
                # Validate email format
                if not validate_email(email):
                    results['errors'].append(f"Row {row_number}: Invalid email format: {email}")
                    continue
                
                # Check for duplicate email
                if User.query.filter_by(email=email).first():
                    results['skipped'].append(f"Row {row_number}: Email already exists: {email}")
                    continue
                
                # Check for duplicate employee ID
                if Teacher.query.filter_by(employee_id=employee_id).first():
                    results['skipped'].append(f"Row {row_number}: Employee ID already exists: {employee_id}")
                    continue
                
                # Create user
                user = User(
                    name=name,
                    email=email,
                    password_hash=generate_password_hash(password),
                    role='teacher',
                    is_active=True
                )
                db.session.add(user)
                db.session.flush()
                
                # Create teacher
                teacher = Teacher(
                    user_id=user.user_id,
                    employee_id=employee_id,
                    subject=subject,
                    department=department if department else None
                )
                db.session.add(teacher)
                
                results['imported_count'] += 1
                
            except Exception as e:
                results['errors'].append(f"Row {row_number}: {str(e)}")
                db.session.rollback()
                continue
        
        # Commit all changes
        db.session.commit()
        
    except CSVImportError as e:
        results['success'] = False
        results['errors'].append(str(e))
    except Exception as e:
        results['success'] = False
        results['errors'].append(f"Failed to parse CSV: {str(e)}")
        db.session.rollback()
    
    return results


def import_parents_from_csv(file_content, clear_existing=False):
    """
    Import parents from CSV file
    Expected format: Name, Email, Password, Phone, Student Roll Number, Relation, Occupation
    """
    results = {
        'success': True,
        'imported_count': 0,
        'errors': [],
        'skipped': []
    }
    
    try:
        # Handle UTF-8 BOM if present
        content = file_content.decode('utf-8-sig')
        
        # Parse CSV
        csv_file = io.StringIO(content)
        reader = csv.DictReader(csv_file)
        
        # Normalize headers (lowercase and replace spaces with underscores)
        if reader.fieldnames:
            normalized_headers = [h.strip().lower().replace(' ', '_') for h in reader.fieldnames]
            reader.fieldnames = normalized_headers
        
        # Clear existing data if requested
        if clear_existing:
            User.query.filter_by(role='parent').delete()
            db.session.commit()
        
        # Process each row
        row_number = 1
        for row in reader:
            row_number += 1
            try:
                # Validate required fields using .get() for safer access
                name = row.get('name', '').strip()
                email = row.get('email', '').strip().lower()
                password = row.get('password', '').strip()
                phone = row.get('phone', '').strip()
                student_roll_number = row.get('student_roll_number', '').strip()
                relation = row.get('relation', '').strip()
                occupation = row.get('occupation', '').strip()  # Optional field
                
                if not all([name, email, password, student_roll_number]):
                    results['errors'].append(f"Row {row_number}: Missing required fields")
                    continue
                
                # Validate email format
                if not validate_email(email):
                    results['errors'].append(f"Row {row_number}: Invalid email format: {email}")
                    continue
                
                # Check if student exists
                student = Student.query.filter_by(roll_number=student_roll_number).first()
                if not student:
                    results['errors'].append(f"Row {row_number}: Student with roll number {student_roll_number} not found")
                    continue
                
                # Check for duplicate email
                if User.query.filter_by(email=email).first():
                    results['skipped'].append(f"Row {row_number}: Email already exists: {email}")
                    continue
                
                # Create user (parent)
                user = User(
                    name=name,
                    email=email,
                    password_hash=generate_password_hash(password),
                    role='parent',
                    is_active=True
                )
                db.session.add(user)
                db.session.flush()
                
                # Link parent to student
                if not student.parent_id:
                    student.parent_id = user.user_id
                
                results['imported_count'] += 1
                
            except Exception as e:
                results['errors'].append(f"Row {row_number}: {str(e)}")
                db.session.rollback()
                continue
        
        # Commit all changes
        db.session.commit()
        
    except CSVImportError as e:
        results['success'] = False
        results['errors'].append(str(e))
    except Exception as e:
        results['success'] = False
        results['errors'].append(f"Failed to parse CSV: {str(e)}")
        db.session.rollback()
    
    return results


def import_marks_from_csv(file_content, clear_existing=False):
    """
    Import marks from CSV file
    Expected format: roll_number,subject,exam_type,score,max_score,exam_date
    """
    results = {
        'success': True,
        'imported_count': 0,
        'errors': [],
        'skipped': []
    }
    
    try:
        # Handle UTF-8 BOM if present
        content = file_content.decode('utf-8-sig')
        
        # Parse CSV
        csv_file = io.StringIO(content)
        reader = csv.DictReader(csv_file)
        
        # Normalize headers (lowercase and replace spaces with underscores)
        if reader.fieldnames:
            normalized_headers = [h.strip().lower().replace(' ', '_') for h in reader.fieldnames]
            reader.fieldnames = normalized_headers
        
        # Clear existing data if requested
        if clear_existing:
            Marks.query.delete()
            db.session.commit()
        
        # Exam type mapping for flexibility
        exam_type_mapping = {
            'quiz': 'quiz',
            'quizzes': 'quiz',
            'test': 'quiz',
            'unit_test': 'quiz',
            'unit test': 'quiz',
            'unit_test_1': 'quiz',
            'unit test 1': 'quiz',
            'unit_test_2': 'quiz',
            'unit test 2': 'quiz',
            'unit_test_3': 'quiz',
            'unit test 3': 'quiz',
            'class_test': 'quiz',
            'class test': 'quiz',
            'weekly_test': 'quiz',
            'weekly test': 'quiz',
            'midterm': 'midterm',
            'mid-term': 'midterm',
            'mid_term': 'midterm',
            'mid term': 'midterm',
            'mid': 'midterm',
            'half_yearly': 'midterm',
            'half yearly': 'midterm',
            'half-yearly': 'midterm',
            'semester': 'midterm',
            'term': 'midterm',
            'final': 'final',
            'finals': 'final',
            'final_exam': 'final',
            'final exam': 'final',
            'annual': 'final',
            'yearly': 'final',
            'annual_exam': 'final',
            'annual exam': 'final',
            'assignment': 'assignment',
            'assignments': 'assignment',
            'homework': 'assignment',
            'project': 'assignment',
            'practical': 'assignment',
            'lab': 'assignment',
            'internal': 'assignment'
        }
        
        # Process each row
        row_number = 1
        for row in reader:
            row_number += 1
            try:
                # Validate required fields using .get() for safer access
                roll_number = row.get('roll_number', '').strip()
                subject = row.get('subject', '').strip()
                exam_type_raw = row.get('exam_type', '').strip().lower()
                score = row.get('score', '').strip()
                max_score = row.get('max_score', '').strip()
                exam_date_str = row.get('exam_date', '').strip()
                
                if not all([roll_number, subject, exam_type_raw, score, max_score, exam_date_str]):
                    results['errors'].append(f"Row {row_number}: Missing required fields")
                    continue
                
                # Find student
                student = Student.query.filter_by(roll_number=roll_number).first()
                if not student:
                    results['errors'].append(f"Row {row_number}: Student with roll number {roll_number} not found")
                    continue
                
                # Map exam type to valid value
                exam_type = exam_type_mapping.get(exam_type_raw)
                if not exam_type:
                    valid_types = list(set(exam_type_mapping.values()))
                    results['errors'].append(f"Row {row_number}: Invalid exam type '{exam_type_raw}'. Must be one of: {', '.join(valid_types)}")
                    continue
                
                # Parse numeric values
                try:
                    score_val = float(score)
                    max_score_val = float(max_score)
                except ValueError:
                    results['errors'].append(f"Row {row_number}: Score and max_score must be numeric")
                    continue
                
                # Validate score range
                if score_val < 0 or score_val > max_score_val:
                    results['errors'].append(f"Row {row_number}: Score must be between 0 and max_score")
                    continue
                
                # Parse date with multiple formats
                exam_date = None
                date_formats = ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y', '%d.%m.%Y', '%Y/%m/%d']
                for fmt in date_formats:
                    try:
                        exam_date = datetime.strptime(exam_date_str, fmt).date()
                        break
                    except ValueError:
                        continue
                
                if not exam_date:
                    results['errors'].append(f"Row {row_number}: Invalid date format '{exam_date_str}'. Use YYYY-MM-DD, DD-MM-YYYY, or MM/DD/YYYY")
                    continue
                
                # Create marks entry
                marks = Marks(
                    student_id=student.student_id,
                    subject=subject,
                    exam_type=exam_type,
                    score=score_val,
                    max_score=max_score_val,
                    exam_date=exam_date
                )
                db.session.add(marks)
                
                results['imported_count'] += 1
                
            except Exception as e:
                results['errors'].append(f"Row {row_number}: {str(e)}")
                db.session.rollback()
                continue
        
        # Commit all changes
        db.session.commit()
        
    except CSVImportError as e:
        results['success'] = False
        results['errors'].append(str(e))
    except Exception as e:
        results['success'] = False
        results['errors'].append(f"Failed to parse CSV: {str(e)}")
        db.session.rollback()
    
    return results


def import_attendance_from_csv(file_content, clear_existing=False):
    """
    Import attendance from CSV file
    Expected format: roll_number,date,status
    """
    results = {
        'success': True,
        'imported_count': 0,
        'errors': [],
        'skipped': []
    }
    
    try:
        # Parse CSV
        csv_file = io.StringIO(file_content.decode('utf-8'))
        reader = csv.DictReader(csv_file)
        
        # Validate headers
        expected_headers = ['roll_number', 'date', 'status']
        if reader.fieldnames:
            validate_csv_headers(reader.fieldnames, expected_headers)
        
        # Clear existing data if requested
        if clear_existing:
            Attendance.query.delete()
            db.session.commit()
        
        # Process each row
        row_number = 1
        for row in reader:
            row_number += 1
            try:
                # Validate required fields
                roll_number = row['roll_number'].strip()
                date_str = row['date'].strip()
                status = row['status'].strip().lower()
                
                if not all([roll_number, date_str, status]):
                    results['errors'].append(f"Row {row_number}: Missing required fields")
                    continue
                
                # Find student
                student = Student.query.filter_by(roll_number=roll_number).first()
                if not student:
                    results['errors'].append(f"Row {row_number}: Student with roll number {roll_number} not found")
                    continue
                
                # Validate status
                valid_statuses = ['present', 'absent', 'late']
                if status not in valid_statuses:
                    results['errors'].append(f"Row {row_number}: Invalid status. Must be one of: {', '.join(valid_statuses)}")
                    continue
                
                # Parse date
                try:
                    attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    results['errors'].append(f"Row {row_number}: Invalid date format. Use YYYY-MM-DD")
                    continue
                
                # Check for duplicate
                existing = Attendance.query.filter_by(
                    student_id=student.student_id,
                    date=attendance_date
                ).first()
                
                if existing:
                    results['skipped'].append(f"Row {row_number}: Attendance already exists for {roll_number} on {date_str}")
                    continue
                
                # Create attendance entry
                attendance = Attendance(
                    student_id=student.student_id,
                    date=attendance_date,
                    status=status
                )
                db.session.add(attendance)
                
                results['imported_count'] += 1
                
            except Exception as e:
                results['errors'].append(f"Row {row_number}: {str(e)}")
                db.session.rollback()
                continue
        
        # Commit all changes
        db.session.commit()
        
    except CSVImportError as e:
        results['success'] = False
        results['errors'].append(str(e))
    except Exception as e:
        results['success'] = False
        results['errors'].append(f"Failed to parse CSV: {str(e)}")
        db.session.rollback()
    
    return results


def generate_csv_template(template_type):
    """
    Generate CSV template with correct headers
    """
    templates = {
        'students': 'name,email,password,roll_number,class,section\n'
                   'John Doe,john@example.com,password123,S001,10,A\n'
                   'Jane Smith,jane@example.com,password123,S002,10,A\n',
        
        'teachers': 'name,email,password,employee_id,subject,department\n'
                   'Dr. Smith,smith@school.com,teacher123,T001,Mathematics,Science\n'
                   'Prof. Johnson,johnson@school.com,teacher123,T002,Physics,Science\n',
        
        'parents': 'name,email,password,phone,student_roll_number,relation\n'
                  'Parent One,parent1@email.com,parent123,1234567890,S001,Father\n'
                  'Parent Two,parent2@email.com,parent123,0987654321,S002,Mother\n',
        
        'marks': 'roll_number,subject,exam_type,score,max_score,exam_date\n'
                'S001,Mathematics,midterm,85,100,2024-01-15\n'
                'S001,Physics,midterm,78,100,2024-01-16\n',
        
        'attendance': 'roll_number,date,status\n'
                     'S001,2024-01-15,present\n'
                     'S001,2024-01-16,present\n'
    }
    
    return templates.get(template_type, '')
