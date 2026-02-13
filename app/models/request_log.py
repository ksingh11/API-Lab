from datetime import datetime
from app import db

class RequestLog(db.Model):
    """Request log model for tracking API calls"""
    __tablename__ = 'request_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(10), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    latency_ms = db.Column(db.Integer)
    request_body = db.Column(db.Text)
    response_body = db.Column(db.Text)
    auth_method = db.Column(db.String(20))  # 'basic', 'token', or 'none'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'id': self.id,
            'method': self.method,
            'path': self.path,
            'status_code': self.status_code,
            'latency_ms': self.latency_ms,
            'request_body': self.request_body,
            'response_body': self.response_body,
            'auth_method': self.auth_method,
            'user_id': self.user_id,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    def __repr__(self):
        return f'<RequestLog {self.method} {self.path}>'
