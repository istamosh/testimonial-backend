import os
from flask import Flask
from .extensions import db, bcrypt, jwt, migrate
from .routes import auth_bp, root_bp

def create_app(config=None):
    app = Flask(__name__)

    # Configure SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', os.environ.get('SECRET_KEY'))
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 24 * 60 * 60  # 24 hours

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(root_bp)

    # Create all database tables
    with app.app_context():
        db.create_all()

    return app