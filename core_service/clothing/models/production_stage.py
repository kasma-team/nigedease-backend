from django.db import models
import uuid


class ProductionStage(models.Model):
    """
    Defines steps in the clothing manufacturing process
    Typical stages include cutting, sewing, quality control, and packaging
    Stores estimated time requirements and sequence information
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    estimated_time_minutes = models.IntegerField(null=True, blank=True)
    sequence_order = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'production_stages' 