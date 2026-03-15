from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models import User

def jwt_required_custom(fn):
    """
    Custom JWT required decorator with better error handling
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token',
                'error': str(e)
            }), 401
    return wrapper

def role_required(allowed_roles):
    """
    Decorator to check if user has required role
    Usage: @role_required(['student', 'teacher'])
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = int(get_jwt_identity())
                
                # Get user from database
                user = User.query.get(user_id)
                
                if not user:
                    return jsonify({
                        'success': False,
                        'message': 'User not found'
                    }), 404
                
                if not user.is_active:
                    return jsonify({
                        'success': False,
                        'message': 'Account is inactive'
                    }), 403
                
                if user.role not in allowed_roles:
                    return jsonify({
                        'success': False,
                        'message': f'Access denied. Required roles: {", ".join(allowed_roles)}'
                    }), 403
                
                return fn(*args, **kwargs)
            
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': 'Authorization failed',
                    'error': str(e)
                }), 401
        
        return wrapper
    return decorator

def get_current_user():
    """
    Helper function to get current authenticated user
    """
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        return user
    except:
        return None
