from rest_framework import serializers
from .models import Store, Inventory, Material
from product.serializers import ProductSerializer
from product.models import ProductVariant

class MaterialSerializer(serializers.ModelSerializer):
    company_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Material
        fields = ['id', 'company', 'name', 'description', 'material_type', 
                 'properties', 'unit_of_measure', 'created_at', 'updated_at', 'company_id']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']

    def validate_company_id(self, value):
        from financial.models import Company
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value

class StoreSerializer(serializers.ModelSerializer):
    company_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Store
        fields = ['id', 'company', 'name', 'location', 'store_type', 
                 'created_at', 'updated_at', 'company_id']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']

    def validate_company_id(self, value):
        from financial.models import Company
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value

class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    store = StoreSerializer(read_only=True)
    store_id = serializers.UUIDField(write_only=True)
    product_variant_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_id', 'product_variant_id', 
                 'store', 'store_id', 'quantity', 'min_stock_level', 'max_stock_level',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_product_id(self, value):
        from product.models import Product
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Product with id {value} does not exist.")
        return value

    def validate_store_id(self, value):
        if not Store.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Store with id {value} does not exist.")
        return value
    
    def validate_product_variant_id(self, value):
        if value and not ProductVariant.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Product Variant with id {value} does not exist.")
        return value

