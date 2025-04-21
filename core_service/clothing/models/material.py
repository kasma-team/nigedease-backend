from django.db import models
import uuid


class Material(models.Model):
    """
    Catalogs raw materials used in clothing manufacturing
    Stores fabrics (cotton, polyester, denim), notions (buttons, zippers), and trims
    Tracks properties like stretch, water resistance, and unit of measurement
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    material_type = models.CharField(max_length=100)
    unit_of_measurement = models.CharField(max_length=50)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    is_stretch = models.BooleanField(default=False)
    is_water_resistant = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'materials' 