"""
Error Playground Middleware
Simulates various API errors for educational purposes
"""

import random
import time
from flask import request, jsonify, g

# Error scenarios for learning
ERROR_SCENARIOS = [
    {
        'type': 'timeout',
        'status': 408,
        'message': 'Request Timeout - Server took too long to respond',
        'explanation': 'This happens when the server is slow or overloaded. In production, implement retry logic.'
    },
    {
        'type': 'server_error',
        'status': 500,
        'message': 'Internal Server Error - Something went wrong on the server',
        'explanation': 'Server-side bugs cause this. The client cannot fix it - the server team needs to debug.'
    },
    {
        'type': 'service_unavailable',
        'status': 503,
        'message': 'Service Unavailable - Server is temporarily down',
        'explanation': 'Server is overloaded or under maintenance. Retry after a delay (exponential backoff).'
    },
    {
        'type': 'rate_limit',
        'status': 429,
        'message': 'Too Many Requests - You\'ve exceeded the rate limit',
        'explanation': 'APIs limit request frequency. Implement rate limiting on client side or upgrade your plan.'
    },
    {
        'type': 'bad_gateway',
        'status': 502,
        'message': 'Bad Gateway - Proxy or gateway error',
        'explanation': 'The server received an invalid response from an upstream server. Temporary issue.'
    }
]

def setup_error_playground(app):
    """Setup error playground middleware"""
    
    @app.before_request
    def inject_chaos():
        """Randomly inject errors based on settings"""
        
        # Skip for static files and admin endpoints
        if request.path.startswith('/static') or request.path == '/api/health':
            return None
        
        # Check if error playground is enabled (from query param or session)
        enabled = request.args.get('error_playground', 'false').lower() == 'true'
        chaos_level = float(request.args.get('chaos_level', '0.1'))
        latency = int(request.args.get('simulate_latency', '0'))
        
        # Store in g for access in other parts of request
        g.error_playground_enabled = enabled
        g.chaos_level = chaos_level
        
        # Simulate latency if requested
        if latency > 0 and enabled:
            time.sleep(latency / 1000.0)  # Convert ms to seconds
        
        # Inject random errors
        if enabled and random.random() < chaos_level:
            error_scenario = random.choice(ERROR_SCENARIOS)
            
            return jsonify({
                'error': error_scenario['message'],
                'code': f"SIMULATED_{error_scenario['type'].upper()}",
                'explanation': error_scenario['explanation'],
                'simulated': True,
                'hint': '🔥 This is a simulated error from Error Playground. Turn it off in Settings.'
            }), error_scenario['status']
        
        return None
    
    @app.after_request
    def add_playground_header(response):
        """Add header indicating if error playground is active"""
        if hasattr(g, 'error_playground_enabled') and g.error_playground_enabled:
            response.headers['X-Error-Playground'] = 'enabled'
            response.headers['X-Chaos-Level'] = str(g.chaos_level)
        return response
