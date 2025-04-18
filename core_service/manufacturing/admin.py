from django.contrib import admin
from .models import (
    BillOfMaterials, BOMItem, 
    ProductionStage, ProductionOrder, ProductionOrderStage
)

admin.site.register(BillOfMaterials)
admin.site.register(BOMItem)
admin.site.register(ProductionStage)
admin.site.register(ProductionOrder)
admin.site.register(ProductionOrderStage) 