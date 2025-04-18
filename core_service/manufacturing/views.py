from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import BillOfMaterials, BOMItem, ProductionStage, ProductionOrder, ProductionOrderStage
from .serializers import (
    BillOfMaterialsSerializer, BOMItemSerializer, ProductionStageSerializer,
    ProductionOrderSerializer, ProductionOrderStageSerializer
)
import requests
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

class BillOfMaterialsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Bills of Materials.
    """
    queryset = BillOfMaterials.objects.all()
    serializer_class = BillOfMaterialsSerializer
    permission_classes = [VerifyTokenPermission]

    def get_queryset(self):
        # Filter by company_id from the token
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        # Save with company_id from the token
        serializer.save(company_id=self.request.company_id)

class BOMItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Bill of Materials Items.
    """
    queryset = BOMItem.objects.all()
    serializer_class = BOMItemSerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('bom_id', openapi.IN_QUERY, 
                              description="Filter by Bill of Materials ID", 
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID)
        ]
    )
    def list(self, request, *args, **kwargs):
        bom_id = request.query_params.get('bom_id')
        queryset = self.queryset
        
        if bom_id:
            queryset = queryset.filter(bom_id=bom_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

class ProductionStageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Production Stages.
    """
    queryset = ProductionStage.objects.all()
    serializer_class = ProductionStageSerializer
    permission_classes = [VerifyTokenPermission]

    def get_queryset(self):
        # Filter by company_id from the token
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        # Save with company_id from the token
        serializer.save(company_id=self.request.company_id)

class ProductionOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Production Orders.
    """
    queryset = ProductionOrder.objects.all()
    serializer_class = ProductionOrderSerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, 
                              description="Filter by production order status", 
                              type=openapi.TYPE_STRING,
                              enum=['draft', 'scheduled', 'in_progress', 'completed', 'cancelled']),
            openapi.Parameter('product_id', openapi.IN_QUERY, 
                              description="Filter by product ID", 
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID)
        ]
    )
    def list(self, request, *args, **kwargs):
        status = request.query_params.get('status')
        product_id = request.query_params.get('product_id')
        
        queryset = self.get_queryset()
        
        if status:
            queryset = queryset.filter(status=status)
        
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        # Filter by company_id from the token
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        # Save with company_id from the token
        serializer.save(company_id=self.request.company_id)

class ProductionOrderStageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Production Order Stages.
    """
    queryset = ProductionOrderStage.objects.all()
    serializer_class = ProductionOrderStageSerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('production_order_id', openapi.IN_QUERY, 
                              description="Filter by Production Order ID", 
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            openapi.Parameter('status', openapi.IN_QUERY, 
                              description="Filter by stage status", 
                              type=openapi.TYPE_STRING,
                              enum=['pending', 'in_progress', 'completed', 'skipped'])
        ]
    )
    def list(self, request, *args, **kwargs):
        production_order_id = request.query_params.get('production_order_id')
        status = request.query_params.get('status')
        
        queryset = self.queryset
        
        if production_order_id:
            queryset = queryset.filter(production_order_id=production_order_id)
        
        if status:
            queryset = queryset.filter(status=status)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save() 