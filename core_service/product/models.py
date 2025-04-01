import uuid
from datetime import datetime
from core_service.mongodb import db

# MongoDB Collections
product_units = db.product_units
product_categories = db.product_categories
products = db.products

class ProductUnit:
    @staticmethod
    def create(company_id, name, description=None):
        """Create a new product unit"""
        product_unit = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "name": name,
            "description": description,
            "created_at": datetime.utcnow()
        }
        product_units.insert_one(product_unit)
        return product_unit
    
    @staticmethod
    def get_by_id(unit_id):
        """Get product unit by ID"""
        return product_units.find_one({"id": unit_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all product units for a company"""
        return list(product_units.find({"company_id": company_id}))
    
    @staticmethod
    def update(unit_id, data):
        """Update a product unit"""
        product_units.update_one({"id": unit_id}, {"$set": data})
        return product_units.find_one({"id": unit_id})
    
    @staticmethod
    def delete(unit_id):
        """Delete a product unit"""
        product_units.delete_one({"id": unit_id})

class ProductCategory:
    @staticmethod
    def create(company_id, name, description=None):
        """Create a new product category"""
        category = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "name": name,
            "description": description,
            "created_at": datetime.utcnow()
        }
        product_categories.insert_one(category)
        return category
    
    @staticmethod
    def get_by_id(category_id):
        """Get product category by ID"""
        return product_categories.find_one({"id": category_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all product categories for a company"""
        return list(product_categories.find({"company_id": company_id}))
    
    @staticmethod
    def update(category_id, data):
        """Update a product category"""
        product_categories.update_one({"id": category_id}, {"$set": data})
        return product_categories.find_one({"id": category_id})
    
    @staticmethod
    def delete(category_id):
        """Delete a product category"""
        product_categories.delete_one({"id": category_id})

class Product:
    @staticmethod
    def create(company_id, name, description=None, category_id=None, unit_id=None):
        """Create a new product"""
        product = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "name": name,
            "description": description,
            "category_id": category_id,
            "unit_id": unit_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        products.insert_one(product)
        return product
    
    @staticmethod
    def get_by_id(product_id):
        """Get product by ID"""
        return products.find_one({"id": product_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all products for a company"""
        return list(products.find({"company_id": company_id}))
    
    @staticmethod
    def update(product_id, data):
        """Update a product"""
        data["updated_at"] = datetime.utcnow()
        products.update_one({"id": product_id}, {"$set": data})
        return products.find_one({"id": product_id})
    
    @staticmethod
    def delete(product_id):
        """Delete a product"""
        products.delete_one({"id": product_id})