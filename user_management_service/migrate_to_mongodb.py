import os
import django
import pymongo
from django.conf import settings
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')
django.setup()

# MongoDB connection
mongo_client = pymongo.MongoClient(
    host=settings.DATABASES['default']['CLIENT']['host'],
    port=settings.DATABASES['default']['CLIENT']['port'],
    username=settings.DATABASES['default']['CLIENT']['username'],
    password=settings.DATABASES['default']['CLIENT']['password']
)

# Get database
db = mongo_client[settings.DATABASES['default']['NAME']]

def migrate_users():
    from users.models import User, Role, Permission
    print("Migrating users data...")
    
    # Migrate Permissions
    permissions = Permission.objects.all()
    for permission in permissions:
        db.permissions.insert_one({
            'id': str(permission.id),
            'name': permission.name,
            'codename': permission.codename,
            'description': permission.description,
            'created_at': permission.created_at,
            'updated_at': permission.updated_at
        })
    
    # Migrate Roles
    roles = Role.objects.all()
    for role in roles:
        # Get permissions for this role
        role_permissions = [str(p.id) for p in role.permissions.all()]
        
        db.roles.insert_one({
            'id': str(role.id),
            'name': role.name,
            'description': role.description,
            'permissions': role_permissions,
            'created_at': role.created_at,
            'updated_at': role.updated_at
        })
    
    # Migrate Users
    users = User.objects.all()
    for user in users:
        # Get roles for this user
        user_roles = [str(r.id) for r in user.roles.all()]
        
        db.users.insert_one({
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'password': user.password,  # This is the hashed password
            'roles': user_roles,
            'created_at': user.date_joined,
            'updated_at': user.date_joined
        })

def main():
    print("Starting migration to MongoDB...")
    
    # Create indexes
    db.users.create_index('username', unique=True)
    db.users.create_index('email', unique=True)
    db.roles.create_index('name', unique=True)
    db.permissions.create_index('codename', unique=True)
    
    # Run migrations
    migrate_users()
    
    print("Migration completed successfully!")

if __name__ == '__main__':
    main() 