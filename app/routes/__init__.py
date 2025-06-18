from .auth import auth_bp
from .root import root_bp
from .admin import admin_bp

BLUEPRINTS = [
    (auth_bp, '/user'),
    (root_bp, ''),
    (admin_bp, '/admin')
]

__all__ = ['BLUEPRINTS']