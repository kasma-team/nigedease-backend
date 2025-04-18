from rest_framework import serializers
from .models import (
    ProductUnit, ProductCategory, Product, 
    Season, Collection, Color, Size, SizeChart,
    ProductVariant
)

class ProductUnitSerializer(serializers.ModelSerializer):
    company_id = serializers.UUIDField(write_only=True)  # Add this to accept company_id directly

    class Meta:
        model = ProductUnit
        fields = ['id', 'company', 'name', 'description', 'created_at', 'updated_at', 'company_id']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']  # company is read-only, set via company_id

    def validate_company_id(self, value):
        from financial.models import Company
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value

class SizeChartSerializer(serializers.ModelSerializer):
    company_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = SizeChart
        fields = ['id', 'company', 'name', 'category', 'chart_data', 
                 'created_at', 'updated_at', 'company_id']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']

    def validate_company_id(self, value):
        from financial.models import Company
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value

class SeasonSerializer(serializers.ModelSerializer):
    company_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Season
        fields = ['id', 'company', 'name', 'start_date', 'end_date', 
                 'description', 'created_at', 'updated_at', 'company_id']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']

    def validate_company_id(self, value):
        from financial.models import Company
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value

class CollectionSerializer(serializers.ModelSerializer):
    company_id = serializers.UUIDField(write_only=True)
    season = SeasonSerializer(read_only=True)
    season_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Collection
        fields = ['id', 'company', 'name', 'description', 'release_date',
                 'is_active', 'season', 'season_id', 'created_at', 'updated_at', 'company_id']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']

    def validate_company_id(self, value):
        from financial.models import Company
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value
    
    def validate_season_id(self, value):
        if value and not Season.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Season with id {value} does not exist.")
        return value

class ProductCategorySerializer(serializers.ModelSerializer):
    company_id = serializers.UUIDField(write_only=True, required=False)  # Make it optional
    parent_category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all(), required=False, allow_null=True)
    size_chart = SizeChartSerializer(read_only=True)
    size_chart_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'company', 'name', 'description', 'parent_category',
                 'size_chart', 'size_chart_id', 'created_at', 'updated_at', 'company_id']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']  # company is read-only, set via company_id

    def validate_company_id(self, value):
        from financial.models import Company
        if value and not Company.objects.filter(id=value).exists():  # Only validate if provided
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value
    
    def validate_size_chart_id(self, value):
        if value and not SizeChart.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Size Chart with id {value} does not exist.")
        return value

class ColorSerializer(serializers.ModelSerializer):
    company_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Color
        fields = ['id', 'company', 'name', 'color_code', 'is_active', 
                 'created_at', 'updated_at', 'company_id']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']

    def validate_company_id(self, value):
        from financial.models import Company
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value

class SizeSerializer(serializers.ModelSerializer):
    company_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Size
        fields = ['id', 'company', 'name', 'description', 'category',
                 'measurement_unit', 'measurements', 'created_at', 'updated_at', 'company_id']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']

    def validate_company_id(self, value):
        from financial.models import Company
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    unit = ProductUnitSerializer(read_only=True)
    unit_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    company_id = serializers.UUIDField(write_only=True)  # Add this to accept company_id directly
    collection = CollectionSerializer(read_only=True)
    collection_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'company', 'name', 'description', 'category', 'category_id', 
                 'unit', 'unit_id', 'sku', 'barcode', 'cost_price', 'retail_price',
                 'wholesale_price', 'gender', 'weight', 'weight_unit', 'is_featured',
                 'image', 'image_urls', 'metadata', 'collection', 'collection_id',
                 'created_at', 'updated_at', 'company_id']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']  # company is read-only, set via company_id

    def validate_company_id(self, value):
        from financial.models import Company
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value
    
    def validate_category_id(self, value):
        if value and not ProductCategory.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Product Category with id {value} does not exist.")
        return value
    
    def validate_unit_id(self, value):
        if value and not ProductUnit.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Product Unit with id {value} does not exist.")
        return value
    
    def validate_collection_id(self, value):
        if value and not Collection.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Collection with id {value} does not exist.")
        return value

class ProductVariantSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    size = SizeSerializer(read_only=True)
    size_id = serializers.UUIDField(write_only=True)
    color = ColorSerializer(read_only=True)
    color_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'product_id', 'size', 'size_id', 'color', 'color_id',
                 'sku', 'barcode', 'additional_cost', 'weight', 'dimensions', 'image_url',
                 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Product with id {value} does not exist.")
        return value
    
    def validate_size_id(self, value):
        if not Size.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Size with id {value} does not exist.")
        return value
    
    def validate_color_id(self, value):
        if not Color.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Color with id {value} does not exist.")
        return value