#!/usr/bin/env python
"""
Database initialization script for production deployment.

This script:
1. Creates all database tables
2. Creates initial admin user
3. Can be run once after deployment on Render

Usage:
    python init_db.py

After running, you can log in with:
    Email: admin@school.edu
    Password: Admin@123
"""

import os
import sys
from app import create_app
from models import db, User

def init_database():
    """Initialize database and create admin user."""
    
    print("🚀 Initializing database...\n")
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            print("📊 Creating database tables...")
            db.create_all()
            print("✓ Database tables created successfully!\n")
            
            # Check if admin already exists
            admin = User.query.filter_by(email='admin@school.edu').first()
            
            if admin:
                print("⚠️  Admin user already exists!")
                print(f"   Email: {admin.email}")
                print(f"   Role: {admin.role}")
                print("\n✓ Database initialization complete!")
                return True
            
            # Create admin user
            print("👤 Creating admin user...")
            admin = User(
                name='Administrator',
                email='admin@school.edu',
                password='Admin@123',
                role='admin',
                is_active=True
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print("✓ Admin user created successfully!\n")
            print("📋 Admin Credentials:")
            print("   Email: admin@school.edu")
            print("   Password: Admin@123")
            print("\n⚠️  IMPORTANT: Change the password after first login!")
            print("   Go to Settings → Change Password\n")
            print("✓ Database initialization complete!")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error during initialization: {str(e)}")
            print("\nTroubleshooting:")
            print("1. Make sure DATABASE_URL is set correctly")
            print("2. Check that PostgreSQL is running")
            print("3. Verify network connectivity")
            sys.exit(1)

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
