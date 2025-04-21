from rest_framework import viewsets
from .models import (
    Material, Color, Size, SizeChart, Season, Collection,
    ProductVariant, BillOfMaterials, BomItem, ProductionStage,
    ProductionOrder, ProductionOrderStage
)
from .serializers import (
    MaterialSerializer, ColorSerializer, SizeSerializer, SizeChartSerializer,
    SeasonSerializer, CollectionSerializer, ProductVariantSerializer,
    BillOfMaterialsSerializer, BomItemSerializer, ProductionStageSerializer,
    ProductionOrderSerializer, ProductionOrderStageSerializer
)

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class SizeChartViewSet(viewsets.ModelViewSet):
    queryset = SizeChart.objects.all()
    serializer_class = SizeChartSerializer

class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

class BillOfMaterialsViewSet(viewsets.ModelViewSet):
    queryset = BillOfMaterials.objects.all()
    serializer_class = BillOfMaterialsSerializer

class BomItemViewSet(viewsets.ModelViewSet):
    queryset = BomItem.objects.all()
    serializer_class = BomItemSerializer

class ProductionStageViewSet(viewsets.ModelViewSet):
    queryset = ProductionStage.objects.all()
    serializer_class = ProductionStageSerializer

class ProductionOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrder.objects.all()
    serializer_class = ProductionOrderSerializer

class ProductionOrderStageViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrderStage.objects.all()
    serializer_class = ProductionOrderStageSerializer 