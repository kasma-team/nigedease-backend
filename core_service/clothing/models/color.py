from django.db import models
import uuid


class Color(models.Model):
    """
    Manages color options available for clothing products
    Standardizes colors across the product line with consistent naming and hex codes
    Essential for variant management and consistent merchandising
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    hex_code = models.CharField(max_length=7, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'colors' 