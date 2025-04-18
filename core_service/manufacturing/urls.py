from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BillOfMaterialsViewSet, BOMItemViewSet, ProductionStageViewSet,
    ProductionOrderViewSet, ProductionOrderStageViewSet
)

router = DefaultRouter()
router.register(r'boms', BillOfMaterialsViewSet)
router.register(r'bom-items', BOMItemViewSet)
router.register(r'production-stages', ProductionStageViewSet)
router.register(r'production-orders', ProductionOrderViewSet)
router.register(r'production-order-stages', ProductionOrderStageViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 