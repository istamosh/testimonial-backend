from werkzeug.exceptions import HTTPException

class APIError(HTTPException):
    """Base error class for our API exceptions"""
    code = 500
    error_type = "Internal Server Error"
    
    def __init__(self, message=None):
        super().__init__()
        self.message = message or self.description

    def get_response_dict(self):
        return {
            'error': self.error_type,
            'message': self.message
        }

class NotFoundError(APIError):
    code = 404
    error_type = "Not Found"
    description = "The requested URL was not found on the server."

class MethodNotAllowedError(APIError):
    code = 405
    error_type = "Method Not Allowed"
    description = "The method is not allowed for the requested URL."
