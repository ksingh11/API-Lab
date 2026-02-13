#!/usr/bin/env python3
"""
API Zero to Hero - Interactive API Learning Sandbox
Entry point for the application
"""

import os
from app import create_app

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
