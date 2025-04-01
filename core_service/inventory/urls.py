from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, InventoryViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet, basename='store')
router.register(r'inventory', InventoryViewSet, basename='inventory')

urlpatterns = [
    path('', include(router.urls)),
]