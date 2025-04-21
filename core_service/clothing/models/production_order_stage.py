from django.db import models
import uuid


class ProductionOrderStage(models.Model):
    """
    Tracks the progress of production orders through each manufacturing stage
    Records quality metrics including pass/fail rates at each stage
    Provides visibility into production bottlenecks and quality issues
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    production_order = models.ForeignKey('clothing.ProductionOrder', on_delete=models.CASCADE)
    production_stage = models.ForeignKey('clothing.ProductionStage', on_delete=models.RESTRICT)
    start_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    completed_quantity = models.IntegerField(null=True, blank=True)
    failure_quantity = models.IntegerField(default=0)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'production_order_stages' 