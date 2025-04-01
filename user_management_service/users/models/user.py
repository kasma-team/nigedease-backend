import uuid
from datetime import datetime
from user_management.mongodb import db
from werkzeug.security import generate_password_hash, check_password_hash

# MongoDB Collections
users_collection = db.users

class UserManager:
    @staticmethod
    def create_user(email, password=None, **extra_fields):
        """Create a new user"""
        if not email:
            raise ValueError('The Email field must be set')
        
        # Check if user with this email already exists
        if users_collection.find_one({"email": email}):
            raise ValueError(f'User with email {email} already exists')
        
        # Create new user document
        user = {
            "id": str(uuid.uuid4()),
            "email": email.lower(),
            "password": generate_password_hash(password) if password else None,
            "first_name": extra_fields.get('first_name', ''),
            "last_name": extra_fields.get('last_name', ''),
            "company_id": extra_fields.get('company_id'),
            "role_id": extra_fields.get('role_id'),
            "phone_number": extra_fields.get('phone_number'),
            "profile_image": extra_fields.get('profile_image', ''),
            "is_active": extra_fields.get('is_active', True),
            "is_staff": extra_fields.get('is_staff', False),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        users_collection.insert_one(user)
        return user
    
    @staticmethod
    def create_superuser(email, password=None, **extra_fields):
        """Create a new superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('company_id', str(uuid.uuid4()))
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
            
        return UserManager.create_user(email, password, **extra_fields)

class User:
    objects = UserManager()
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        return users_collection.find_one({"id": user_id})
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        return users_collection.find_one({"email": email.lower()})
    
    @staticmethod
    def get_all():
        """Get all users"""
        return list(users_collection.find().sort("created_at", -1))
    
    @staticmethod
    def update(user_id, data):
        """Update a user"""
        data["updated_at"] = datetime.utcnow()
        
        # Handle password updates separately with hashing
        if "password" in data and data["password"]:
            data["password"] = generate_password_hash(data["password"])
            
        users_collection.update_one({"id": user_id}, {"$set": data})
        return users_collection.find_one({"id": user_id})
    
    @staticmethod
    def delete(user_id):
        """Delete a user"""
        users_collection.delete_one({"id": user_id})
    
    @staticmethod
    def check_password(user_document, password):
        """Check if the provided password matches the user's password"""
        if not user_document or not user_document.get("password"):
            return False
        return check_password_hash(user_document["password"], password) 