from .auth import auth_bp
from .root import root_bp

BLUEPRINTS = [
    (auth_bp, '/user'),
    (root_bp, '')
]

__all__ = ['BLUEPRINTS']