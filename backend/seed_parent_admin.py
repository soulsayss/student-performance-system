"""
Script to seed parent and admin users
"""
from app import create_app
from models import db, User, Student

app = create_app()

with app.app_context():
    print("Creating parent and admin users...")
    
    # Create parent user
    parent = User(
        name="Mary Doe",
        email="mary@example.com",
        role="parent",
        is_active=True
    )
    parent.set_password("Parent123")
    db.session.add(parent)
    db.session.flush()
    
    print(f"Parent created: {parent.name} (ID: {parent.user_id})")
    
    # Link John Doe (student) to parent
    student = Student.query.get(1)
    if student:
        student.parent_id = parent.user_id
        print(f"Linked student {student.user.name} to parent {parent.name}")
    
    # Create admin user
    admin = User(
        name="Admin User",
        email="admin@example.com",
        role="admin",
        is_active=True
    )
    admin.set_password("Admin123")
    db.session.add(admin)
    
    print(f"Admin created: {admin.name}")
    
    db.session.commit()
    print("\n✅ Parent and admin users created successfully!")
    print("\nLogin credentials:")
    print("Parent - Email: mary@example.com, Password: Parent123")
    print("Admin - Email: admin@example.com, Password: Admin123")
