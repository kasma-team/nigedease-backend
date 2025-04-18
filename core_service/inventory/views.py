from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import models
import requests

from .models import Store, Inventory, Material
from .serializers import StoreSerializer, InventorySerializer, MaterialSerializer

class VerifyTokenPermission(IsAuthenticated):
    def has_permission(self, request, view):
        request.company_id = "72527190-f935-4f91-be61-ae11c50b9fcb" # Default company_id for testing
        return True
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token: 
            return False
        response = requests.post(
            'http://127.0.0.1:8000/api/auth/verify-token/',  # User Management Service
            json={'token': token},
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            data = response.json()
            request.company_id = data.get('company_id')  # Set company_id from token
            if not request.company_id:
                raise PermissionDenied("No company_id in token")
            return True
        return False

class StoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing stores.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('store_type', openapi.IN_QUERY, 
                             description="Filter by store type", 
                             type=openapi.TYPE_STRING,
                             enum=['retail', 'warehouse', 'factory']),
        ]
    )
    def list(self, request, *args, **kwargs):
        store_type = request.query_params.get('store_type')
        queryset = self.get_queryset()
        
        if store_type:
            queryset = queryset.filter(store_type=store_type)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        # Filter by company_id from the token
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        # Save with company_id from the token
        serializer.save(company_id=self.request.company_id)

class InventoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing inventory.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('store_id', openapi.IN_QUERY, 
                             description="Filter by store ID", 
                             type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            openapi.Parameter('product_id', openapi.IN_QUERY, 
                             description="Filter by product ID", 
                             type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            openapi.Parameter('product_variant_id', openapi.IN_QUERY, 
                             description="Filter by product variant ID", 
                             type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            openapi.Parameter('low_stock', openapi.IN_QUERY, 
                             description="Filter by low stock (quantity below min_stock_level)", 
                             type=openapi.TYPE_BOOLEAN),
        ]
    )
    def list(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id')
        product_id = request.query_params.get('product_id')
        product_variant_id = request.query_params.get('product_variant_id')
        low_stock = request.query_params.get('low_stock')
        
        queryset = self.get_queryset()
        
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        if product_variant_id:
            queryset = queryset.filter(product_variant_id=product_variant_id)
        
        if low_stock and low_stock.lower() == 'true':
            queryset = queryset.filter(quantity__lt=models.F('min_stock_level'))
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        # Filter by company_id from the token using the store relationship
        return self.queryset.filter(store__company_id=self.request.company_id)

    def perform_create(self, serializer):
        serializer.save()

class MaterialViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing materials.
    """
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('material_type', openapi.IN_QUERY, 
                             description="Filter by material type", 
                             type=openapi.TYPE_STRING,
                             enum=['fabric', 'thread', 'button', 'zipper', 'elastic', 'trim', 'lining', 'interfacing', 'other']),
        ]
    )
    def list(self, request, *args, **kwargs):
        material_type = request.query_params.get('material_type')
        queryset = self.get_queryset()
        
        if material_type:
            queryset = queryset.filter(material_type=material_type)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        # Filter by company_id from the token
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        # Save with company_id from the token
        serializer.save(company_id=self.request.company_id)