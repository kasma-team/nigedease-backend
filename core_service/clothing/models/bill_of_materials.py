from django.db import models
import uuid


class BillOfMaterials(models.Model):
    """
    Defines the recipe for manufacturing a clothing product
    Lists all required materials, labor costs, and overhead expenses
    Used to calculate product costs and plan production requirements
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2)
    overhead_cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bill_of_materials'
        unique_together = ('product', 'version') 