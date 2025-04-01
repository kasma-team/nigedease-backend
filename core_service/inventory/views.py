from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from pymongo import MongoClient
from bson import ObjectId
from django.conf import settings
import requests
from .serializers import StoreSerializer, InventorySerializer

# Base class for MongoDB ViewSets
class MongoDBViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    collection_name = None
    serializer_class = None
    
    def get_db(self):
        client = MongoClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_NAME]
        return db
    
    def get_collection(self):
        db = self.get_db()
        return db[self.collection_name]
    
    def get_queryset(self):
        collection = self.get_collection()
        company_id = self.get_company_id()
        if company_id:
            return collection.find({"company_id": company_id})
        return collection.find()
    
    def get_company_id(self):
        """Get the company ID associated with the request token"""
        token = self.request.headers.get('Authorization', '').split(' ')[-1]
        if not token:
            return None
            
        # Call user management service to get the user's company
        try:
            response = requests.get(
                f"{settings.USER_MANAGEMENT_SERVICE_URL}/api/users/me/",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                user_data = response.json()
                return user_data.get('company_id')
        except Exception as e:
            print(f"Error getting company ID: {e}")
        
        # Return a default company ID for testing
        return "72527190-f935-4f91-be61-ae11c50b9fcb"
    
    def list(self, request):
        queryset = self.get_queryset()
        # Convert MongoDB documents to list and serialize
        items = list(queryset)
        for item in items:
            if '_id' in item:
                item['id'] = str(item['_id'])
                del item['_id']
        
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            collection = self.get_collection()
            item = collection.find_one({"_id": ObjectId(pk)})
            if not item:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
                
            # Check company association
            company_id = self.get_company_id()
            if company_id and item.get('company_id') != company_id:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
                
            # Convert ObjectId to string
            item['id'] = str(item['_id'])
            del item['_id']
            
            serializer = self.serializer_class(item)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Add company ID if available
            company_id = self.get_company_id()
            if company_id:
                data['company_id'] = company_id
                
            # Insert into MongoDB
            collection = self.get_collection()
            result = collection.insert_one(data)
            
            # Return the created object
            created_item = collection.find_one({"_id": result.inserted_id})
            created_item['id'] = str(created_item['_id'])
            del created_item['_id']
            
            return Response(self.serializer_class(created_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        try:
            collection = self.get_collection()
            item = collection.find_one({"_id": ObjectId(pk)})
            if not item:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
                
            # Check company association
            company_id = self.get_company_id()
            if company_id and item.get('company_id') != company_id:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(data=request.data, partial=True)
            if serializer.is_valid():
                data = serializer.validated_data
                
                # Don't allow changing company_id
                if 'company_id' in data and data['company_id'] != item.get('company_id'):
                    return Response({"detail": "Cannot change company_id"}, status=status.HTTP_400_BAD_REQUEST)
                
                # Update in MongoDB
                collection.update_one({"_id": ObjectId(pk)}, {"$set": data})
                
                # Return the updated object
                updated_item = collection.find_one({"_id": ObjectId(pk)})
                updated_item['id'] = str(updated_item['_id'])
                del updated_item['_id']
                
                return Response(self.serializer_class(updated_item).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            collection = self.get_collection()
            item = collection.find_one({"_id": ObjectId(pk)})
            if not item:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
                
            # Check company association
            company_id = self.get_company_id()
            if company_id and item.get('company_id') != company_id:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            
            # Delete from MongoDB
            collection.delete_one({"_id": ObjectId(pk)})
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StoreViewSet(MongoDBViewSet):
    collection_name = 'store'
    serializer_class = StoreSerializer

class InventoryViewSet(MongoDBViewSet):
    collection_name = 'inventory'
    serializer_class = InventorySerializer
    
    def list(self, request):
        # Special handling for inventory to get inventory across all stores
        company_id = self.get_company_id()
        
        if not company_id:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get stores
        db = self.get_db()
        stores = list(db.store.find({"company_id": company_id}))
        store_ids = [str(store['_id']) for store in stores]
        
        # Get inventory for these stores
        collection = self.get_collection()
        items = list(collection.find({"store_id": {"$in": store_ids}}))
        
        # Process IDs for serialization
        for item in items:
            if '_id' in item:
                item['id'] = str(item['_id'])
                del item['_id']
                
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)