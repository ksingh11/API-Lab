import time
import json
from flask import request, g
from app import db
from app.models import RequestLog

def setup_request_logging(app):
    """Setup request logging middleware"""
    
    @app.before_request
    def before_request():
        """Record request start time"""
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        """Log request details after response is generated"""
        
        # Skip logging for static files and health check
        if request.path.startswith('/static') or request.path == '/api/health':
            return response
        
        # Calculate latency
        latency_ms = int((time.time() - g.start_time) * 1000) if hasattr(g, 'start_time') else None
        
        # Get request body (if JSON)
        request_body = None
        if request.is_json:
            try:
                request_body = json.dumps(request.get_json())
            except:
                pass
        
        # Get response body (if JSON and not too large)
        response_body = None
        if response.is_json and response.content_length and response.content_length < 10000:
            try:
                response_body = response.get_data(as_text=True)
            except:
                pass
        
        # Detect auth method
        auth_method = 'none'
        user_id = None
        
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Basic '):
            auth_method = 'basic'
            # Try to get user from Basic Auth
            try:
                from app import basic_auth
                user = basic_auth.current_user()
                if user:
                    user_id = user.id
            except:
                pass
        elif auth_header.startswith('Bearer '):
            auth_method = 'token'
            # Try to get user from JWT
            try:
                from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
                verify_jwt_in_request(optional=True)
                user_id = get_jwt_identity()
            except:
                pass
        
        # Create log entry
        log = RequestLog(
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            latency_ms=latency_ms,
            request_body=request_body,
            response_body=response_body,
            auth_method=auth_method,
            user_id=user_id,
            ip_address=request.remote_addr
        )
        
        db.session.add(log)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        
        return response
