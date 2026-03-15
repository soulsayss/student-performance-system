from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from models import db, User, Student, Teacher
from utils.validators import validate_email, validate_password_strength, validate_role, validate_name, sanitize_input
from utils.decorators import jwt_required_custom
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

# Token blacklist (in production, use Redis)
token_blacklist = set()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    POST /api/auth/register
    Body: {name, email, password, role, additional_data}
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Extract and sanitize inputs
        name = sanitize_input(data.get('name', ''), 100)
        email = sanitize_input(data.get('email', ''), 120).lower()
        password = data.get('password', '')
        role = sanitize_input(data.get('role', ''), 20).lower()
        
        # Validate inputs
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
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 409
        
        # Create new user
        new_user = User(
            name=name,
            email=email,
            role=role,
            is_active=True
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.flush()  # Get user_id before commit
        
        # Create role-specific record
        if role == 'student':
            roll_number = data.get('roll_number')
            class_name = data.get('class')
            section = data.get('section')
            
            if not all([roll_number, class_name, section]):
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': 'Student registration requires roll_number, class, and section'
                }), 400
            
            student = Student(
                user_id=new_user.user_id,
                roll_number=sanitize_input(roll_number, 50),
                class_name=sanitize_input(class_name, 20),
                section=sanitize_input(section, 10),
                gender=data.get('gender'),
                dob=data.get('dob')
            )
            db.session.add(student)
        
        elif role == 'teacher':
            employee_id = data.get('employee_id')
            subject = data.get('subject')
            
            if not all([employee_id, subject]):
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': 'Teacher registration requires employee_id and subject'
                }), 400
            
            teacher = Teacher(
                user_id=new_user.user_id,
                employee_id=sanitize_input(employee_id, 50),
                subject=sanitize_input(subject, 100),
                department=data.get('department')
            )
            db.session.add(teacher)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': new_user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Registration failed',
            'error': str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and generate JWT token
    POST /api/auth/login
    Body: {email, password}
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        email = sanitize_input(data.get('email', ''), 120).lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'message': 'Account is inactive. Please contact administrator.'
            }), 403
        
        # Generate tokens
        access_token = create_access_token(identity=str(user.user_id))
        refresh_token = create_refresh_token(identity=str(user.user_id))
        
        # Get role-specific data
        user_data = user.to_dict()
        
        if user.role == 'student' and user.student_profile:
            user_data['student_info'] = user.student_profile.to_dict()
        elif user.role == 'teacher' and user.teacher_profile:
            user_data['teacher_info'] = user.teacher_profile.to_dict()
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user_data
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Login failed',
            'error': str(e)
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user (add token to blacklist)
    POST /api/auth/logout
    """
    try:
        jti = get_jwt()['jti']
        token_blacklist.add(jti)
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Logout failed',
            'error': str(e)
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user profile
    GET /api/auth/profile
    """
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        user_data = user.to_dict()
        
        # Add role-specific data
        if user.role == 'student' and user.student_profile:
            user_data['student_info'] = user.student_profile.to_dict()
        elif user.role == 'teacher' and user.teacher_profile:
            user_data['teacher_info'] = user.teacher_profile.to_dict()
        
        return jsonify({
            'success': True,
            'user': user_data
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch profile',
            'error': str(e)
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    POST /api/auth/refresh
    """
    try:
        user_id = int(get_jwt_identity())
        access_token = create_access_token(identity=str(user_id))
        
        return jsonify({
            'success': True,
            'access_token': access_token
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Token refresh failed',
            'error': str(e)
        }), 500

# Check if token is blacklisted
@auth_bp.before_app_request
def check_if_token_revoked():
    """
    Check if token is in blacklist before processing request
    """
    try:
        if request.endpoint and 'auth' in request.endpoint:
            jwt_data = get_jwt()
            if jwt_data and jwt_data.get('jti') in token_blacklist:
                return jsonify({
                    'success': False,
                    'message': 'Token has been revoked'
                }), 401
    except:
        pass
