from rest_framework import serializers
from .models import (
    Material, Color, Size, SizeChart, Season, Collection,
    ProductVariant, BillOfMaterials, BomItem, ProductionStage,
    ProductionOrder, ProductionOrderStage
)

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class SizeChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeChart
        fields = '__all__'

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'

class BillOfMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillOfMaterials
        fields = '__all__'

class BomItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BomItem
        fields = '__all__'

class ProductionStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionStage
        fields = '__all__'

class ProductionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrder
        fields = '__all__'

class ProductionOrderStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrderStage
        fields = '__all__' 