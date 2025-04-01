import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)

def get_mongodb_client():
    """
    Create and return a MongoDB client connection based on environment variables.
    """
    mongo_host = os.getenv('MONGO_HOST', 'localhost')
    mongo_port = int(os.getenv('MONGO_PORT', 27017))
    mongo_user = os.getenv('MONGO_USER', '')
    mongo_password = os.getenv('MONGO_PASSWORD', '')
    mongo_db = os.getenv('MONGO_DB', 'user_management_db')
    
    # Build connection string
    if mongo_user and mongo_password:
        connection_string = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}"
    else:
        connection_string = f"mongodb://{mongo_host}:{mongo_port}/{mongo_db}"
    
    try:
        client = MongoClient(connection_string)
        # The ismaster command is cheap and does not require auth
        client.admin.command('ismaster')
        logger.info("MongoDB connection successful")
        return client
    except ConnectionFailure as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise

# Create a MongoDB client instance
mongo_client = get_mongodb_client()
db = mongo_client[os.getenv('MONGO_DB', 'user_management_db')] 