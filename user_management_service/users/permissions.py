from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    """
    Permission to only allow superadmin users to access.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated and has the Superadmin role
        return request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role and request.user.role.name == 'Superadmin'

class IsAdmin(BasePermission):
    """
    Permission to only allow admin users to access.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated and has the Admin role
        return request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role and request.user.role.name == 'Admin'

class IsSales(BasePermission):
    """
    Permission to only allow sales users to access.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated and has the Sales role
        return request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role and request.user.role.name == 'Sales'

class IsStockManager(BasePermission):
    """
    Permission to only allow stock manager users to access.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated and has the Stock Manager role
        return request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role and request.user.role.name == 'Stock Manager'

class HasRolePermission(BasePermission):
    """
    Permission to check if a user has a specific permission.
    """
    def __init__(self, required_permission):
        self.required_permission = required_permission
        
    def has_permission(self, request, view):
        # Check if user is authenticated and has the required permission
        if not request.user.is_authenticated or not hasattr(request.user, 'role') or not request.user.role:
            return False
            
        return request.user.role.has_permission(self.required_permission) 