from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MaterialViewSet, ColorViewSet, SizeViewSet, SizeChartViewSet,
    SeasonViewSet, CollectionViewSet, ProductVariantViewSet,
    BillOfMaterialsViewSet, BomItemViewSet, ProductionStageViewSet,
    ProductionOrderViewSet, ProductionOrderStageViewSet
)

router = DefaultRouter()
router.register(r'materials', MaterialViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'size-charts', SizeChartViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'collections', CollectionViewSet)
router.register(r'product-variants', ProductVariantViewSet)
router.register(r'bill-of-materials', BillOfMaterialsViewSet)
router.register(r'bom-items', BomItemViewSet)
router.register(r'production-stages', ProductionStageViewSet)
router.register(r'production-orders', ProductionOrderViewSet)
router.register(r'production-order-stages', ProductionOrderStageViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 