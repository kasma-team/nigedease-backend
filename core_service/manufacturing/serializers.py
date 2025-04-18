from rest_framework import serializers
from .models import BillOfMaterials, BOMItem, ProductionStage, ProductionOrder, ProductionOrderStage
from product.serializers import ProductSerializer
from inventory.serializers import MaterialSerializer

class BillOfMaterialsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    company_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = BillOfMaterials
        fields = ['id', 'name', 'description', 'labor_cost', 'overhead_cost', 
                 'total_cost', 'product', 'product_id', 'company', 'company_id',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']

    def validate_company_id(self, value):
        from financial.models import Company
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value
    
    def validate_product_id(self, value):
        from product.models import Product
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Product with id {value} does not exist.")
        return value

class BOMItemSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)
    material_id = serializers.UUIDField(write_only=True)
    bom = BillOfMaterialsSerializer(read_only=True)
    bom_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = BOMItem
        fields = ['id', 'bom', 'bom_id', 'material', 'material_id', 'quantity', 
                 'unit_cost', 'waste_percentage', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_material_id(self, value):
        from inventory.models import Material
        if not Material.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Material with id {value} does not exist.")
        return value
    
    def validate_bom_id(self, value):
        if not BillOfMaterials.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Bill of Materials with id {value} does not exist.")
        return value

class ProductionStageSerializer(serializers.ModelSerializer):
    company_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = ProductionStage
        fields = ['id', 'name', 'description', 'sequence_number', 'estimated_time',
                 'company', 'company_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']

    def validate_company_id(self, value):
        from financial.models import Company
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value

class ProductionOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    bom = BillOfMaterialsSerializer(read_only=True)
    bom_id = serializers.UUIDField(write_only=True)
    company_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = ProductionOrder
        fields = ['id', 'order_number', 'description', 'planned_quantity', 
                 'produced_quantity', 'start_date', 'end_date', 'status', 'notes',
                 'product', 'product_id', 'bom', 'bom_id', 'company', 'company_id',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']

    def validate_company_id(self, value):
        from financial.models import Company
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Company with id {value} does not exist.")
        return value
    
    def validate_product_id(self, value):
        from product.models import Product
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Product with id {value} does not exist.")
        return value
    
    def validate_bom_id(self, value):
        if not BillOfMaterials.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Bill of Materials with id {value} does not exist.")
        return value

class ProductionOrderStageSerializer(serializers.ModelSerializer):
    production_order = ProductionOrderSerializer(read_only=True)
    production_order_id = serializers.UUIDField(write_only=True)
    production_stage = ProductionStageSerializer(read_only=True)
    production_stage_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = ProductionOrderStage
        fields = ['id', 'production_order', 'production_order_id', 
                 'production_stage', 'production_stage_id', 'started_at', 
                 'completed_at', 'quantity_processed', 'quantity_passed', 
                 'quantity_rejected', 'notes', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_production_order_id(self, value):
        if not ProductionOrder.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Production Order with id {value} does not exist.")
        return value
    
    def validate_production_stage_id(self, value):
        if not ProductionStage.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Production Stage with id {value} does not exist.")
        return value 