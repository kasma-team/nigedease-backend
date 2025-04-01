import os
import sys
import uuid
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from core_service.mongodb import db
from product.models import Product, ProductCategory, ProductUnit
from financial.models import Company

def init_db():
    """Initialize the core service database with test data."""
    print("Initializing core service database with test data...")
    
    # Create a default company
    print("Creating company...")
    company_id = str(uuid.uuid4())
    company = Company.create(
        name="Test Company",
        address="123 Test Street",
        email="company@example.com",
        phone_number="+1234567890"
    )
    
    # Create product units
    print("Creating product units...")
    kg_unit = ProductUnit.create(
        company_id=company["id"],
        name="Kilogram",
        description="Weight measurement in kilograms"
    )
    
    liter_unit = ProductUnit.create(
        company_id=company["id"],
        name="Liter",
        description="Volume measurement in liters"
    )

    piece_unit = ProductUnit.create(
        company_id=company["id"],
        name="Piece",
        description="Count measurement in pieces"
    )
    
    # Create product categories
    print("Creating product categories...")
    food_category = ProductCategory.create(
        company_id=company["id"],
        name="Food",
        description="Food products"
    )
    
    electronics_category = ProductCategory.create(
        company_id=company["id"],
        name="Electronics",
        description="Electronic products"
    )
    
    clothing_category = ProductCategory.create(
        company_id=company["id"],
        name="Clothing",
        description="Clothing products"
    )
    
    # Create products
    print("Creating products...")
    products = [
        Product.create(
            company_id=company["id"],
            name="Rice",
            description="Premium rice",
            category_id=food_category["id"],
            unit_id=kg_unit["id"]
        ),
        Product.create(
            company_id=company["id"],
            name="Water",
            description="Mineral water",
            category_id=food_category["id"],
            unit_id=liter_unit["id"]
        ),
        Product.create(
            company_id=company["id"],
            name="Laptop",
            description="High-performance laptop",
            category_id=electronics_category["id"],
            unit_id=piece_unit["id"]
        ),
        Product.create(
            company_id=company["id"],
            name="T-Shirt",
            description="Cotton t-shirt",
            category_id=clothing_category["id"],
            unit_id=piece_unit["id"]
        )
    ]
    
    print(f"Created {len(products)} products")
    print("Database initialization complete!")

if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"Error initializing database: {e}") 