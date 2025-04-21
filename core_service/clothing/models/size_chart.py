from django.db import models
import uuid


class SizeChart(models.Model):
    """
    Provides detailed measurement guides for different product categories
    Maps between labeled sizes and actual measurements (chest, waist, hips, etc.)
    Used for online shopping guidance and quality control
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    size = models.ForeignKey('clothing.Size', on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    chest_measurement = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    waist_measurement = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hip_measurement = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    inseam_measurement = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'size_charts' 