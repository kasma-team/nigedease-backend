from django.db import models
import uuid


class BomItem(models.Model):
    """
    Details each material component needed in a bill of materials
    Specifies exact quantities, accounting for waste percentages
    Used for material requirements planning and cost calculations
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bom = models.ForeignKey('clothing.BillOfMaterials', on_delete=models.CASCADE)
    material = models.ForeignKey('clothing.Material', on_delete=models.RESTRICT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    waste_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bom_items' 