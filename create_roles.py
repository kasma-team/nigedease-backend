#!/usr/bin/env python
import os
import django
import uuid

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')
django.setup()

from users.models.role import Role, Permission

def create_permission(name, description=None):
    """Create a permission if it doesn't exist"""
    if description is None:
        description = f"Allows {name}"
    
    permission, created = Permission.objects.get_or_create(
        name=name,
        defaults={"description": description}
    )
    
    if created:
        print(f"Created permission: {name}")
    
    return permission

def create_role(name, description, permissions):
    """Create a role with the given permissions"""
    role, created = Role.objects.get_or_create(
        name=name,
        defaults={
            "id": uuid.uuid4(),
            "description": description
        }
    )
    
    # Clear existing permissions and add new ones
    if not created:
        role.permissions.clear()
        print(f"Updated existing role: {name}")
    else:
        print(f"Created new role: {name}")
    
    # Add permissions
    role.permissions.add(*permissions)
    print(f"Added {len(permissions)} permissions to {name}")
    
    return role

def setup_roles():
    """Set up all roles and permissions"""
    print("Setting up permissions...")
    
    # Common permissions
    view_dashboard = create_permission("view_dashboard", "Allows viewing the dashboard")
    
    # Sales role permissions
    manage_sales = create_permission("manage_sales", "Allows creating and managing sales")
    view_customers = create_permission("view_customers", "Allows viewing customer information")
    process_payments = create_permission("process_payments", "Allows processing payments")
    
    # Stock Manager permissions
    manage_inventory = create_permission("manage_inventory", "Allows managing inventory levels")
    track_stock = create_permission("track_stock", "Allows tracking stock movements")
    manage_suppliers = create_permission("manage_suppliers", "Allows managing suppliers")
    
    # Admin permissions (these already exist but let's ensure they're there)
    manage_users = create_permission("manage_users", "Allows managing user accounts")
    view_reports = create_permission("view_reports", "Allows viewing reports")
    edit_settings = create_permission("edit_settings", "Allows editing system settings")
    
    # Superadmin additional permissions
    system_config = create_permission("system_config", "Allows configuring system-wide settings")
    manage_roles = create_permission("manage_roles", "Allows managing roles and permissions")
    
    print("\nSetting up roles...")
    
    # Create Sales role
    create_role(
        "Sales",
        "Sales staff responsible for managing sales and customers",
        [manage_sales, view_customers, process_payments, view_dashboard]
    )
    
    # Create Stock Manager role
    create_role(
        "Stock Manager",
        "Staff responsible for managing inventory and stock",
        [manage_inventory, track_stock, manage_suppliers, view_dashboard]
    )
    
    # Create Admin role (should already exist but let's ensure it has the right permissions)
    create_role(
        "Admin",
        "Administrator with management access",
        [manage_users, view_reports, edit_settings, view_dashboard]
    )
    
    # Create Superadmin role
    create_role(
        "Superadmin",
        "Super administrator with full system access",
        [
            manage_users, view_reports, edit_settings,
            manage_sales, view_customers, process_payments,
            manage_inventory, track_stock, manage_suppliers,
            system_config, manage_roles, view_dashboard
        ]
    )
    
    print("\nRole setup complete!")

if __name__ == "__main__":
    setup_roles() 