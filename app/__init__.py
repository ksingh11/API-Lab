from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_httpauth import HTTPBasicAuth
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
