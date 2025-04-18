from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductUnitViewSet, ProductCategoryViewSet, ProductViewSet,
    SeasonViewSet, CollectionViewSet, ColorViewSet, SizeViewSet,
    SizeChartViewSet, ProductVariantViewSet
)

router = DefaultRouter()
router.register(r'units', ProductUnitViewSet)
router.register(r'categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sizecharts', SizeChartViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'collections', CollectionViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'variants', ProductVariantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]