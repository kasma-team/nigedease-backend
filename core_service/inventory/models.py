import uuid
import datetime
from core_service.mongodb import db
from financial.models import Company  # Import Company from Financial app
from product.models import Product    # Import Product from Product app

class Store:
    @staticmethod
    def create(company_id, name, location=None):
        """Create a new store"""
        store = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "name": name,
            "location": location,
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow()
        }
        
        db.stores.insert_one(store)
        return store
    
    @staticmethod
    def get_by_id(store_id):
        """Get store by ID"""
        return db.stores.find_one({"id": store_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all stores for a company"""
        return list(db.stores.find({"company_id": company_id}).sort("name", 1))
    
    @staticmethod
    def update(store_id, data):
        """Update a store"""
        data["updated_at"] = datetime.datetime.utcnow()
        db.stores.update_one({"id": store_id}, {"$set": data})
        return db.stores.find_one({"id": store_id})
    
    @staticmethod
    def delete(store_id):
        """Delete a store"""
        db.stores.delete_one({"id": store_id})

class Inventory:
    @staticmethod
    def create(product_id, store_id, quantity):
        """Create a new inventory entry"""
        # Check if inventory already exists for this product and store
        existing = db.inventory.find_one({"product_id": product_id, "store_id": store_id})
        if existing:
            # Update quantity if it exists
            existing["quantity"] = quantity
            existing["updated_at"] = datetime.datetime.utcnow()
            db.inventory.update_one({"id": existing["id"]}, {"$set": existing})
            return existing
        
        # Create new inventory entry
        inventory = {
            "id": str(uuid.uuid4()),
            "product_id": product_id,
            "store_id": store_id,
            "quantity": quantity,
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow()
        }
        
        db.inventory.insert_one(inventory)
        return inventory
    
    @staticmethod
    def get_by_id(inventory_id):
        """Get inventory by ID"""
        return db.inventory.find_one({"id": inventory_id})
    
    @staticmethod
    def get_by_product_store(product_id, store_id):
        """Get inventory for a product in a store"""
        return db.inventory.find_one({"product_id": product_id, "store_id": store_id})
    
    @staticmethod
    def get_by_store(store_id):
        """Get all inventory for a store"""
        return list(db.inventory.find({"store_id": store_id}))
    
    @staticmethod
    def get_by_product(product_id):
        """Get all inventory for a product"""
        return list(db.inventory.find({"product_id": product_id}))
    
    @staticmethod
    def update(inventory_id, data):
        """Update inventory"""
        data["updated_at"] = datetime.datetime.utcnow()
        db.inventory.update_one({"id": inventory_id}, {"$set": data})
        return db.inventory.find_one({"id": inventory_id})
    
    @staticmethod
    def delete(inventory_id):
        """Delete inventory"""
        db.inventory.delete_one({"id": inventory_id})