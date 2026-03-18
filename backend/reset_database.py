"""
Database Reset Script - Can be triggered via API endpoint
"""
from app import create_app, db
from models import User
from utils.seed_database import seed_all_data

def reset_and_reseed():
    """Drop all tables, recreate them, and reseed with fresh data"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("⚠️  DATABASE RESET INITIATED")
        print("="*60)
        
        # Drop all tables
        print("\n🗑️  Dropping all tables...")
        db.drop_all()
        print("✅ All tables dropped")
        
        # Recreate tables
        print("\n🔨 Creating fresh tables...")
        db.create_all()
        print("✅ Tables created")
        
        # Seed with new data
        print("\n🌱 Seeding database with new data...")
        seed_all_data()
        
        # Verify
        user_count = User.query.count()
        print(f"\n✅ Database reset complete!")
        print(f"📊 Total users: {user_count}")
        print("="*60 + "\n")
        
        return True

if __name__ == '__main__':
    reset_and_reseed()
