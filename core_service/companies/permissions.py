from rest_framework.permissions import BasePermission
import requests
from django.conf import settings

class IsSuperAdmin(BasePermission):
    """
    Custom permission that allows all authenticated users (temporarily replacing role-based access)
    """
    def has_permission(self, request, view):
        # Temporarily allowing all authenticated users
        return True

class HasRole(BasePermission):
    """
    Custom permission to check if a user has a specific role.
    """
    def __init__(self, role_name):
        self.role_name = role_name
        
    def has_permission(self, request, view):
        # Check the role directly from the authenticated user
        return (
            hasattr(request.user, 'role') and 
            request.user.role == self.role_name
        )

class IsAdmin(BasePermission):
    """
    Permission to only allow admin users to access.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'Admin'

class IsSales(BasePermission):
    """
    Permission to only allow sales users to access.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'Sales'

class IsStockManager(BasePermission):
    """
    Permission to only allow stock manager users to access.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'Stock Manager' 