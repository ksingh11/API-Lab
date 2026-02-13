from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger
from app.config import config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
basic_auth = HTTPBasicAuth()

def create_app(config_name='default'):
    """Flask application factory"""
    app = Flask(__name__, 
                static_folder='static',
                static_url_path='/static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Initialize Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs/swagger"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API Zero to Hero - Interactive Learning API",
            "description": """
# Welcome to API Zero to Hero! 🎓

Learn REST APIs through hands-on experimentation in your browser!

## 🔐 How to Authenticate

Click the **"Authorize"** button (top right) and choose one method:

### Option 1: Basic Auth (Username/Password)
- **Username:** `testuser@apilab.dev`  
- **Password:** `test123`

**Admin credentials:**  
- **Username:** `admin@apilab.dev`  
- **Password:** `admin123`

### Option 2: Bearer Token (JWT)
1. Call **POST /api/auth/login** with credentials
2. Copy the `token` from response
3. Click "Authorize" → Enter: `Bearer YOUR_TOKEN`

---

**💡 Tip:** Click any endpoint below → "Try it out" → "Execute" to see it in action!
            """,
            "version": "1.0.0",
            "contact": {
                "name": "API Zero to Hero",
                "url": "https://github.com/yourusername/apilab"
            }
        },
        "host": "",  # Will be auto-detected
        "basePath": "/api",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT token from /api/auth/login. Format: 'Bearer YOUR_TOKEN_HERE'"
            },
            "BasicAuth": {
                "type": "basic",
                "description": "Use email as username. Default: testuser@apilab.dev / test123"
            }
        },
        "tags": [
            {"name": "Authentication", "description": "Login and get JWT tokens"},
            {"name": "Todos", "description": "Create, read, update, and delete todo items"},
            {"name": "Admin", "description": "Admin-only endpoints (user management, database)"}
        ]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Register blueprints
    from app.routes import auth, todos, admin, postman, main, scenarios
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(todos.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(postman.bp)
    app.register_blueprint(scenarios.bp)
    
    # Setup request logging middleware
    from app.middleware.logging import setup_request_logging
    setup_request_logging(app)
    
    # Setup error playground middleware
    from app.middleware.error_playground import setup_error_playground
    setup_error_playground(app)
    
    # Create database tables and auto-seed if empty
    with app.app_context():
        import os
        
        # Create instance directory if it doesn't exist
        instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
            print(f"✅ Created instance directory: {instance_path}")
        
        # Create tables if they don't exist
        db.create_all()
        
        # Auto-seed if database is empty
        from app.models import User
        if User.query.count() == 0:
            print("⚠️  Database is empty. Auto-seeding with default data...")
            from app.utils.seed import seed_database
            seed_database()
    
    return app
