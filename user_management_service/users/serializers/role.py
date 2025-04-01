from rest_framework import serializers
from ..models.role import Role, Permission, RolePermission

class PermissionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True) 
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

class RolePermissionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    role_id = serializers.CharField()
    permission_id = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

class RoleSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    permissions = PermissionSerializer(many=True, required=False)

    def create(self, validated_data):
        permission_ids = validated_data.pop('permission_ids', [])
        role = Role.objects.create(**validated_data)
        
        # Add permissions
        if permission_ids:
            permissions = Permission.objects.filter(id__in=permission_ids)
            RolePermission.objects.bulk_create([
                RolePermission(role=role, permission=permission)
                for permission in permissions
            ])
        
        return role

    def update(self, instance, validated_data):
        permission_ids = validated_data.pop('permission_ids', None)
        
        # Update role fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update permissions if provided
        if permission_ids is not None:
            # Clear existing permissions
            RolePermission.objects.filter(role=instance).delete()
            
            # Add new permissions
            if permission_ids:
                permissions = Permission.objects.filter(id__in=permission_ids)
                RolePermission.objects.bulk_create([
                    RolePermission(role=instance, permission=permission)
                    for permission in permissions
                ])

        return instance 