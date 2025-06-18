from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.db_handler import handle_db_operation
from app.models import PreservedTestimonial, Testimonial
from app.forms import PreservedTestimonialForm, TestimonialForm
from app.extensions import db
from datetime import datetime, timezone

root_bp = Blueprint('root', __name__)

@root_bp.route('/')
@handle_db_operation
def home():
    return 'Hello from testimonial-backend!'

@root_bp.route('/request-form', methods=['POST'])
@jwt_required()
@handle_db_operation
def request_form():
    # Get current user's ID from JWT token
    current_user_id = get_jwt_identity()

    # Initialize and validate form
    form = PreservedTestimonialForm(meta={'csrf': False})
    if not form.validate_on_submit():
        return jsonify({'errors': form.errors}), 400

    # Create new preserved testimonial
    preserved = PreservedTestimonial(
        name=form.name.data,
        user_id=current_user_id
    )
    db.session.add(preserved)
    db.session.commit()

    return jsonify({
        'message': 'Form request created successfully',
        'access_uuid': preserved.access_uuid
    }), 201

@root_bp.route('/testimonial', methods=['POST'])
@handle_db_operation
def submit_testimonial():
    # Get JSON data
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    # Initialize and validate form with JSON data
    form = TestimonialForm(meta={'csrf': False}, data=data)
    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    # Create new testimonial
    testimonial = Testimonial(
        first_name=data['first_name'],
        last_name=data['last_name'],
        role_company=data.get('role_company'),  # Optional field
        profile_link=data['profile_link'],  # Required field
        testimonial=data['testimonial'],
        censor_first_name=data.get('censor_first_name', False),
        censor_last_name=data.get('censor_last_name', False),
        consent_given=data['consent_given'],
        status='PENDING'  # Default status
    )
    
    db.session.add(testimonial)
    db.session.commit()

    return jsonify({
        'message': 'Testimonial submitted successfully',
        'status': 'PENDING',
        'createdAt': testimonial.created_at.isoformat() + 'Z'
    }), 201
