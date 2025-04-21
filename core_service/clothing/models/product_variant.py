from django.db import models
import uuid


class ProductVariant(models.Model):
    """
    Represents specific size/color combinations of a base product
    Each variant has its own inventory, SKU, and potentially unique pricing
    Example: "Blue Denim Shirt" in "Medium" and "Light Blue" is one variant
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)
    size = models.ForeignKey('clothing.Size', on_delete=models.RESTRICT)
    color = models.ForeignKey('clothing.Color', on_delete=models.RESTRICT)
    sku = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_variants' 