import uuid
from django.db import models
from django.core.validators import MinValueValidator
from financial.models import Company  # Import Company from Financial app
from product.models import Product, ProductVariant  # Import Product and ProductVariant from Product app

class Store(models.Model):
    STORE_TYPE_CHOICES = [
        ('retail', 'Retail Store'),
        ('warehouse', 'Warehouse'),
        ('factory', 'Factory'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    store_type = models.CharField(max_length=20, choices=STORE_TYPE_CHOICES, default='retail')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.company.name})"

class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=19, decimal_places=4)
    min_stock_level = models.DecimalField(max_digits=10, decimal_places=2, default=5)
    max_stock_level = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('product', 'store', 'product_variant')
    
    def __str__(self):
        base_str = f"{self.product.name} - {self.store.name} ({self.quantity})"
        if self.product_variant:
            return f"{base_str} - {self.product_variant.size.name}/{self.product_variant.color.name}"
        return base_str

class Material(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('fabric', 'Fabric'),
        ('thread', 'Thread'),
        ('button', 'Button'),
        ('zipper', 'Zipper'),
        ('elastic', 'Elastic'),
        ('trim', 'Trim'),
        ('lining', 'Lining'),
        ('interfacing', 'Interfacing'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    material_type = models.CharField(max_length=30, choices=MATERIAL_TYPE_CHOICES)
    properties = models.JSONField(null=True, blank=True)  # e.g., {"stretch": true, "water_resistant": false}
    unit_of_measure = models.CharField(max_length=20)  # meters, yards, pcs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_material_type_display()})"