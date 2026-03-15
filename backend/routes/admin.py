from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Student, Teacher, Attendance, Marks, Resource, Prediction, Alert
from utils.validators import validate_email, validate_password_strength, validate_role, validate_name, sanitize_input
from datetime import datetime, timedelta
from sqlalchemy import func, desc

admin_bp = Blueprint('admin', __name__)

def get_current_admin():
    """Helper to get current admin from JWT"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return None
    
    return user

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """
    GET /api/admin/users
    Returns: all users (paginated)
    Query params: page, per_page, role
    """
    try:
        admin = get_current_admin()
        
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        # Get pagination params
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        role_filter = request.args.get('role', None)
        
        # Build query
        query = User.query
        
        if role_filter:
            query = query.filter_by(role=role_filter)
        
        # Paginate
        pagination = query.order_by(User.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        users_data = []
        for user in pagination.items:
            user_dict = user.to_dict()
            
            # Add role-specific info
            if user.role == 'student' and user.student_profile:
                user_dict['student_info'] = user.student_profile.to_dict()
            elif user.role == 'teacher' and user.teacher_profile:
                user_dict['teacher_info'] = user.teacher_profile.to_dict()
            
            users_data.append(user_dict)
        
        return jsonify({
            'success': True,
            'users': users_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch users',
            'error': str(e)
        }), 500

@admin_bp.route('/user', methods=['POST'])
@jwt_required()
def create_user():
    """
    POST /api/admin/user
    Create new user (any role)
    """
    try:
        admin = get_current_admin()
        
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Extract and validate
        name = sanitize_input(data.get('name', ''), 100)
        email = sanitize_input(data.get('email', ''), 120).lower()
        password = data.get('password', '')
        role = sanitize_input(data.get('role', ''), 20).lower()
        
        # Validate
        is_valid, error = validate_name(name)
        if not is_valid:
            return jsonify({'success': False, 'message': error}), 400
        
        is_valid, error = validate_email(email)
        if not is_valid:
            return jsonify({'success': False, 'message': error}), 400
        
        is_valid, error = validate_password_strength(password)
        if not is_valid:
            return jsonify({'success': False, 'message': error}), 400
        
        is_valid, error = validate_role(role)
        if not is_valid:
            return jsonify({'success': False, 'message': error}), 400
        
        # Check if user exists
        existing = User.query.filter_by(email=email).first()
        if existing:
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 409
        
        # Create user
        new_user = User(
            name=name,
            email=email,
            role=role,
            is_active=data.get('is_active', True)
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.flush()
        
        # Create role-specific record
        if role == 'student':
            student = Student(
                user_id=new_user.user_id,
                roll_number=sanitize_input(data.get('roll_number', ''), 50),
                class_name=sanitize_input(data.get('class', ''), 20),
                section=sanitize_input(data.get('section', ''), 10),
                parent_id=data.get('parent_id'),
                gender=data.get('gender'),
                dob=data.get('dob')
            )
            db.session.add(student)
        
        elif role == 'teacher':
            teacher = Teacher(
                user_id=new_user.user_id,
                employee_id=sanitize_input(data.get('employee_id', ''), 50),
                subject=sanitize_input(data.get('subject', ''), 100),
                department=data.get('department')
            )
            db.session.add(teacher)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': new_user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to create user',
            'error': str(e)
        }), 500

@admin_bp.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    PUT /api/admin/user/:id
    Update user
    """
    try:
        admin = get_current_admin()
        
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Update fields
        if 'name' in data:
            user.name = sanitize_input(data['name'], 100)
        
        if 'email' in data:
            email = sanitize_input(data['email'], 120).lower()
            is_valid, error = validate_email(email)
            if not is_valid:
                return jsonify({'success': False, 'message': error}), 400
            
            # Check if email already exists
            existing = User.query.filter(User.email == email, User.user_id != user_id).first()
            if existing:
                return jsonify({
                    'success': False,
                    'message': 'Email already in use'
                }), 409
            
            user.email = email
        
        if 'password' in data:
            is_valid, error = validate_password_strength(data['password'])
            if not is_valid:
                return jsonify({'success': False, 'message': error}), 400
            user.set_password(data['password'])
        
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        # Update role-specific data
        if user.role == 'student' and user.student_profile:
            if 'class' in data:
                user.student_profile.class_name = sanitize_input(data['class'], 20)
            if 'section' in data:
                user.student_profile.section = sanitize_input(data['section'], 10)
            if 'parent_id' in data:
                user.student_profile.parent_id = data['parent_id']
        
        elif user.role == 'teacher' and user.teacher_profile:
            if 'subject' in data:
                user.teacher_profile.subject = sanitize_input(data['subject'], 100)
            if 'department' in data:
                user.teacher_profile.department = data['department']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update user',
            'error': str(e)
        }), 500

