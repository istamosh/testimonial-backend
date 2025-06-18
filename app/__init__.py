import os
from flask import Flask, jsonify
from .extensions import db, bcrypt, jwt, migrate
from .routes import BLUEPRINTS
from .utils.errors import APIError, NotFoundError, MethodNotAllowedError
from datetime import timedelta

def create_app(config=None):
    app = Flask(__name__)

    # Configure SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', os.environ.get('SECRET_KEY'))
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)
    
    # Cookie-based JWT configuration
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Disable CSRF for API-only usage
    app.config['JWT_COOKIE_SAMESITE'] = 'Strict'

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints with /api prefix
    api_prefix = '/api'
    for blueprint, url_prefix in BLUEPRINTS:
        # Combine /api with the blueprint's specific prefix
        full_prefix = f"{api_prefix}{url_prefix}" if url_prefix else api_prefix
        app.register_blueprint(blueprint, url_prefix=full_prefix)

    # Register error handlers
    @app.errorhandler(APIError)
    def handle_api_error(error):
        return jsonify(error.get_response_dict()), error.code

    @app.errorhandler(404)
    def not_found_error(error):
        return handle_api_error(NotFoundError())

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return handle_api_error(MethodNotAllowedError())

    # Create all database tables
    with app.app_context():
        db.create_all()

    return app