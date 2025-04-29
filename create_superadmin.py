#!/usr/bin/env python
import os
import django
import uuid

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')
django.setup()

from users.models.user import User
from users.models.role import Role
from django.contrib.auth.hashers import make_password

def create_superadmin():
    """Create a super admin user"""
    # Get the Superadmin role
    superadmin_role = Role.objects.get(name='Superadmin')
    
    # Create the super admin user
    user, created = User.objects.get_or_create(
        email='superadmin@example.com',
        defaults={
            'id': uuid.uuid4(),
            'company_id': uuid.uuid4(),
            'first_name': 'Super',
            'last_name': 'Admin',
            'password': make_password('superadmin123'),
            'role': superadmin_role,
            'is_staff': True
        }
    )
    
    if created:
        print("Super admin user created successfully!")
        print(f"Email: {user.email}")
        print("Password: superadmin123")
    else:
        print("Super admin user already exists!")
        print(f"Email: {user.email}")

if __name__ == "__main__":
    create_superadmin() 