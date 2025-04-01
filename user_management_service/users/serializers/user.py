from rest_framework import serializers
from users.models.user import User
from users.models.role import Role
from users.serializers.role import RoleSerializer

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False)
    is_active = serializers.BooleanField(default=True)
    role = serializers.CharField(required=False)
    role_name = serializers.CharField(read_only=True, required=False)
    company = serializers.CharField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_login = serializers.DateTimeField(read_only=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create a new user"""
        return User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            company_id=validated_data.get('company'),
            role_id=validated_data.get('role'),
            phone_number=validated_data.get('phone_number'),
            profile_image=validated_data.get('profile_image', ''),
            is_active=validated_data.get('is_active', True),
            is_staff=validated_data.get('is_staff', False)
        )

    def update(self, instance, validated_data):
        """Update an existing user"""
        # If the instance is a MongoDB document
        user_id = instance.get('id')
        return User.update(user_id, validated_data) 