"""
Create admin account for CSV import
Run this after applying database indexes
"""

import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash
from app import create_app
from models import db, User

def create_admin():
    """Create admin account"""
    app = create_app()
    
    with app.app_context():
        print("🔐 Creating admin account...")
        
        # Check if admin already exists
        existing_admin = User.query.filter_by(email='priyasharma@school.edu').first()
        if existing_admin:
            print("⚠️  Admin account already exists!")
            print(f"   Email: priyasharma@school.edu")
            return
        
        # Create admin user
        admin = User(
            name='Priya Sharma',
            email='priyasharma@school.edu',
            password_hash=generate_password_hash('Priya_Sharma@123'),
            role='admin',
            is_active=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("\n✅ Admin account created successfully!")
        print("\n📋 Login Credentials:")
        print("   Name: Priya Sharma")
        print("   Email: priyasharma@school.edu")
        print("   Password: Priya_Sharma@123")
        print("\n🚀 Next Steps:")
        print("   1. Start backend: python app.py")
        print("   2. Start frontend: npm run dev (in frontend folder)")
        print("   3. Login at http://localhost:3000")
        print("   4. Click 'Import CSV Data' to import your 5 CSV files")

if __name__ == '__main__':
    create_admin()
