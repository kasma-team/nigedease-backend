from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    """Generate tokens for user"""
    refresh = RefreshToken.for_user(user)
    
    # Add user information to token payload
    refresh['email'] = user.email
    refresh['user_id'] = str(user.id)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    } 