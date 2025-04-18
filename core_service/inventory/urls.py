from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, InventoryViewSet, MaterialViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'inventories', InventoryViewSet)
router.register(r'materials', MaterialViewSet)

urlpatterns = [
    path('', include(router.urls)),
]