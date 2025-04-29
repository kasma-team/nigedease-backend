from django.test import TestCase
from clothing.models import (
    Material, Color, Size, SizeChart, Season, Collection,
    ProductVariant, BillOfMaterials, BomItem,
    ProductionStage, ProductionOrder, ProductionOrderStage
)

class ClothingModelsTest(TestCase):
    def test_model_fields(self):
        """Test that all clothing models have the expected fields"""
        models = [
            Material, 
            Color,
            Size,
            SizeChart,
            Season,
            Collection,
            ProductVariant,
            BillOfMaterials,
            BomItem,
            ProductionStage,
            ProductionOrder,
            ProductionOrderStage
        ]
        
        for model in models:
            fields = model._meta.get_fields()
            self.assertTrue(len(fields) > 0, f"{model.__name__} should have fields")
            
            for field in fields:
                self.assertTrue(hasattr(field, 'name'), f"Field in {model.__name__} should have a name")
                
                if hasattr(field, 'choices') and field.choices:
                    self.assertTrue(isinstance(field.choices, (list, tuple)), 
                                 f"Choices in {model.__name__}.{field.name} should be a list or tuple") 