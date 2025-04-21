from django.db import models
import uuid


class ProductionOrder(models.Model):
    """
    Manufacturing work orders to produce specific quantities of items
    Tracks production status, timelines, and completion rates
    Used to manage factory workflow and production scheduling
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.RESTRICT)
    bom = models.ForeignKey('clothing.BillOfMaterials', on_delete=models.RESTRICT)
    order_number = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    target_completion_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(default=1)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'production_orders' 