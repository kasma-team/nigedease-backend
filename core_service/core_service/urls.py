from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TestAuthView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            "message": "Authentication successful",
            "user_id": getattr(request.user, 'id', None),
            "email": getattr(request.user, 'email', None)
        })

schema_view = get_schema_view(
    openapi.Info(
        title="Core Service API",
        default_version='v1',
        description="API documentation for Core Service. For user management endpoints, please use the User Management API at http://localhost:8000/api-docs/",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path('transactions/', include('transactions.urls')),
        path('financials/', include('financials.urls')),
        path('companies/', include('companies.urls')),
        path('inventory/', include('inventory.urls')),
        path('clothing/', include('clothing.urls')),
        path('test-auth/', TestAuthView.as_view()),
    ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Swagger UI endpoints
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('docs.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Legacy Swagger endpoints
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # API Endpoints
    path('transactions/', include('transactions.urls')),
    path('financials/', include('financials.urls')),
    path('companies/', include('companies.urls')),
    path('inventory/', include('inventory.urls')),
    path('clothing/', include('clothing.urls')),
    
    # Test Authentication
    path('test-auth/', TestAuthView.as_view(), name='test-auth'),
]