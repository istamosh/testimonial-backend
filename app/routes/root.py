from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.db_handler import handle_db_operation
from app.models import PreservedTestimonial
from app.forms.preserved_testimonial_form import PreservedTestimonialForm
from app.extensions import db

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
