"""
Fix teacher email addresses that were generated incorrectly
"""
from app import create_app
from models import db, User, Teacher

def fix_teacher_emails():
    """Fix teacher emails by removing leading dots and other issues"""
    app = create_app()
    
    with app.app_context():
        print("Fixing teacher email addresses...")
        
        # Get all teachers
        teachers = User.query.filter_by(role='teacher').all()
        
        fixed_count = 0
        for user in teachers:
            old_email = user.email
            
            # Fix emails that start with a dot
            if user.email.startswith('.'):
                new_email = user.email[1:]  # Remove leading dot
                user.email = new_email
                fixed_count += 1
                print(f"  Fixed: {old_email} → {new_email}")
            
            # Fix emails with double dots
            elif '..' in user.email:
                new_email = user.email.replace('..', '.')
                user.email = new_email
                fixed_count += 1
                print(f"  Fixed: {old_email} → {new_email}")
        
        if fixed_count > 0:
            db.session.commit()
            print(f"\n✅ Fixed {fixed_count} teacher email addresses")
        else:
            print("\n✓ No email addresses needed fixing")
        
        # Print all teacher emails for verification
        print("\n📧 Current teacher emails:")
        teachers = User.query.filter_by(role='teacher').all()
        for user in teachers:
            print(f"  {user.name}: {user.email}")

if __name__ == '__main__':
    fix_teacher_emails()
