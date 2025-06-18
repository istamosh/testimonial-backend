from flask import Blueprint, jsonify, request
from app.models import User, Testimonial
from app.extensions import db
from app.utils.db_handler import handle_db_operation
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/testimonials', methods=['GET'])
@jwt_required()
@handle_db_operation
def get_all_testimonials():
    """Get all testimonials for admin dashboard"""
    # Verify user is authenticated
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'Unauthorized'}), 401

    # Get all testimonials
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    
    testimonials_data = []
    for testimonial in testimonials:
        testimonials_data.append({
            'id': testimonial.id,
            'name': f"{testimonial.first_name} {testimonial.last_name}",
            'first_name': testimonial.first_name,
            'last_name': testimonial.last_name,
            'role_company': testimonial.role_company or '',
            'profile_link': testimonial.profile_link or '',
            'testimonial': testimonial.testimonial,
            'status': testimonial.status,
            'censor_first_name': testimonial.censor_first_name,
            'censor_last_name': testimonial.censor_last_name,
            'consent_given': testimonial.consent_given,
            'created_at': testimonial.created_at.isoformat(),
            'approved_at': testimonial.approved_at.isoformat() if testimonial.approved_at else None
        })
    
    return jsonify(testimonials_data), 200

@admin_bp.route('/testimonials/<int:testimonial_id>', methods=['PATCH'])
@jwt_required()
@handle_db_operation
def update_testimonial_status(testimonial_id):
    """Update testimonial status (approve/reject)"""
    # Verify user is authenticated
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'Unauthorized'}), 401

    # Get testimonial
    testimonial = Testimonial.query.get(testimonial_id)
    if not testimonial:
        return jsonify({'message': 'Testimonial not found'}), 404

    # Get new status from request
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'message': 'Status is required'}), 400

    new_status = data['status'].upper()
    if new_status not in ['APPROVED', 'REJECTED', 'PENDING']:
        return jsonify({'message': 'Invalid status. Must be APPROVED, REJECTED, or PENDING'}), 400

    try:
        # Update testimonial status
        testimonial.status = new_status
        
        # Set approved_at timestamp if approving, clear it if retracting to pending or rejecting
        if new_status == 'APPROVED':
            from datetime import datetime, timezone
            testimonial.approved_at = datetime.now(timezone.utc)
        elif new_status in ['REJECTED', 'PENDING']:
            testimonial.approved_at = None
            
        db.session.commit()
        
        return jsonify({
            'message': f'Testimonial {new_status.lower()} successfully',
            'testimonial': {
                'id': testimonial.id,
                'status': new_status,
                'approved_at': testimonial.approved_at.isoformat() if testimonial.approved_at else None
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update testimonial'}), 500

@admin_bp.route('/testimonials/approved', methods=['GET'])
@handle_db_operation
def get_approved_testimonials():
    """Get approved testimonials for public display"""
    # Get only approved testimonials
    approved_testimonials = Testimonial.query.filter_by(status='APPROVED').order_by(Testimonial.created_at.desc()).all()
    
    testimonials_data = []
    for testimonial in approved_testimonials:
        # Handle name censoring
        display_first_name = testimonial.first_name[0] + '*' * (len(testimonial.first_name) - 1) if testimonial.censor_first_name else testimonial.first_name
        display_last_name = testimonial.last_name[0] + '*' * (len(testimonial.last_name) - 1) if testimonial.censor_last_name else testimonial.last_name
        
        testimonials_data.append({
            'id': testimonial.id,
            'name': f"{display_first_name} {display_last_name}",
            'role_company': testimonial.role_company or '',
            'profile_link': testimonial.profile_link or '',
            'testimonial': testimonial.testimonial,
            'created_at': testimonial.created_at.isoformat()
        })
    
    return jsonify(testimonials_data), 200
