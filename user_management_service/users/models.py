from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model that inherits from Django's AbstractUser
    
    This model exists to satisfy Django's AUTH_USER_MODEL setting,
    but the actual user data is stored in MongoDB collections
    as defined in users/models/user.py
    """
    # Add any custom fields needed
    
    class Meta:
        # This tells Django this model exists in the DB
        # even though we're using MongoDB
        managed = False 