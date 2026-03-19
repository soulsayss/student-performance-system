"""
Force reseed script - manually drops and recreates database
Run this when database is locked
"""
import os
import sys

# Delete database file
db_path = 'instance/student_academic.db'
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print(f"✓ Deleted {db_path}")
    except Exception as e:
        print(f"✗ Could not delete {db_path}: {e}")
        print("Please close any programs accessing the database and try again")
        sys.exit(1)

# Now run seed script
print("\nRunning seed script...")
os.system('python utils/seed_database.py')
