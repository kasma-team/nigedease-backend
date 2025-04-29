import requests
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
import logging
import jwt

logger = logging.getLogger(__name__)

class SimpleUser:
    """
    Simple user class that can hold authentication information.
    """
    def __init__(self, user_id, email):
        self.id = user_id
        self.email = email
        self.is_authenticated = True
        self.is_anonymous = False

class UserManagementJWTAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class that validates JWT tokens directly using JWT_SECRET_KEY
    """
    
    def authenticate(self, request):
        # Get the token from the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            logger.debug("No Authorization header found")
            return None
            
        try:
            # Extract the token
            auth_parts = auth_header.split()
            if len(auth_parts) != 2 or auth_parts[0].lower() != 'bearer':
                logger.debug(f"Invalid Authorization header format: {auth_header}")
                return None
                
            token = auth_parts[1]
            logger.debug(f"Processing token: {token[:10]}...")
            
            # Try to decode the token
            try:
                decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token.get('user_id')
                email = decoded_token.get('email')
                
                if user_id and email:
                    logger.debug(f"Successfully authenticated user {email} with ID {user_id}")
                    # Create a user object from the decoded token
                    user = SimpleUser(user_id, email)
                    return (user, token)
                
                logger.debug("Token missing user_id or email")
                
            except jwt.ExpiredSignatureError:
                logger.debug("Token has expired")
                raise exceptions.AuthenticationFailed('Token has expired')
                
            except jwt.InvalidTokenError as e:
                logger.debug(f"Invalid token: {str(e)}")
                raise exceptions.AuthenticationFailed('Invalid token')
            
            return None
            
        except Exception as e:
            # Handle any other errors
            logger.error(f"Authentication error: {str(e)}")
            raise exceptions.AuthenticationFailed(f'Authentication error: {str(e)}')
    
    def authenticate_header(self, request):
        return 'Bearer' 