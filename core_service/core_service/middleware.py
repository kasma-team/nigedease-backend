from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

class AuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to check if the request has a valid authentication token.
    If token is present, it will be validated against the user management service.
    """
    
    def process_request(self, request):
        # Skip authentication for admin and API docs
        if request.path.startswith('/admin/') or request.path.startswith('/api-docs/') or request.path.startswith('/swagger'):
            return None
            
        # Get the token from the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            # Let the DRF authentication classes handle this
            return None
            
        # Log authentication attempts in debug mode
        if settings.DEBUG:
            logger.debug(f"Authenticating request to {request.path}")
            
        # The actual authentication will be handled by our custom authentication class
        # This middleware is just for logging and potential future enhancements
        return None 