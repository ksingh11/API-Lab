from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app import db, basic_auth
from app.models import Todo, User
import base64

bp = Blueprint('todos', __name__, url_prefix='/api/todos')

def get_authenticated_user():
    """
    Get authenticated user from either JWT token or Basic Auth.
    Returns User object or None if not authenticated.
    """
    auth_header = request.headers.get('Authorization', '')
    
    # Try JWT first
    if auth_header.startswith('Bearer '):
        try:
            verify_jwt_in_request(optional=False)
            user_id_str = get_jwt_identity()
            if user_id_str:
                user_id = int(user_id_str)  # Convert string back to int
                user = User.query.get(user_id)
                if user:
                    return user
        except:
            pass
    
    # Try Basic Auth
    if auth_header.startswith('Basic '):
        try:
            # Decode Basic Auth credentials
            encoded_credentials = auth_header.replace('Basic ', '')
            decoded = base64.b64decode(encoded_credentials).decode('utf-8')
            email, password = decoded.split(':', 1)
            
            # Verify credentials
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                return user
        except:
            pass
    
    return None

@bp.route('', methods=['GET'])
def get_todos():
    """
    Get all todos for the authenticated user.
    Supports both Basic Auth and JWT Token Auth.
    
    Headers:
        Authorization: Basic <base64(email:password)>
        OR
        Authorization: Bearer <jwt_token>
    
    Response:
        {
            "data": [...],
            "count": 5
        }
    """
    user = get_authenticated_user()
    
    if not user:
        return jsonify({
            'error': 'Authentication required',
            'code': 'AUTH_REQUIRED',
            'hint': 'Use Basic Auth (email:password) or Bearer token'
        }), 401
    
    todos = Todo.query.filter_by(user_id=user.id).all()
    
    return jsonify({
        'data': [todo.to_dict() for todo in todos],
        'count': len(todos)
    }), 200

@bp.route('/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """
    Get a specific todo by ID.
    User can only access their own todos.
    """
    user = get_authenticated_user()
    
    if not user:
        return jsonify({
            'error': 'Authentication required',
            'code': 'AUTH_REQUIRED'
        }), 401
    
    todo = Todo.query.get(todo_id)
    
    if not todo:
        return jsonify({
            'error': 'Todo not found',
            'code': 'TODO_NOT_FOUND'
        }), 404
    
    # Check ownership
    if todo.user_id != user.id:
        return jsonify({
            'error': 'You do not have permission to view this todo',
            'code': 'FORBIDDEN'
        }), 403
    
    return jsonify({
        'data': todo.to_dict()
    }), 200

@bp.route('', methods=['POST'])
def create_todo():
    """
    Create a new todo.
    
    Request Body:
        {
            "title": "My new todo",
            "description": "Optional description",
            "completed": false
        }
    
    Response:
        {
            "data": {...}
        }
    """
    user = get_authenticated_user()
    
    if not user:
        return jsonify({
            'error': 'Authentication required',
            'code': 'AUTH_REQUIRED'
        }), 401
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Request body is required',
            'code': 'NO_DATA'
        }), 400
    
    # Validate title
    title = data.get('title', '').strip()
    if not title:
        return jsonify({
            'error': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'fields': {
                'title': 'Title is required'
            }
        }), 422
    
    if len(title) > 255:
        return jsonify({
            'error': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'fields': {
                'title': 'Title must be 255 characters or less'
            }
        }), 422
    
    # Create todo
    todo = Todo(
        title=title,
        description=data.get('description', ''),
        completed=data.get('completed', False),
        user_id=user.id
    )
    
    db.session.add(todo)
    db.session.commit()
    
    return jsonify({
        'data': todo.to_dict()
    }), 201

@bp.route('/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """
    Update an existing todo.
    
    Request Body:
        {
            "title": "Updated title",
            "description": "Updated description",
            "completed": true
        }
    """
    user = get_authenticated_user()
    
    if not user:
        return jsonify({
            'error': 'Authentication required',
            'code': 'AUTH_REQUIRED'
        }), 401
    
    todo = Todo.query.get(todo_id)
    
    if not todo:
        return jsonify({
            'error': 'Todo not found',
            'code': 'TODO_NOT_FOUND'
        }), 404
    
    # Check ownership
    if todo.user_id != user.id:
        return jsonify({
            'error': 'You do not have permission to update this todo',
            'code': 'FORBIDDEN'
        }), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Request body is required',
            'code': 'NO_DATA'
        }), 400
    
    # Update fields
    if 'title' in data:
        title = data['title'].strip()
        if not title:
            return jsonify({
                'error': 'Validation failed',
                'code': 'VALIDATION_ERROR',
                'fields': {
                    'title': 'Title cannot be empty'
                }
            }), 422
        todo.title = title
    
    if 'description' in data:
        todo.description = data['description']
    
    if 'completed' in data:
        todo.completed = bool(data['completed'])
    
    db.session.commit()
    
    return jsonify({
        'data': todo.to_dict()
    }), 200

@bp.route('/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """
    Delete a todo.
    """
    user = get_authenticated_user()
    
    if not user:
        return jsonify({
            'error': 'Authentication required',
            'code': 'AUTH_REQUIRED'
        }), 401
    
    todo = Todo.query.get(todo_id)
    
    if not todo:
        return jsonify({
            'error': 'Todo not found',
            'code': 'TODO_NOT_FOUND'
        }), 404
    
    # Check ownership
    if todo.user_id != user.id:
        return jsonify({
            'error': 'You do not have permission to delete this todo',
            'code': 'FORBIDDEN'
        }), 403
    
    db.session.delete(todo)
    db.session.commit()
    
    return '', 204
