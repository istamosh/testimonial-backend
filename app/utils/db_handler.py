from functools import wraps
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def handle_db_operation(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except IntegrityError as e:
            # Handle specific database integrity errors (like unique constraint violations)
            return jsonify({'error': 'Database integrity error', 'message': str(e.orig)}), 400
        except SQLAlchemyError as e:
            # Handle general SQLAlchemy errors
            return jsonify({'error': 'Database error', 'message': str(e)}), 500
        except Exception as e:
            # Handle any other unexpected errors
            return jsonify({'error': 'An unexpected error occurred', 'message': str(e)}), 500
        
    return decorated_function
