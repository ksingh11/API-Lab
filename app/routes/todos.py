from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app import db, basic_auth
from app.models import Todo, User
import base64

bp = Blueprint('todos', __name__, url_prefix='/api/todos')

@bp.errorhandler(405)
def method_not_allowed(e):
    """
    Handle Method Not Allowed errors with helpful guidance.
    """
    method = request.method
    path = request.path
    
    # Common mistakes and helpful hints
    hints = []
    
    if method in ['PUT', 'PATCH', 'DELETE']:
        if not any(char.isdigit() for char in path):
            hints.append(f"{method} requires a todo ID in the URL. Example: /api/todos/5")
    
    if method == 'POST' and '/' in path.replace('/api/todos', '').replace('/api/todos/', ''):
        hints.append("POST creates new todos and doesn't need an ID. Use /api/todos (without ID)")
    
    return jsonify({
        'error': 'Method Not Allowed',
        'code': 'METHOD_NOT_ALLOWED',
        'method': method,
        'path': path,
        'hint': hints[0] if hints else f'{method} is not supported for this endpoint',
        'allowed_methods': {
            '/api/todos': ['GET', 'POST'],
            '/api/todos/:id': ['GET', 'PUT', 'PATCH', 'DELETE']
        }
    }), 405

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
    Get all todos for the authenticated user
    ---
    tags:
      - Todos
    summary: Get all todos
    description: Returns all todos for the authenticated user. Supports both Basic Auth and JWT Token Auth.
    security:
      - Bearer: []
      - BasicAuth: []
    responses:
      200:
        description: List of todos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              title:
                type: string
                example: "Buy groceries"
              description:
                type: string
                example: "Milk, eggs, bread"
              completed:
                type: boolean
                example: false
              owner_id:
                type: integer
                example: 1
              created_at:
                type: string
                format: date-time
              updated_at:
                type: string
                format: date-time
      401:
        description: Unauthorized - Authentication required
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Authentication required"
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
    Get a single todo by ID
    ---
    tags:
      - Todos
    summary: Get one specific todo
    description: Returns a single todo item. Users can only view their own todos.
    security:
      - Bearer: []
      - BasicAuth: []
    parameters:
      - in: path
        name: todo_id
        required: true
        type: integer
        description: ID of the todo to retrieve
        example: 1
    responses:
      200:
        description: Todo retrieved successfully
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                title:
                  type: string
                  example: Buy groceries
                description:
                  type: string
                completed:
                  type: boolean
                owner_id:
                  type: integer
                created_at:
                  type: string
                  format: date-time
      401:
        description: Authentication required
      403:
        description: Not authorized to view this todo
      404:
        description: Todo not found
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
    Create a new todo
    ---
    tags:
      - Todos
    summary: Create a new todo item
    description: Creates a new todo task. Requires authentication.
    security:
      - Bearer: []
      - BasicAuth: []
    parameters:
      - in: body
        name: todo
        required: true
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
              example: Buy groceries
              description: Todo title (required, max 255 chars)
            description:
              type: string
              example: Milk, eggs, bread
              description: Optional description
            completed:
              type: boolean
              example: false
              description: Completion status (default false)
    responses:
      201:
        description: Todo created successfully
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 42
                title:
                  type: string
                  example: Buy groceries
                description:
                  type: string
                completed:
                  type: boolean
                owner_id:
                  type: integer
                created_at:
                  type: string
                  format: date-time
      400:
        description: Missing request body
      401:
        description: Authentication required
      422:
        description: Validation error (missing title or too long)
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

@bp.route('/<int:todo_id>', methods=['PUT', 'PATCH'])
def update_todo(todo_id):
    """
    Update a todo (PUT = full update, PATCH = partial update)
    ---
    tags:
      - Todos
    summary: Update an existing todo
    description: |
      **PUT**: Full update - send all fields (replaces entire todo)
      
      **PATCH**: Partial update - send only fields to change
    security:
      - Bearer: []
      - BasicAuth: []
    parameters:
      - in: path
        name: todo_id
        required: true
        type: integer
        description: ID of the todo to update
        example: 5
      - in: body
        name: todo
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: Buy milk and eggs
              description: New title (required for PUT, optional for PATCH)
            description:
              type: string
              example: From the organic store
              description: New description (optional)
            completed:
              type: boolean
              example: true
              description: Completion status (optional)
    responses:
      200:
        description: Todo updated successfully
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                id:
                  type: integer
                title:
                  type: string
                description:
                  type: string
                completed:
                  type: boolean
                owner_id:
                  type: integer
                updated_at:
                  type: string
                  format: date-time
      401:
        description: Authentication required
      403:
        description: Not authorized to update this todo
      404:
        description: Todo not found
      422:
        description: Validation error
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
    Delete a todo
    ---
    tags:
      - Todos
    summary: Delete a todo item
    description: Permanently deletes a todo. Only the owner can delete their todos.
    security:
      - Bearer: []
      - BasicAuth: []
    parameters:
      - in: path
        name: todo_id
        required: true
        type: integer
        description: ID of the todo to delete
        example: 5
    responses:
      204:
        description: Todo deleted successfully (no content)
      401:
        description: Authentication required
      403:
        description: Not authorized to delete this todo
      404:
        description: Todo not found
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
