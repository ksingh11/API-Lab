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
    """
    Reset database to default state.
    
    IMPORTANT: This preserves the default users (admin, testuser) to prevent lockout.
    Only todos and request logs are cleared and reseeded.
    """
    print("🔄 Resetting database...")
    
    # Import RequestLog here to avoid circular imports
    from app.models import RequestLog
    
    # Clear todos (all of them)
    Todo.query.delete()
    print("  ✓ Cleared all todos")
    
    # Clear request logs
    RequestLog.query.delete()
    print("  ✓ Cleared request logs")
    
    # Ensure default users exist (don't delete users to prevent lockout)
    admin = User.query.filter_by(email='admin@apilab.dev').first()
    if not admin:
        admin = User(email='admin@apilab.dev', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        print("  ✓ Created admin user")
    else:
        # Reset admin password in case it was changed
        admin.set_password('admin123')
        admin.role = 'admin'
        print("  ✓ Reset admin credentials")
    
    testuser = User.query.filter_by(email='testuser@apilab.dev').first()
    if not testuser:
        testuser = User(email='testuser@apilab.dev', role='user')
        testuser.set_password('test123')
        db.session.add(testuser)
        print("  ✓ Created test user")
    else:
        # Reset testuser password in case it was changed
        testuser.set_password('test123')
        testuser.role = 'user'
        print("  ✓ Reset testuser credentials")
    
    db.session.commit()
    
    # Refresh user objects to get their IDs
    db.session.refresh(admin)
    db.session.refresh(testuser)
    
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
            title='Partially update with PATCH',
            description='Update only specific fields using PATCH method',
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
    
    print(f"✅ Database reset complete: 2 users, {len(todos)} todos")
    return {
        'users': 2,
        'todos': len(todos)
    }
