from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests

from .models import (
    ProductUnit, ProductCategory, Product,
    Season, Collection, Color, Size, SizeChart,
    ProductVariant
)
from .serializers import (
    ProductUnitSerializer, ProductCategorySerializer, ProductSerializer,
    SeasonSerializer, CollectionSerializer, ColorSerializer, SizeSerializer,
    SizeChartSerializer, ProductVariantSerializer
)

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

class ProductUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product units.
    """
    queryset = ProductUnit.objects.all()
    serializer_class = ProductUnitSerializer
    permission_classes = [VerifyTokenPermission]

    def get_queryset(self):
        # Filter by company_id from the token
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        # Save with company_id from the token
        serializer.save(company_id=self.request.company_id)
         
class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product categories.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('parent_id', openapi.IN_QUERY, 
                              description="Filter by parent category ID", 
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
        ]
    )
    def list(self, request, *args, **kwargs):
        parent_id = request.query_params.get('parent_id')
        queryset = self.get_queryset()
        
        if parent_id:
            if parent_id.lower() == 'null':
                queryset = queryset.filter(parent_category__isnull=True)
            else:
                queryset = queryset.filter(parent_category_id=parent_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        # Always use company_id from token, ignoring payload company_id
        serializer.save(company_id=self.request.company_id)

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category_id', openapi.IN_QUERY, 
                              description="Filter by category ID", 
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            openapi.Parameter('collection_id', openapi.IN_QUERY, 
                              description="Filter by collection ID", 
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            openapi.Parameter('gender', openapi.IN_QUERY, 
                              description="Filter by gender", 
                              type=openapi.TYPE_STRING,
                              enum=['men', 'women', 'unisex', 'children']),
            openapi.Parameter('is_featured', openapi.IN_QUERY, 
                              description="Filter by featured status", 
                              type=openapi.TYPE_BOOLEAN),
        ]
    )
    def list(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id')
        collection_id = request.query_params.get('collection_id')
        gender = request.query_params.get('gender')
        is_featured = request.query_params.get('is_featured')
        
        queryset = self.get_queryset()
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        if collection_id:
            queryset = queryset.filter(collection_id=collection_id)
        
        if gender:
            queryset = queryset.filter(gender=gender)
        
        if is_featured is not None:
            is_featured_bool = is_featured.lower() == 'true'
            queryset = queryset.filter(is_featured=is_featured_bool)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        # Filter by company_id from the token
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        # Save with company_id from the token
        serializer.save(company_id=self.request.company_id)

class SizeChartViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing size charts.
    """
    queryset = SizeChart.objects.all()
    serializer_class = SizeChartSerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, 
                              description="Filter by category", 
                              type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category')
        queryset = self.get_queryset()
        
        if category:
            queryset = queryset.filter(category=category)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        serializer.save(company_id=self.request.company_id)

class SeasonViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing seasons.
    """
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [VerifyTokenPermission]

    def get_queryset(self):
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        serializer.save(company_id=self.request.company_id)

class CollectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing collections.
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('season_id', openapi.IN_QUERY, 
                              description="Filter by season ID", 
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            openapi.Parameter('is_active', openapi.IN_QUERY, 
                              description="Filter by active status", 
                              type=openapi.TYPE_BOOLEAN),
        ]
    )
    def list(self, request, *args, **kwargs):
        season_id = request.query_params.get('season_id')
        is_active = request.query_params.get('is_active')
        
        queryset = self.get_queryset()
        
        if season_id:
            queryset = queryset.filter(season_id=season_id)
        
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        serializer.save(company_id=self.request.company_id)

class ColorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing colors.
    """
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, 
                              description="Filter by active status", 
                              type=openapi.TYPE_BOOLEAN),
        ]
    )
    def list(self, request, *args, **kwargs):
        is_active = request.query_params.get('is_active')
        
        queryset = self.get_queryset()
        
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        serializer.save(company_id=self.request.company_id)

class SizeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing sizes.
    """
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, 
                              description="Filter by category", 
                              type=openapi.TYPE_STRING,
                              enum=['men', 'women', 'children', 'unisex']),
        ]
    )
    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category')
        
        queryset = self.get_queryset()
        
        if category:
            queryset = queryset.filter(category=category)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset.filter(company_id=self.request.company_id)

    def perform_create(self, serializer):
        serializer.save(company_id=self.request.company_id)

class ProductVariantViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product variants.
    """
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [VerifyTokenPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_QUERY, 
                              description="Filter by product ID", 
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            openapi.Parameter('size_id', openapi.IN_QUERY, 
                              description="Filter by size ID", 
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            openapi.Parameter('color_id', openapi.IN_QUERY, 
                              description="Filter by color ID", 
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            openapi.Parameter('is_active', openapi.IN_QUERY, 
                              description="Filter by active status", 
                              type=openapi.TYPE_BOOLEAN),
        ]
    )
    def list(self, request, *args, **kwargs):
        product_id = request.query_params.get('product_id')
        size_id = request.query_params.get('size_id')
        color_id = request.query_params.get('color_id')
        is_active = request.query_params.get('is_active')
        
        queryset = self.queryset
        
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        if size_id:
            queryset = queryset.filter(size_id=size_id)
        
        if color_id:
            queryset = queryset.filter(color_id=color_id)
        
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()