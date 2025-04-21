import requests
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import AnonymousUser
import logging

logger = logging.getLogger(__name__)

class UserManagementJWTAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class that validates JWT tokens against the user management service.
    """
    
    def authenticate(self, request):
        # Get the token from the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
            
        try:
            # Extract the token
            auth_parts = auth_header.split()
            if len(auth_parts) != 2 or auth_parts[0].lower() != 'bearer':
                return None
                
            token = auth_parts[1]
            
            # Validate token with user management service
            verify_url = f"{settings.USER_MANAGEMENT_SERVICE_URL}/auth/verify-token/"
            logger.debug(f"Calling verify-token at {verify_url} with token: {token}")
            response = requests.post(
                verify_url,
                json={"token": token},
                timeout=5  # 5 seconds timeout
            )
            # Debug output for token verification
            print(f"[CORE_AUTH] verify-token URL: {verify_url}")
            print(f"[CORE_AUTH] Response status: {response.status_code}")
            print(f"[CORE_AUTH] Response body: {response.text}")
            logger.debug(f"verify-token response status: {response.status_code}, body: {response.text}")
            
            if response.status_code != 200:
                raise exceptions.AuthenticationFailed(
                    f'Invalid token or token expired (status {response.status_code})'
                )
                
            # Extract user info from response
            user_data = response.json()
            if not user_data.get('is_valid'):
                raise exceptions.AuthenticationFailed('Invalid token')
                
            # Create a user object from the response
            user = AnonymousUser()
            user.id = user_data.get('user_id')
            user.email = user_data.get('email')
            user.is_authenticated = True
            
            # Return the user and token
            return (user, token)
            
        except requests.RequestException as e:
            # Handle connection errors with user management service
            raise exceptions.AuthenticationFailed(f'Error communicating with authentication service: {str(e)}')
        except Exception as e:
            # Handle any other errors
            raise exceptions.AuthenticationFailed(f'Authentication error: {str(e)}')
    
    def authenticate_header(self, request):
        return 'Bearer' 