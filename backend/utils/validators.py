import re
from typing import Tuple

def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format
    Returns: (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    email = email.strip().lower()
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    if len(email) > 120:
        return False, "Email is too long"
    
    return True, ""

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength
    Requirements: min 8 chars, 1 uppercase, 1 lowercase, 1 number
    Returns: (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > 128:
        return False, "Password is too long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, ""

def sanitize_input(text: str, max_length: int = 255) -> str:
    """
    Sanitize user input by stripping whitespace and limiting length
    """
    if not text:
        return ""
    
    text = text.strip()
    
    if len(text) > max_length:
        text = text[:max_length]
    
    return text

def validate_role(role: str) -> Tuple[bool, str]:
    """
    Validate user role
    Returns: (is_valid, error_message)
    """
    valid_roles = ['student', 'teacher', 'parent', 'admin']
    
    if not role:
        return False, "Role is required"
    
    role = role.lower().strip()
    
    if role not in valid_roles:
        return False, f"Invalid role. Must be one of: {', '.join(valid_roles)}"
    
    return True, ""

def validate_name(name: str) -> Tuple[bool, str]:
    """
    Validate user name
    Returns: (is_valid, error_message)
    """
    if not name:
        return False, "Name is required"
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name) > 100:
        return False, "Name is too long"
    
    return True, ""
