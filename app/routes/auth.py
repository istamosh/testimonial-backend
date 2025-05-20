from flask import Blueprint, jsonify
from app.models import User
from app.extensions import db
from app.forms import SignupForm, LoginForm, UpdateUserForm
from app.utils.db_handler import handle_db_operation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('', methods=['POST'])  # Changed from /signup to empty string (matches /user from blueprint prefix)
@handle_db_operation
def create_user():  # Renamed from signup to create_user
    # Only allow one user
    existing_user = User.query.first()
    if existing_user:
        return jsonify({'error': 'User creation not allowed.'}), 400
    
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

@auth_bp.route('', methods=['PUT'])
@jwt_required()
@handle_db_operation
def update_user():
    form = UpdateUserForm()
    if not form.validate_on_submit():
        return jsonify({'errors': form.errors}), 400

    # Get current user
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Verify current password
    if not user.check_password(form.current_password.data):
        return jsonify({'error': 'Current password is incorrect'}), 401

    try:
        # Update username if provided
        if form.username.data:
            user.username = form.username.data

        # Update password if provided
        if form.new_password.data:
            user.set_password(form.new_password.data)

        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
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
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token
    }), 200
