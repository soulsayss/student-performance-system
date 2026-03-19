from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Student, Teacher, Attendance, Marks, Alert, Prediction
from datetime import datetime, timedelta
from sqlalchemy import func, desc, and_
from sqlalchemy.orm import joinedload
from utils.helpers import detect_at_risk_students, generate_alert_for_student
import csv
import io

teacher_bp = Blueprint('teacher', __name__)

def get_current_teacher():
    """Helper to get current teacher from JWT"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or user.role != 'teacher':
        return None
    
    # Return the user object, not just teacher_profile
    return user

@teacher_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """
    GET /api/teacher/dashboard?days=30
    Returns: class overview, total students, at-risk count
    - Class teachers: ONLY students in their assigned class (20 students)
    - Subject teachers: ALL students across all classes (60 students)
    OPTIMIZED: Uses query parameters for date range
    Query params:
    - days: Number of days to look back (default: 30, max: 180)
    """
    try:
        user = get_current_teacher()
        
        if not user or not user.teacher_profile:
            return jsonify({
                'success': False,
                'message': 'Teacher profile not found'
            }), 404
        
        teacher = user.teacher_profile
        
        # Get days parameter, default to 30
        days = request.args.get('days', 30, type=int)
        days = min(max(days, 7), 180)  # Min 7, max 180
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Determine teacher type and filter students accordingly
        if teacher.is_class_teacher and teacher.assigned_class and teacher.assigned_section:
            # Class teacher: ONLY students in assigned class
            students_query = Student.query.filter_by(
                class_name=teacher.assigned_class,
                section=teacher.assigned_section
            )
            teacher_type = 'class_teacher'
        else:
            # Subject teacher: ALL students
            students_query = Student.query
            teacher_type = 'subject_teacher'
        
        students = students_query.all()
        total_students = len(students)
        student_ids = [s.student_id for s in students]
        
        # OPTIMIZATION: Calculate at-risk using database aggregation
        at_risk_count = 0
        
        if student_ids:
            # Count students with low attendance using subquery
            low_attendance_subquery = db.session.query(
                Attendance.student_id,
                func.count(Attendance.attendance_id).label('total'),
                func.sum(func.case((Attendance.status == 'present', 1), else_=0)).label('present')
            ).filter(
                Attendance.student_id.in_(student_ids),
                Attendance.date >= cutoff_date.date()
            ).group_by(Attendance.student_id).subquery()
            
            low_attendance_students = db.session.query(
                low_attendance_subquery.c.student_id
            ).filter(
                (low_attendance_subquery.c.present * 100.0 / low_attendance_subquery.c.total) < 75
            ).all()
            
            # Count students with low marks using subquery
            low_marks_subquery = db.session.query(
                Marks.student_id,
                func.avg(Marks.score / Marks.max_score * 100).label('avg_percentage')
            ).filter(
                Marks.student_id.in_(student_ids),
                Marks.max_score > 0
            ).group_by(Marks.student_id).subquery()
            
            low_marks_students = db.session.query(
                low_marks_subquery.c.student_id
            ).filter(
                low_marks_subquery.c.avg_percentage < 50
            ).all()
            
            # Combine unique at-risk students
            at_risk_ids = set([s[0] for s in low_attendance_students] + [s[0] for s in low_marks_students])
            at_risk_count = len(at_risk_ids)
        
        # Get today's attendance stats
        today = datetime.utcnow().date()
        present_today = 0
        if student_ids:
            present_today = Attendance.query.filter(
                Attendance.date == today,
                Attendance.student_id.in_(student_ids),
                Attendance.status == 'present'
            ).count()
        
        # Get class average using aggregation
        class_average = 0
        if student_ids:
            avg_result = db.session.query(
                func.avg(Marks.score / Marks.max_score * 100)
            ).filter(
                Marks.student_id.in_(student_ids),
                Marks.max_score > 0
            ).scalar()
            class_average = round(avg_result, 2) if avg_result else 0
        
        return jsonify({
            'success': True,
            'dashboard': {
                'total_students': total_students,
                'at_risk_students': at_risk_count,
                'present_today': present_today,
                'class_average': class_average,
                'teacher_type': teacher_type,
                'days_range': days,
                'teacher_info': {
                    'name': user.name,
                    'subject': teacher.subject,
                    'department': teacher.department,
                    'employee_id': teacher.employee_id,
                    'is_class_teacher': teacher.is_class_teacher,
                    'assigned_class': teacher.assigned_class,
                    'assigned_section': teacher.assigned_section
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch dashboard',
            'error': str(e)
        }), 500

@teacher_bp.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    """
    GET /api/teacher/students?days=30
    Returns: students based on teacher type
    - Class teachers: ONLY students in their assigned class (20 students)
    - Subject teachers: ALL students across all classes (60 students)
    OPTIMIZED: Uses query parameters for date range to prevent memory overflow
    Query params:
    - days: Number of days to look back for attendance (default: 30, max: 180)
    """
    try:
        user = get_current_teacher()
        
        if not user or not user.teacher_profile:
            return jsonify({
                'success': False,
                'message': 'Teacher profile not found'
            }), 404
        
        teacher = user.teacher_profile
        
        # Get days parameter from query string, default to 30
        days = request.args.get('days', 30, type=int)
        # Limit maximum to prevent memory issues
        days = min(max(days, 7), 180)  # Min 7 days, max 180 days
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # OPTIMIZATION: Load only user data with students, no heavy relationships
        students_query = Student.query.options(joinedload(Student.user))
        
        # Filter based on teacher type
        if teacher.is_class_teacher and teacher.assigned_class and teacher.assigned_section:
            # Class teacher: show ONLY students in assigned class
            students_query = students_query.filter_by(
                class_name=teacher.assigned_class,
                section=teacher.assigned_section
            )
            teacher_type = 'class_teacher'
        else:
            # Subject teacher: show ALL students
            teacher_type = 'subject_teacher'
        
        students = students_query.all()
        
        students_data = []
        
        for student in students:
            student_dict = student.to_dict()
            student_dict['name'] = student.user.name
            student_dict['email'] = student.user.email
            
            # OPTIMIZATION: Query only recent attendance with date filter
            attendance_records = Attendance.query.filter(
                Attendance.student_id == student.student_id,
                Attendance.date >= cutoff_date.date()
            ).all()
            
            if attendance_records:
                present = sum(1 for a in attendance_records if a.status == 'present')
                student_dict['attendance_percentage'] = round((present / len(attendance_records)) * 100, 2)
            else:
                student_dict['attendance_percentage'] = 0
            
            # OPTIMIZATION: Calculate average from database aggregation instead of loading all marks
            avg_result = db.session.query(
                func.avg(Marks.score / Marks.max_score * 100)
            ).filter(
                Marks.student_id == student.student_id,
                Marks.max_score > 0
            ).scalar()
            
            student_dict['average_marks'] = round(avg_result, 2) if avg_result else 0
            
            # Get latest prediction without loading all predictions
            prediction = Prediction.query.filter_by(
                student_id=student.student_id
            ).order_by(desc(Prediction.created_at)).first()
            
            student_dict['risk_level'] = prediction.risk_level if prediction else 'unknown'
            
            students_data.append(student_dict)
        
        return jsonify({
            'success': True,
            'students': students_data,
            'total': len(students_data),
            'teacher_type': teacher_type,
            'days_range': days
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch students',
            'error': str(e)
        }), 500

@teacher_bp.route('/attendance', methods=['POST'])
@jwt_required()
def mark_attendance():
    """
    POST /api/teacher/attendance
    Accept: student_id, date, status OR CSV file
    """
    try:
        user = get_current_teacher()
        
        if not user or not user.teacher_profile:
            return jsonify({
                'success': False,
                'message': 'Teacher profile not found'
            }), 404
        
        teacher = user.teacher_profile
        
        # Check if CSV file is uploaded
        if 'file' in request.files:
            file = request.files['file']
            
            if not file.filename.endswith('.csv'):
                return jsonify({
                    'success': False,
                    'message': 'Only CSV files are allowed'
                }), 400
            
            # Parse CSV
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)
            
            records_added = 0
            errors = []
            
            for row in csv_reader:
                try:
                    student_id = int(row.get('student_id'))
                    date_str = row.get('date')
                    status = row.get('status', 'present').lower()
                    
                    # Validate student exists
                    student = Student.query.get(student_id)
                    if not student:
                        errors.append(f"Student ID {student_id} not found")
                        continue
                    
                    # Parse date
                    date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    
                    # Check if attendance already exists
                    existing = Attendance.query.filter_by(
                        student_id=student_id,
                        date=date
                    ).first()
                    
                    if existing:
                        existing.status = status
                        existing.marked_by = teacher.teacher_id
                    else:
                        attendance = Attendance(
                            student_id=student_id,
                            date=date,
                            status=status,
                            marked_by=teacher.teacher_id
                        )
                        db.session.add(attendance)
                    
                    records_added += 1
                
                except Exception as e:
                    errors.append(f"Row error: {str(e)}")
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Attendance marked for {records_added} records',
                'records_added': records_added,
                'errors': errors if errors else None
            }), 201
        
        # Single attendance record
        else:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'No data provided'
                }), 400
            
            student_id = data.get('student_id')
            date_str = data.get('date')
            status = data.get('status', 'present').lower()
            
            if not all([student_id, date_str, status]):
                return jsonify({
                    'success': False,
                    'message': 'student_id, date, and status are required'
                }), 400
            
            # Validate student
            student = Student.query.get(student_id)
            if not student:
                return jsonify({
                    'success': False,
                    'message': 'Student not found'
                }), 404
            
            # Parse date
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid date format. Use YYYY-MM-DD'
                }), 400
            
            # Validate status
            if status not in ['present', 'absent', 'late']:
                return jsonify({
                    'success': False,
                    'message': 'Status must be present, absent, or late'
                }), 400
            
            # Check if attendance already exists
            existing = Attendance.query.filter_by(
                student_id=student_id,
                date=date
            ).first()
            
            if existing:
                existing.status = status
                existing.marked_by = teacher.teacher_id
                message = 'Attendance updated successfully'
            else:
                attendance = Attendance(
                    student_id=student_id,
                    date=date,
                    status=status,
                    marked_by=teacher.teacher_id
                )
                db.session.add(attendance)
                message = 'Attendance marked successfully'
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': message
            }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to mark attendance',
            'error': str(e)
        }), 500

@teacher_bp.route('/marks', methods=['POST'])
@jwt_required()
def add_marks():
    """
    POST /api/teacher/marks
    Accept: student_id, subject, exam_type, score, max_score OR CSV file
    """
    try:
        user = get_current_teacher()
        
        if not user or not user.teacher_profile:
            return jsonify({
                'success': False,
                'message': 'Teacher profile not found'
            }), 404
        
        teacher = user.teacher_profile
        
        # Check if CSV file is uploaded
        if 'file' in request.files:
            file = request.files['file']
            
            if not file.filename.endswith('.csv'):
                return jsonify({
                    'success': False,
                    'message': 'Only CSV files are allowed'
                }), 400
            
            # Parse CSV
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)
            
            records_added = 0
            errors = []
            
            for row in csv_reader:
                try:
                    student_id = int(row.get('student_id'))
                    subject = row.get('subject')
                    exam_type = row.get('exam_type')
                    score = float(row.get('score'))
                    max_score = float(row.get('max_score', 100))
                    exam_date_str = row.get('exam_date')
                    
                    # Validate student
                    student = Student.query.get(student_id)
                    if not student:
                        errors.append(f"Student ID {student_id} not found")
                        continue
                    
                    # Parse exam date
                    exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date() if exam_date_str else datetime.utcnow().date()
                    
                    marks = Marks(
                        student_id=student_id,
                        subject=subject,
                        exam_type=exam_type,
                        score=score,
                        max_score=max_score,
                        exam_date=exam_date
                    )
                    db.session.add(marks)
                    records_added += 1
                
                except Exception as e:
                    errors.append(f"Row error: {str(e)}")
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Marks added for {records_added} records',
                'records_added': records_added,
                'errors': errors if errors else None
            }), 201
        
        # Single marks record
        else:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'No data provided'
                }), 400
            
            student_id = data.get('student_id')
            subject = data.get('subject')
            exam_type = data.get('exam_type')
            score = data.get('score')
            max_score = data.get('max_score', 100)
            exam_date_str = data.get('exam_date')
            
            if not all([student_id, subject, exam_type, score is not None]):
                return jsonify({
                    'success': False,
                    'message': 'student_id, subject, exam_type, and score are required'
                }), 400
            
            # Validate student
            student = Student.query.get(student_id)
            if not student:
                return jsonify({
                    'success': False,
                    'message': 'Student not found'
                }), 404
            
            # Parse exam date
            if exam_date_str:
                try:
                    exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({
                        'success': False,
                        'message': 'Invalid date format. Use YYYY-MM-DD'
                    }), 400
            else:
                exam_date = datetime.utcnow().date()
            
            marks = Marks(
                student_id=student_id,
                subject=subject,
                exam_type=exam_type,
                score=float(score),
                max_score=float(max_score),
                exam_date=exam_date
            )
            db.session.add(marks)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Marks added successfully',
                'marks': marks.to_dict()
            }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to add marks',
            'error': str(e)
        }), 500

@teacher_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    """
    GET /api/teacher/analytics
    Returns: class performance charts data
    """
    try:
        user = get_current_teacher()
        
        if not user or not user.teacher_profile:
            return jsonify({
                'success': False,
                'message': 'Teacher profile not found'
            }), 404
        
        # Get all students
        students = Student.query.all()
        
        # Subject-wise performance
        subjects = db.session.query(Marks.subject).distinct().all()
        subject_performance = []
        
        for (subject,) in subjects:
            marks = Marks.query.filter_by(subject=subject).all()
            if marks:
                avg = sum((m.score / m.max_score * 100) for m in marks if m.max_score > 0) / len(marks)
                subject_performance.append({
                    'subject': subject,
                    'average': round(avg, 2),
                    'total_exams': len(marks)
                })
        
        # Attendance trends (last 6 months)
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        attendance_records = Attendance.query.filter(
            Attendance.date >= six_months_ago.date()
        ).all()
        
        # Group by month
        monthly_attendance = {}
        for record in attendance_records:
            month = record.date.strftime('%Y-%m')
            if month not in monthly_attendance:
                monthly_attendance[month] = {'present': 0, 'absent': 0, 'late': 0, 'total': 0}
            monthly_attendance[month][record.status] += 1
            monthly_attendance[month]['total'] += 1
        
        attendance_trend = [
            {
                'month': month,
                'present': data['present'],
                'absent': data['absent'],
                'late': data['late'],
                'attendance_rate': round((data['present'] / data['total'] * 100), 2) if data['total'] > 0 else 0
            }
            for month, data in sorted(monthly_attendance.items())
        ]
        
        # Grade distribution
        all_marks = Marks.query.all()
        grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        
        for mark in all_marks:
            percentage = (mark.score / mark.max_score * 100) if mark.max_score > 0 else 0
            if percentage >= 90:
                grade_distribution['A'] += 1
            elif percentage >= 80:
                grade_distribution['B'] += 1
            elif percentage >= 70:
                grade_distribution['C'] += 1
            elif percentage >= 60:
                grade_distribution['D'] += 1
            else:
                grade_distribution['F'] += 1
        
        # Risk level distribution
        risk_distribution = {'low': 0, 'medium': 0, 'high': 0, 'unknown': 0}
        
        for student in students:
            prediction = Prediction.query.filter_by(
                student_id=student.student_id
            ).order_by(desc(Prediction.created_at)).first()
            
            if prediction:
                risk_distribution[prediction.risk_level] += 1
            else:
                risk_distribution['unknown'] += 1
        
        return jsonify({
            'success': True,
            'analytics': {
                'subject_performance': subject_performance,
                'attendance_trend': attendance_trend,
                'grade_distribution': grade_distribution,
                'risk_distribution': risk_distribution,
                'total_students': len(students)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch analytics',
            'error': str(e)
        }), 500

@teacher_bp.route('/at-risk-students', methods=['GET'])
@jwt_required()
def get_at_risk_students():
    """
    GET /api/teacher/at-risk-students
    Returns: flagged students (low attendance/performance)
    - Class teachers: ONLY at-risk students from their assigned class
    - Subject teachers: ALL at-risk students
    """
    try:
        user = get_current_teacher()
        
        if not user or not user.teacher_profile:
            return jsonify({
                'success': False,
                'message': 'Teacher profile not found'
            }), 404
        
        teacher = user.teacher_profile
        
        # Use helper function to detect at-risk students
        all_at_risk = detect_at_risk_students()
        
        # Filter by teacher type
        if teacher.is_class_teacher and teacher.assigned_class and teacher.assigned_section:
            # Class teacher: ONLY at-risk students from assigned class
            at_risk_students = [
                s for s in all_at_risk 
                if s.get('class_name') == teacher.assigned_class and s.get('section') == teacher.assigned_section
            ]
        else:
            # Subject teacher: ALL at-risk students
            at_risk_students = all_at_risk
        
        # Generate alerts for newly detected at-risk students
        for student_data in at_risk_students:
            # Check if alert already exists for this student today
            today = datetime.utcnow().date()
            existing_alert = Alert.query.filter(
                Alert.student_id == student_data['student_id'],
                func.date(Alert.created_at) == today
            ).first()
            
            if not existing_alert:
                # Create alert message
                message = f"Student flagged as at-risk. Factors: {', '.join(student_data['risk_factors'])}"
                severity = 'critical' if len(student_data['risk_factors']) >= 3 else 'warning'
                generate_alert_for_student(student_data['student_id'], message, severity)
        
        return jsonify({
            'success': True,
            'at_risk_students': at_risk_students,
            'total': len(at_risk_students)
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch at-risk students',
            'error': str(e)
        }), 500

@teacher_bp.route('/send-alert', methods=['POST'])
@jwt_required()
def send_alert():
    """
    POST /api/teacher/send-alert
    Accept: student_id, message, severity
    """
    try:
        user = get_current_teacher()
        
        if not user or not user.teacher_profile:
            return jsonify({
                'success': False,
                'message': 'Teacher profile not found'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        student_id = data.get('student_id')
        message = data.get('message')
        severity = data.get('severity', 'info').lower()
        
        if not all([student_id, message]):
            return jsonify({
                'success': False,
                'message': 'student_id and message are required'
            }), 400
        
        # Validate student
        student = Student.query.get(student_id)
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
        
        # Validate severity
        if severity not in ['info', 'warning', 'critical']:
            return jsonify({
                'success': False,
                'message': 'Severity must be info, warning, or critical'
            }), 400
        
        # Create alert
        alert = Alert(
            student_id=student_id,
            message=message,
            severity=severity,
            is_read=False
        )
        db.session.add(alert)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Alert sent successfully',
            'alert': alert.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to send alert',
            'error': str(e)
        }), 500
