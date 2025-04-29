from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


<<<<<<< Updated upstream

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    
    path('api-docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-swagger-ui'),
    path('swagger.json', SpectacularAPIView.as_view(), name='schema'),
    
    # API Endpoints
    path('transactions/', include('transactions.urls')),
    path('financials/', include('financials.urls')),
    path('companies/', include('companies.urls')),
    path('inventory/', include('inventory.urls')),
    path('clothings/', include('clothings.urls')),
=======
schema_view = get_schema_view(
    openapi.Info(
        title="Core Service API",
        default_version='v1',
        description="API for managing companies, transactions, and more",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('companies/', include('companies.urls')),
    path('inventory/', include('inventory.urls')),
    path('transactions/', include('transactions.urls')),
    path('financials/', include('financials.urls')),
    path('clothing/', include('clothing.urls')),
    path('test-auth/', TestAuthView.as_view(), name='test-auth'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
>>>>>>> Stashed changes
]