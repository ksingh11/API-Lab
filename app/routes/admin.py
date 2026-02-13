from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Todo, RequestLog
from app.utils.seed import reset_database

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def require_admin():
    """Helper to check if current user is admin"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return None, jsonify({
            'error': 'User not found',
            'code': 'USER_NOT_FOUND'
        }), 404
    
    if user.role != 'admin':
        return None, jsonify({
            'error': 'Admin access required',
            'code': 'ADMIN_REQUIRED',
            'hint': 'This endpoint requires admin role'
        }), 403
    
    return user, None, None

@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """
    Get all users (admin only).
    
    Response:
        {
            "data": [...],
            "count": 2
        }
    """
    user, error, status = require_admin()
    if error:
        return error, status
    
    users = User.query.all()
    
    return jsonify({
        'data': [u.to_dict() for u in users],
        'count': len(users)
    }), 200

@bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    """
    Get request logs (admin only).
    
    Query Parameters:
        limit: Maximum number of logs (default: 100)
        method: Filter by HTTP method (GET, POST, etc.)
        status: Filter by status code
    
    Response:
        {
            "data": [...],
            "count": 23
        }
    """
    user, error, status = require_admin()
    if error:
        return error, status
    
    # Get query parameters
    limit = request.args.get('limit', 100, type=int)
    method = request.args.get('method', None)
    status_code = request.args.get('status', None, type=int)
    
    # Build query
    query = RequestLog.query
    
    if method:
        query = query.filter_by(method=method.upper())
    
    if status_code:
        query = query.filter_by(status_code=status_code)
    
    # Order by newest first and limit
    logs = query.order_by(RequestLog.timestamp.desc()).limit(limit).all()
    
    return jsonify({
        'data': [log.to_dict() for log in logs],
        'count': len(logs)
    }), 200

@bp.route('/db/tables/<table_name>', methods=['GET'])
@jwt_required()
def get_table_data(table_name):
    """
    Get all data from a specific table.
    For learning purposes, any authenticated user can view database tables.
    
    Supported tables: todos, users, request_logs
    
    Response:
        {
            "table": "todos",
            "rows": [...],
            "count": 5
        }
    """
    # Allow any authenticated user to view database (learning platform)
    # No admin check needed
    
    # Map table names to models
    tables = {
        'todos': Todo,
        'users': User,
        'request_logs': RequestLog
    }
    
    if table_name not in tables:
        return jsonify({
            'error': f'Invalid table name: {table_name}',
            'code': 'INVALID_TABLE',
            'valid_tables': list(tables.keys())
        }), 400
    
    model = tables[table_name]
    rows = model.query.all()
    
    return jsonify({
        'table': table_name,
        'rows': [row.to_dict() for row in rows],
        'count': len(rows)
    }), 200

@bp.route('/reset', methods=['POST'])
@jwt_required()
def reset_db():
    """
    Reset database to default seed data.
    
    For learning purposes, any authenticated user can reset the database.
    In production, this would be admin-only.
    
    WARNING: This will delete ALL data and restore defaults.
    
    Response:
        {
            "message": "Database reset successfully",
            "seed_data": {
                "users": 2,
                "todos": 6
            }
        }
    """
    # Allow any authenticated user to reset (this is a learning sandbox)
    # In production, you would use: require_admin()
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'error': 'User not found',
            'code': 'USER_NOT_FOUND'
        }), 404
    
    try:
        result = reset_database()
        
        return jsonify({
            'message': 'Database reset successfully',
            'seed_data': result
        }), 200
    except Exception as e:
        return jsonify({
            'error': f'Failed to reset database: {str(e)}',
            'code': 'RESET_FAILED'
        }), 500
