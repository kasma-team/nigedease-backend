import uuid
from datetime import datetime
from user_management.mongodb import db

# MongoDB Collections
permissions_collection = db.permissions
roles_collection = db.roles
role_permissions_collection = db.role_permissions

class Permission:
    @staticmethod
    def create(name, description=""):
        """Create a new permission"""
        # Check if permission with this name already exists
        if permissions_collection.find_one({"name": name}):
            raise ValueError(f'Permission with name {name} already exists')
            
        permission = {
            "id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        permissions_collection.insert_one(permission)
        return permission
    
    @staticmethod
    def get_by_id(permission_id):
        """Get permission by ID"""
        return permissions_collection.find_one({"id": permission_id})
    
    @staticmethod
    def get_by_name(name):
        """Get permission by name"""
        return permissions_collection.find_one({"name": name})
    
    @staticmethod
    def get_all():
        """Get all permissions"""
        return list(permissions_collection.find().sort("name", 1))
    
    @staticmethod
    def update(permission_id, data):
        """Update a permission"""
        data["updated_at"] = datetime.utcnow()
        permissions_collection.update_one({"id": permission_id}, {"$set": data})
        return permissions_collection.find_one({"id": permission_id})
    
    @staticmethod
    def delete(permission_id):
        """Delete a permission"""
        permissions_collection.delete_one({"id": permission_id})
        # Also delete any role_permission records
        role_permissions_collection.delete_many({"permission_id": permission_id})

class Role:
    @staticmethod
    def create(name, description="", permissions=None):
        """Create a new role"""
        # Check if role with this name already exists
        if roles_collection.find_one({"name": name}):
            raise ValueError(f'Role with name {name} already exists')
            
        role = {
            "id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        roles_collection.insert_one(role)
        
        # Add permissions if provided
        if permissions:
            for permission_id in permissions:
                RolePermission.create(role["id"], permission_id)
                
        return role
    
    @staticmethod
    def get_by_id(role_id):
        """Get role by ID"""
        return roles_collection.find_one({"id": role_id})
    
    @staticmethod
    def get_by_name(name):
        """Get role by name"""
        return roles_collection.find_one({"name": name})
    
    @staticmethod
    def get_all():
        """Get all roles"""
        return list(roles_collection.find().sort("name", 1))
    
    @staticmethod
    def update(role_id, data):
        """Update a role"""
        data["updated_at"] = datetime.utcnow()
        roles_collection.update_one({"id": role_id}, {"$set": data})
        return roles_collection.find_one({"id": role_id})
    
    @staticmethod
    def delete(role_id):
        """Delete a role"""
        roles_collection.delete_one({"id": role_id})
        # Also delete any role_permission records
        role_permissions_collection.delete_many({"role_id": role_id})
    
    @staticmethod
    def get_permissions(role_id):
        """Get all permissions for a role"""
        role_permissions = role_permissions_collection.find({"role_id": role_id})
        permission_ids = [rp["permission_id"] for rp in role_permissions]
        return list(permissions_collection.find({"id": {"$in": permission_ids}}))
    
    @staticmethod
    def has_permission(role_id, permission_name):
        """Check if role has a specific permission"""
        permission = permissions_collection.find_one({"name": permission_name})
        if not permission:
            return False
            
        return role_permissions_collection.find_one({
            "role_id": role_id,
            "permission_id": permission["id"]
        }) is not None

class RolePermission:
    @staticmethod
    def create(role_id, permission_id):
        """Create a new role-permission association"""
        # Check if association already exists
        if role_permissions_collection.find_one({
            "role_id": role_id, 
            "permission_id": permission_id
        }):
            return
            
        role_permission = {
            "id": str(uuid.uuid4()),
            "role_id": role_id,
            "permission_id": permission_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        role_permissions_collection.insert_one(role_permission)
        return role_permission
    
    @staticmethod
    def delete(role_id, permission_id):
        """Delete a role-permission association"""
        role_permissions_collection.delete_one({
            "role_id": role_id,
            "permission_id": permission_id
        }) 