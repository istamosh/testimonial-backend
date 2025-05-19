from flask import Blueprint
from app.utils.db_handler import handle_db_operation

root_bp = Blueprint('root', __name__)

@root_bp.route('/')
@handle_db_operation
def home():
    return 'Hello from testimonial-backend!'
