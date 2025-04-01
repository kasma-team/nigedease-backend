"""
URL configuration for core_service project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings

# Create a basic view for API health check
class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

# Create a basic view for API root
class ApiRootView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            "message": "Welcome to Core Service API",
            "version": "1.0",
            "endpoints": {
                "financial": "/financial/",
                "product": "/product/",
                "inventory": "/inventory/",
                "documentation": "/api-docs/"
            }
        }, status=status.HTTP_200_OK)

# Create schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Core Service API",
        default_version='1.0',
        description="API for core business operations",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path('financial/', include('financial.urls')),
        path('product/', include('product.urls')),
        path('inventory/', include('inventory.urls')),
    ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ApiRootView.as_view(), name='api-root'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # API documentation
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-docs/swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # App URLs
    path('financial/', include('financial.urls')),
    path('product/', include('product.urls')),
    path('inventory/', include('inventory.urls')),
]

# Add static file serving
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)