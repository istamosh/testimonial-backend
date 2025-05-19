from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db, jwt
from app.forms import SignupForm, LoginForm
from app.utils.db_handler import handle_db_operation
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
@handle_db_operation
def signup():
    form = SignupForm()
    if not form.validate_on_submit():
        return jsonify({'errors': form.errors}), 400
        
    username = form.username.data

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    try:
        # Create new user
        new_user = User(username=username)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except:
        db.session.rollback()
        raise

@auth_bp.route('/login', methods=['POST'])
@handle_db_operation
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        return jsonify({'errors': form.errors}), 400

    # Find user by username
    user = User.query.filter_by(username=form.username.data).first()
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    # Check password
    if not user.check_password(form.password.data):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Generate access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token
    }), 200
