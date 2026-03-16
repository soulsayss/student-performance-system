from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from config import Config
from models import db
import os

# Initialize cache
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Cache configuration
    app.config['CACHE_TYPE'] = 'SimpleCache'  # Use 'RedisCache' for production
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes default
    
    # CORS Configuration - Allow multiple origins
    cors_origins = [
        'http://localhost:3000',           # Local development
        'http://localhost:5000',           # Local backend
        'https://*.vercel.app',            # Vercel deployments
    ]
    
    # Add production frontend URL if set
    production_frontend = os.environ.get('PRODUCTION_FRONTEND_URL')
    if production_frontend:
        cors_origins.append(production_frontend)
    
    CORS(app, origins=cors_origins, supports_credentials=True)
    
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
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    @app.route('/')
    def index():
        return {'message': 'Student Academic Performance System API', 'status': 'running'}
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
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

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
