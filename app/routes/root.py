from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.db_handler import handle_db_operation
from app.models import Testimonial
from app.forms import TestimonialForm
from app.extensions import db
from datetime import datetime, timezone

root_bp = Blueprint('root', __name__)

@root_bp.route('/')
@handle_db_operation
def home():
    return 'Hello from testimonial-backend!'

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
