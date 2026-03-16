"""
Script to create initial admin user on Render deployment.
Run this after deployment to set up the first admin account.

Usage:
    python create_admin_render.py
"""

import os
import sys
from app import create_app
from models import db, User

def create_admin():
    """Create initial admin user for production deployment."""
    
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@school.com').first()
        
        if admin:
            print("✓ Admin user already exists!")
            print(f"  Email: {admin.email}")
            print(f"  Role: {admin.role}")
            return
        
        # Create new admin user
        try:
            admin = User(
                name='Administrator',
                email='admin@school.com',
                password='admin123',  # Change this after first login!
                role='admin',
                is_active=True
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print("✓ Admin user created successfully!")
            print("\n📋 Admin Credentials:")
            print("   Email: admin@school.com")
            print("   Password: admin123")
            print("\n⚠️  IMPORTANT: Change the password after first login!")
            print("   Go to Settings → Change Password")
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error creating admin user: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    print("🚀 Creating admin user for Render deployment...\n")
    create_admin()
    print("\n✓ Setup complete!")
