"""
URL configuration for user_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, get_resolver
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Create schema view with proper documentation
schema_view = get_schema_view(
    openapi.Info(
        title="User Management API",
        default_version='v1',
        description="API for user management operations",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def api_root(request):
    return JsonResponse({
        "message": "Welcome to User Management API",
        "endpoints": {
            "users": "/users/",
            "roles": "/roles/",
            "auth": "/auth/login/",
            "documentation": "/api-docs/"
        }
    })

def health_check(request):
    return JsonResponse({"status": "healthy"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),
    path('health/', health_check, name='health-check'),
    
    # Swagger documentation - place before other URLs to avoid collision
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-docs/swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # API endpoints
    path('', include('users.urls')),
]

# Add static file serving
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
