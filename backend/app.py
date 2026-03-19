from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from config import Config
from models import db, User
import os

# Initialize cache
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Cache configuration
    app.config['CACHE_TYPE'] = 'SimpleCache'  # Use 'RedisCache' for production
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes default
    
    # CORS Configuration - Allow Vercel frontend and Railway
    # Must be configured before registering blueprints
    CORS(app, 
         resources={
             r"/*": {
                 "origins": [
                     "http://localhost:3000",
                     "http://localhost:5000", 
                     "http://localhost:5173",
                     "https://student-performance-system-kohl.vercel.app",
                     "https://student-performance-system-soulsayss-projects.vercel.app",
                     "https://*.railway.app"  # Allow Railway domains
                 ],
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                 "allow_headers": ["Content-Type", "Authorization"],
                 "supports_credentials": True,
                 "expose_headers": ["Content-Type", "Authorization"]
             }
         }
    )
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    cache.init_app(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.teacher import teacher_bp
    from routes.parent import parent_bp
    from routes.admin import admin_bp
    from routes.ml import ml_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(student_bp, url_prefix='/api/student')
    app.register_blueprint(teacher_bp, url_prefix='/api/teacher')
    app.register_blueprint(parent_bp, url_prefix='/api/parent')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(ml_bp, url_prefix='/api/ml')
    
    # Create database tables and auto-seed on first deployment
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
        
        # Fix teacher emails if needed (one-time fix for existing data)
        try:
            teachers = User.query.filter_by(role='teacher').all()
            fixed_count = 0
            for user in teachers:
                if user.email.startswith('.') or '..' in user.email:
                    old_email = user.email
                    # Remove leading dots
                    new_email = user.email.lstrip('.')
                    # Fix double dots
                    new_email = new_email.replace('..', '.')
                    user.email = new_email
                    fixed_count += 1
                    print(f"  Fixed teacher email: {old_email} → {new_email}")
            
            if fixed_count > 0:
                db.session.commit()
                print(f"✅ Fixed {fixed_count} teacher email addresses")
        except Exception as e:
            print(f"⚠️ Email fix check: {str(e)}")
        
        # Auto-seed database on first deployment (only if empty)
        try:
            user_count = User.query.count()
            
            # Check for force reseed environment variable
            force_reseed = os.getenv('FORCE_RESEED', 'false').lower() == 'true'
            
            if user_count <= 1 or force_reseed:  # Empty or only admin OR force reseed
                if force_reseed:
                    print("\n" + "="*60)
                    print("FORCE RESEED ENABLED - DROPPING ALL TABLES")
                    print("="*60)
                    db.drop_all()
                    db.create_all()
                
                print("\n" + "="*60)
                print("DATABASE IS EMPTY - RUNNING AUTO-SEED SCRIPT")
                print("="*60)
                
                # Import and run seed script
                from utils.seed_database import seed_all_data
                seed_all_data()
                
                print("\n✅ Auto-seeding completed successfully!")
            else:
                print(f"✓ Database already populated with {user_count} users. Skipping seed.")
                print(f"💡 To force reseed, set environment variable: FORCE_RESEED=true")
        except Exception as e:
            print(f"⚠️ Database initialization: {str(e)}")
            print("Note: You can manually seed the database using:")
            print("  python utils/seed_database.py")
    
    @app.route('/')
    def index():
        return {'message': 'Student Academic Performance System API', 'status': 'running'}
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    @app.route('/api/health', methods=['GET'])
    def api_health():
        """Health check endpoint for frontend"""
        try:
            # Test database connection
            user_count = User.query.count()
            return {
                'status': 'ok',
                'message': 'Backend is running',
                'database': 'connected',
                'total_users': user_count
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Backend error',
                'database': 'disconnected',
                'error': str(e)
            }, 500
    
    @app.route('/api/debug/users', methods=['GET'])
    def debug_users():
        """Debug endpoint to show sample users (for development only)"""
        try:
            students = User.query.filter_by(role='student').limit(5).all()
            parents = User.query.filter_by(role='parent').limit(5).all()
            teachers = User.query.filter_by(role='teacher').limit(5).all()
            
            return {
                'sample_students': [{'email': s.email, 'name': s.name} for s in students],
                'sample_parents': [{'email': p.email, 'name': p.name} for p in parents],
                'sample_teachers': [{'email': t.email, 'name': t.name} for t in teachers],
                'total_users': {
                    'students': User.query.filter_by(role='student').count(),
                    'parents': User.query.filter_by(role='parent').count(),
                    'teachers': User.query.filter_by(role='teacher').count(),
                    'admins': User.query.filter_by(role='admin').count()
                }
            }, 200
        except Exception as e:
            return {
                'error': str(e)
            }, 500
    
    @app.route('/api/admin/reset-database', methods=['POST'])
    def reset_database():
        """
        DANGER: Reset entire database and reseed
        Requires special secret key for security
        """
        from flask import request
        
        # Security check - require secret key
        secret = request.headers.get('X-Reset-Secret')
        if secret != 'RESET_DB_2026_SECURE':
            return {'success': False, 'message': 'Unauthorized'}, 401
        
        try:
            # Drop all tables
            db.drop_all()
            # Recreate tables
            db.create_all()
            
            # Seed with new data
            from utils.seed_database import seed_all_data
            seed_all_data()
            
            # Verify
            user_count = User.query.count()
            
            return {
                'success': True,
                'message': 'Database reset and reseeded successfully',
                'total_users': user_count
            }, 200
        except Exception as e:
            return {
                'success': False,
                'message': 'Failed to reset database',
                'error': str(e)
            }, 500
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'success': False, 'message': 'Internal server error'}, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'success': False, 'message': 'Bad request'}, 400
    
    return app

# Create app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
