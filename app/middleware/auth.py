from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models import User
from app import basic_auth

# Basic Auth password verifier
@basic_auth.verify_password
def verify_password(email, password):
    """Verify Basic Auth credentials"""
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None

@basic_auth.error_handler
def basic_auth_error(status):
    """Return JSON error for Basic Auth failures"""
    return jsonify({
        'error': 'Invalid credentials',
        'code': 'BASIC_AUTH_FAILED',
        'hint': 'Check your username (email) and password'
    }), status

# Admin role checker for JWT
def admin_required():
    """Decorator to require admin role for JWT-protected routes"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({
                    'error': 'User not found',
                    'code': 'USER_NOT_FOUND'
                }), 404
            
            if user.role != 'admin':
                return jsonify({
                    'error': 'Admin access required',
                    'code': 'ADMIN_REQUIRED'
                }), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper
