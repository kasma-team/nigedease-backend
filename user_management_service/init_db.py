import os
import sys
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from users.models.user import User, UserManager
from users.models.role import Role, Permission, RolePermission

def init_db():
    """Initialize the database with test data."""
    print("Initializing database with test data...")
    
    # Create default permissions
    print("Creating permissions...")
    view_users_perm = Permission.create("view_users", "Can view users")
    create_users_perm = Permission.create("create_users", "Can create users")
    update_users_perm = Permission.create("update_users", "Can update users")
    delete_users_perm = Permission.create("delete_users", "Can delete users")

    # Create default roles
    print("Creating roles...")
    admin_role = Role.create("Admin", "Administrator with full access")
    user_role = Role.create("User", "Regular user with limited access")
    
    # Assign permissions to roles
    print("Assigning permissions to roles...")
    admin_role_id = admin_role["id"]
    user_role_id = user_role["id"]

    # Assign all permissions to admin
    for perm in [view_users_perm, create_users_perm, update_users_perm, delete_users_perm]:
        RolePermission.create(admin_role_id, perm["id"])
    
    # Assign view permission to user role
    RolePermission.create(user_role_id, view_users_perm["id"])
    
    # Create default company
    company_id = str(uuid.uuid4())

    # Create users
    print("Creating users...")
    admin_user = User.objects.create_user(
        email="admin@example.com",
        password="admin123",
        first_name="Admin",
        last_name="User",
        company_id=company_id,
        role_id=admin_role_id,
        is_staff=True
    )
    
    regular_user = User.objects.create_user(
        email="user@example.com",
        password="user123",
        first_name="Regular",
        last_name="User",
        company_id=company_id,
        role_id=user_role_id
    )
    
    print(f"Created admin user: {admin_user['email']}")
    print(f"Created regular user: {regular_user['email']}")
    print("Database initialization complete!")

if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"Error initializing database: {e}") 