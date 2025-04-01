import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import pprint

# Load environment variables
load_dotenv()

# MongoDB connection details
mongo_host = os.getenv('MONGO_HOST', 'localhost')
mongo_port = int(os.getenv('MONGO_PORT', 27017))
mongo_db = os.getenv('MONGO_DB', 'user_management_db')
mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/{mongo_db}"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[mongo_db]

# Print database info
print(f"Connected to MongoDB: {mongo_uri}")
print(f"Available collections: {db.list_collection_names()}")

# Function to test collections
def print_collection_data(collection_name):
    collection = db[collection_name]
    count = collection.count_documents({})
    print(f"\n{collection_name} collection: {count} documents")
    
    if count > 0:
        print(f"First document in {collection_name}:")
        first_doc = collection.find_one({})
        pprint.pprint(first_doc)

# Test users collection
print_collection_data("users")

# Test roles collection
print_collection_data("roles")

# Test permissions collection
print_collection_data("permissions")

# Test role_permissions collection
print_collection_data("role_permissions")

print("\nMongoDB test completed successfully!") 