@admin_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    DELETE /api/admin/user/:id
    Delete user
    """
    try:
        admin = get_current_admin()
        
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Prevent self-deletion
        if user.user_id == admin.user_id:
            return jsonify({
                'success': False,
                'message': 'Cannot delete your own account'
            }), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to delete user',
            'error': str(e)
        }), 500

@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    """
    GET /api/admin/analytics
    Returns: system-wide statistics
    """
    try:
        admin = get_current_admin()
        
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        # User statistics
        total_users = User.query.count()
        students_count = User.query.filter_by(role='student').count()
        teachers_count = User.query.filter_by(role='teacher').count()
        parents_count = User.query.filter_by(role='parent').count()
        admins_count = User.query.filter_by(role='admin').count()
        active_users = User.query.filter_by(is_active=True).count()
        
        # Attendance statistics
        today = datetime.utcnow().date()
        today_attendance = Attendance.query.filter_by(date=today).all()
        present_today = sum(1 for a in today_attendance if a.status == 'present')
        
        # Overall attendance rate (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_attendance = Attendance.query.filter(
            Attendance.date >= thirty_days_ago.date()
        ).all()
        
        if recent_attendance:
            present_count = sum(1 for a in recent_attendance if a.status == 'present')
            overall_attendance_rate = round((present_count / len(recent_attendance)) * 100, 2)
        else:
            overall_attendance_rate = 0
        
        # Marks statistics
        all_marks = Marks.query.all()
        if all_marks:
            overall_average = round(
                sum((m.score / m.max_score * 100) for m in all_marks if m.max_score > 0) / len(all_marks), 2
            )
        else:
            overall_average = 0
        
        # Risk distribution
        all_students = Student.query.all()
        risk_distribution = {'low': 0, 'medium': 0, 'high': 0, 'unknown': 0}
        
        for student in all_students:
            prediction = Prediction.query.filter_by(
                student_id=student.student_id
            ).order_by(desc(Prediction.created_at)).first()
            
            if prediction:
                risk_distribution[prediction.risk_level] += 1
            else:
                risk_distribution['unknown'] += 1
        
        # Recent activity
        recent_users = User.query.order_by(desc(User.created_at)).limit(5).all()
        recent_users_data = [u.to_dict() for u in recent_users]
        
        # Alerts statistics
        total_alerts = Alert.query.count()
        unread_alerts = Alert.query.filter_by(is_read=False).count()
        critical_alerts = Alert.query.filter_by(severity='critical', is_read=False).count()
        
        # Resources statistics
        total_resources = Resource.query.count()
        resources_by_type = db.session.query(
            Resource.resource_type,
            func.count(Resource.resource_id)
        ).group_by(Resource.resource_type).all()
        
        return jsonify({
            'success': True,
            'analytics': {
                'users': {
                    'total': total_users,
                    'students': students_count,
                    'teachers': teachers_count,
                    'parents': parents_count,
                    'admins': admins_count,
                    'active': active_users
                },
                'attendance': {
                    'present_today': present_today,
                    'total_today': len(today_attendance),
                    'overall_rate_30days': overall_attendance_rate
                },
                'performance': {
                    'overall_average': overall_average,
                    'total_exams': len(all_marks)
                },
                'risk_distribution': risk_distribution,
                'alerts': {
                    'total': total_alerts,
                    'unread': unread_alerts,
                    'critical': critical_alerts
                },
                'resources': {
                    'total': total_resources,
                    'by_type': dict(resources_by_type)
                },
                'recent_users': recent_users_data
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch analytics',
            'error': str(e)
        }), 500

@admin_bp.route('/resources', methods=['GET'])
@jwt_required()
def get_resources():
    """
    GET /api/admin/resources
    Returns: all learning resources
    """
    try:
        admin = get_current_admin()
        
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        # Get pagination params
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        subject_filter = request.args.get('subject', None)
        
        # Build query
        query = Resource.query
        
        if subject_filter:
            query = query.filter_by(subject=subject_filter)
        
        # Paginate
        pagination = query.order_by(desc(Resource.created_at)).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        resources_data = [r.to_dict() for r in pagination.items]
        
        return jsonify({
            'success': True,
            'resources': resources_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch resources',
            'error': str(e)
        }), 500

@admin_bp.route('/resource', methods=['POST'])
@jwt_required()
def create_resource():
    """
    POST /api/admin/resource
    Add new learning resource
    """
    try:
        admin = get_current_admin()
        
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        subject = sanitize_input(data.get('subject', ''), 100)
        title = sanitize_input(data.get('title', ''), 200)
        description = sanitize_input(data.get('description', ''), 1000)
        link = sanitize_input(data.get('link', ''), 500)
        resource_type = sanitize_input(data.get('resource_type', ''), 50).lower()
        difficulty = sanitize_input(data.get('difficulty', ''), 20).lower()
        
        if not all([subject, title, link, resource_type, difficulty]):
            return jsonify({
                'success': False,
                'message': 'subject, title, link, resource_type, and difficulty are required'
            }), 400
        
        # Validate resource_type
        if resource_type not in ['video', 'article', 'pdf', 'quiz']:
            return jsonify({
                'success': False,
                'message': 'resource_type must be video, article, pdf, or quiz'
            }), 400
        
        # Validate difficulty
        if difficulty not in ['beginner', 'intermediate', 'advanced']:
            return jsonify({
                'success': False,
                'message': 'difficulty must be beginner, intermediate, or advanced'
            }), 400
        
        resource = Resource(
            subject=subject,
            title=title,
            description=description,
            link=link,
            resource_type=resource_type,
            difficulty=difficulty
        )
        
        db.session.add(resource)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Resource created successfully',
            'resource': resource.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to create resource',
            'error': str(e)
        }), 500

@admin_bp.route('/resource/<int:resource_id>', methods=['DELETE'])
@jwt_required()
def delete_resource(resource_id):
    """
    DELETE /api/admin/resource/:id
    Delete learning resource
    """
    try:
        admin = get_current_admin()
        
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        resource = Resource.query.get(resource_id)
        
        if not resource:
            return jsonify({
                'success': False,
                'message': 'Resource not found'
            }), 404
        
        db.session.delete(resource)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Resource deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to delete resource',
            'error': str(e)
        }), 500


@admin_bp.route('/import-data', methods=['POST'])
@jwt_required()
def import_data():
    """
    POST /api/admin/import-data
    Import data from CSV file
    Form data:
    - file_type: 'students'|'teachers'|'parents'|'marks'|'attendance'
    - file: CSV file
    - clear_existing: boolean (optional)
    """
    try:
        admin = get_current_admin()
        
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        # Check file extension
        if not file.filename.endswith('.csv'):
            return jsonify({
                'success': False,
                'message': 'File must be a CSV'
            }), 400
        
        # Get file type
        file_type = request.form.get('file_type', '').lower()
        clear_existing = request.form.get('clear_existing', 'false').lower() == 'true'
        
        if not file_type:
            return jsonify({
                'success': False,
                'message': 'file_type is required'
            }), 400
        
        # Read file content
        file_content = file.read()
        
        # Import based on type
        from utils.csv_import import (
            import_students_from_csv,
            import_teachers_from_csv,
            import_parents_from_csv,
            import_marks_from_csv,
            import_attendance_from_csv
        )
        
        if file_type == 'students':
            results = import_students_from_csv(file_content, clear_existing)
        elif file_type == 'teachers':
            results = import_teachers_from_csv(file_content, clear_existing)
        elif file_type == 'parents':
            results = import_parents_from_csv(file_content, clear_existing)
        elif file_type == 'marks':
            results = import_marks_from_csv(file_content, clear_existing)
        elif file_type == 'attendance':
            results = import_attendance_from_csv(file_content, clear_existing)
        else:
            return jsonify({
                'success': False,
                'message': f'Invalid file_type: {file_type}. Must be one of: students, teachers, parents, marks, attendance'
            }), 400
        
        # Return results
        status_code = 200 if results['success'] else 400
        
        return jsonify({
            'success': results['success'],
            'message': f"Import completed. {results['imported_count']} records imported.",
            'imported_count': results['imported_count'],
            'errors': results['errors'],
            'skipped': results.get('skipped', [])
        }), status_code
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to import data',
            'error': str(e)
        }), 500


@admin_bp.route('/csv-template/<template_type>', methods=['GET'])
@jwt_required()
def get_csv_template(template_type):
    """
    GET /api/admin/csv-template/:type
    Download CSV template
    Types: students, teachers, parents, marks, attendance
    """
    try:
        admin = get_current_admin()
        
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        from utils.csv_import import generate_csv_template
        from flask import Response
        
        template_type = template_type.lower()
        
        valid_types = ['students', 'teachers', 'parents', 'marks', 'attendance']
        if template_type not in valid_types:
            return jsonify({
                'success': False,
                'message': f'Invalid template type. Must be one of: {", ".join(valid_types)}'
            }), 400
        
        # Generate template
        template_content = generate_csv_template(template_type)
        
        if not template_content:
            return jsonify({
                'success': False,
                'message': 'Template not found'
            }), 404
        
        # Return as downloadable file
        return Response(
            template_content,
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename={template_type}_template.csv'
            }
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to generate template',
            'error': str(e)
        }), 500
