from app import db
from app.models import User, Todo

def seed_database():
    """Seed database with default test data"""
    print("🌱 Seeding database...")
    
    # Create admin user
    admin = User(email='admin@apilab.dev', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create test user
    testuser = User(email='testuser@apilab.dev', role='user')
    testuser.set_password('test123')
    db.session.add(testuser)
    
    db.session.commit()
    
    # Create sample todos
    todos = [
        Todo(
            title='Learn what an API is',
            description='Understand the basics of APIs and REST architecture',
            completed=True,
            user_id=testuser.id
        ),
        Todo(
            title='Make your first GET request',
            description='Fetch the list of todos from the API',
            completed=True,
            user_id=testuser.id
        ),
        Todo(
            title='Create a todo with POST',
            description='Add a new todo to the database using POST method',
            completed=False,
            user_id=testuser.id
        ),
        Todo(
            title='Update a todo with PUT',
            description='Mark a todo as completed using PUT method',
            completed=False,
            user_id=testuser.id
        ),
        Todo(
            title='Delete a todo',
            description='Remove a todo from the database using DELETE method',
            completed=False,
            user_id=testuser.id
        ),
        Todo(
            title='Monitor server health',
            description='Admin task: Check system logs and database status',
            completed=False,
            user_id=admin.id
        )
    ]
    
    for todo in todos:
        db.session.add(todo)
    
    db.session.commit()
    
    print(f"✅ Seeded database with 2 users and {len(todos)} todos")
    return {
        'users': 2,
        'todos': len(todos)
    }

def reset_database():
    """Drop all tables and recreate with seed data"""
    print("🔄 Resetting database...")
    
    # Drop all tables
    db.drop_all()
    print("  ✓ Dropped all tables")
    
    # Recreate tables
    db.create_all()
    print("  ✓ Recreated tables")
    
    # Seed with default data
    result = seed_database()
    
    print("✅ Database reset complete")
    return result
