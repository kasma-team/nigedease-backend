from django.db import models
import uuid
from decimal import Decimal
from inventory.models.store import Store

class Product(models.Model):
    GENDER_CHOICES = (
        ('men', 'Men'),
        ('women', 'Women'),
        ('unisex', 'Unisex'),
        ('kids', 'Kids'),
        ('none', 'None'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    image = models.URLField(null=True)
    product_unit = models.ForeignKey('inventory.ProductUnit', on_delete=models.PROTECT)
    product_category = models.ForeignKey('inventory.ProductCategory', on_delete=models.PROTECT)
    collection = models.ForeignKey('clothing.Collection', on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='none')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

 
    
    