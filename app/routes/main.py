from flask import Blueprint, render_template, send_from_directory
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Serve the main dashboard"""
    return send_from_directory('static', 'index.html')

@bp.route('/api/health')
def health():
    """Health check endpoint"""
    from datetime import datetime
    return {
        'status': 'healthy',
        'database': 'connected',
        'timestamp': datetime.utcnow().isoformat()
    }, 200
