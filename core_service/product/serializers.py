from rest_framework import serializers

class ProductUnitSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company_id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

class ProductCategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company_id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company_id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_null=True)
    category_id = serializers.CharField(required=False, allow_null=True)
    unit_id = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        from .models import Product
        company_id = self.context['request'].company_id
        return Product.create(
            company_id=company_id,
            name=validated_data['name'],
            description=validated_data.get('description'),
            category_id=validated_data.get('category_id'),
            unit_id=validated_data.get('unit_id')
        )
    
    def update(self, instance, validated_data):
        from .models import Product
        product_id = instance['id']
        return Product.update(product_id, validated_data)