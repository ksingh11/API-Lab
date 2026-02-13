from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app import db
from app.models import User

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    """
    Login to get JWT token
    ---
    tags:
      - Authentication
    summary: Login with email and password
    description: Returns a JWT token valid for 24 hours. Use this token for authenticated requests.
    parameters:
      - in: body
        name: credentials
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: testuser@apilab.dev
              description: User email address
            password:
              type: string
              example: test123
              description: User password
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
              description: JWT token (use in Authorization header)
            user:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                email:
                  type: string
                  example: testuser@apilab.dev
                role:
                  type: string
                  example: user
            expires_in:
              type: integer
              example: 86400
              description: Token expiry time in seconds (24 hours)
      400:
        description: Missing email or password
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Request body is required',
            'code': 'NO_DATA'
        }), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({
            'error': 'Email and password are required',
            'code': 'MISSING_CREDENTIALS'
        }), 400
    
    # Find user
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({
            'error': 'Invalid credentials',
            'code': 'LOGIN_FAILED',
            'hint': 'Check your email and password'
        }), 401
    
    # Create access token (identity must be a string)
    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(hours=24)
    )
    
    return jsonify({
        'token': access_token,
        'user': user.to_dict(),
        'expires_in': 86400  # 24 hours in seconds
    }), 200

@bp.route('/me', methods=['GET'])
def get_current_user():
    """
    Get current user info (requires JWT token)
    
    Headers:
        Authorization: Bearer <token>
    
    Response:
        {
            "user": {...}
        }
    """
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    @jwt_required()
    def _get_current_user():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'error': 'User not found',
                'code': 'USER_NOT_FOUND'
            }), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
    
    return _get_current_user()
