from rest_framework import serializers

class StoreSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255, required=False, allow_null=True)
    company_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

class InventorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    product_id = serializers.CharField()
    store_id = serializers.CharField()
    quantity = serializers.IntegerField(min_value=0)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Read-only nested objects
    product = serializers.SerializerMethodField()
    store = serializers.SerializerMethodField()
    
    def get_product(self, obj):
        from pymongo import MongoClient
        from django.conf import settings
        from bson import ObjectId
        
        # Get product details from MongoDB
        if 'product_id' in obj:
            try:
                client = MongoClient(settings.MONGODB_URI)
                db = client[settings.MONGODB_NAME]
                product = db.product.find_one({"_id": ObjectId(obj['product_id'])})
                if product:
                    return {
                        'id': str(product['_id']),
                        'name': product['name'],
                        'description': product.get('description', '')
                    }
            except Exception as e:
                print(f"Error getting product: {e}")
        return None
    
    def get_store(self, obj):
        from pymongo import MongoClient
        from django.conf import settings
        from bson import ObjectId
        
        # Get store details from MongoDB
        if 'store_id' in obj:
            try:
                client = MongoClient(settings.MONGODB_URI)
                db = client[settings.MONGODB_NAME]
                store = db.store.find_one({"_id": ObjectId(obj['store_id'])})
                if store:
                    return {
                        'id': str(store['_id']),
                        'name': store['name'],
                        'location': store.get('location', '')
                    }
            except Exception as e:
                print(f"Error getting store: {e}")
        return None

