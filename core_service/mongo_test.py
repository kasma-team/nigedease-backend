import pymongo
import os
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import pprint

# Load environment variables
load_dotenv()

# MongoDB connection details
mongo_host = os.getenv('MONGO_HOST', 'localhost')
mongo_port = int(os.getenv('MONGO_PORT', 27017))
mongo_db = os.getenv('MONGO_DB', 'core_service_db')
mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/{mongo_db}"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[mongo_db]

# Print database info
print(f"Connected to MongoDB: {mongo_uri}")
print(f"Available collections: {db.list_collection_names()}")

# Create test data
def create_test_data():
    current_time = datetime.datetime.utcnow()
    
    # Create a company
    company = {
        "id": "test-company-id",
        "name": "Test Company",
        "address": "123 Test Street",
        "email": "test@example.com",
        "phone_number": "+1234567890",
        "created_at": current_time,
        "updated_at": current_time
    }
    
    # Check if the company already exists
    if db.companies.count_documents({"id": "test-company-id"}) == 0:
        db.companies.insert_one(company)
        print("Created test company")
    else:
        print("Test company already exists")
    
    # Create a product category
    category = {
        "id": "test-category-id",
        "company_id": "test-company-id",
        "name": "Test Category",
        "description": "A test category",
        "created_at": current_time,
        "updated_at": current_time
    }
    
    # Check if the category already exists
    if db.product_categories.count_documents({"id": "test-category-id"}) == 0:
        db.product_categories.insert_one(category)
        print("Created test product category")
    else:
        print("Test product category already exists")
    
    # Create a product unit
    unit = {
        "id": "test-unit-id",
        "company_id": "test-company-id",
        "name": "Test Unit",
        "description": "A test unit",
        "created_at": current_time,
        "updated_at": current_time
    }
    
    # Check if the unit already exists
    if db.product_units.count_documents({"id": "test-unit-id"}) == 0:
        db.product_units.insert_one(unit)
        print("Created test product unit")
    else:
        print("Test product unit already exists")
    
    # Create a product
    product = {
        "id": "test-product-id",
        "company_id": "test-company-id",
        "name": "Test Product",
        "description": "A test product",
        "category_id": "test-category-id",
        "unit_id": "test-unit-id",
        "created_at": current_time,
        "updated_at": current_time
    }
    
    # Check if the product already exists
    if db.products.count_documents({"id": "test-product-id"}) == 0:
        db.products.insert_one(product)
        print("Created test product")
    else:
        print("Test product already exists")

# Function to test collections
def print_collection_data(collection_name):
    collection = db[collection_name]
    count = collection.count_documents({})
    print(f"\n{collection_name} collection: {count} documents")
    
    if count > 0:
        print(f"First document in {collection_name}:")
        first_doc = collection.find_one({})
        pprint.pprint(first_doc)

# Create test data
create_test_data()

# Test company collection
print_collection_data("companies")

# Test product collections
print_collection_data("product_categories")
print_collection_data("product_units")
print_collection_data("products")

print("\nMongoDB test completed successfully!") 