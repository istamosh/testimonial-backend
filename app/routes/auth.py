from flask import Blueprint, jsonify
from app.models import User
from app.extensions import db
from app.forms import SignupForm, LoginForm
from app.utils.db_handler import handle_db_operation
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
@handle_db_operation
def signup():
    # Only allow one user
    existing_user = User.query.first()
    if existing_user:
        return jsonify({'error': 'Signup not allowed.'}), 400
    
    form = SignupForm()
    if not form.validate_on_submit():
        return jsonify({'errors': form.errors}), 400
        
    username = form.username.data

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
    if not user or not user.check_password(form.password.data):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Generate access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token
    }), 200
