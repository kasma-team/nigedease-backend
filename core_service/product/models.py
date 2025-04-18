import uuid
from django.db import models
from django.core.validators import MinValueValidator
from financial.models import Company  # Import Company from Financial app

class ProductUnit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.company.name})"

class SizeChart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=30)  # shirts, pants, dresses, etc.
    chart_data = models.JSONField(default=dict)  # mapping sizes to measurements
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class ProductCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    size_chart = models.ForeignKey(SizeChart, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.company.name})"

class Season(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)  # Spring/Summer 2023, Fall/Winter 2023
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Color(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    color_code = models.CharField(max_length=10, default='#000000')  # Default to black
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Size(models.Model):
    CATEGORY_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('children', 'Children'),
        ('unisex', 'Unisex'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)  # XS, S, M, L, XL, XXL, or numeric sizes
    description = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='unisex')
    measurement_unit = models.CharField(max_length=10, default='cm')
    measurements = models.JSONField(null=True, blank=True)  # e.g., {"chest": 100, "waist": 80}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Product(models.Model):
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('unisex', 'Unisex'),
        ('children', 'Children'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    unit = models.ForeignKey(ProductUnit, on_delete=models.SET_NULL, null=True)
    sku = models.CharField(max_length=30, blank=True, null=True)
    barcode = models.CharField(max_length=30, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_unit = models.CharField(max_length=5, default='g')
    is_featured = models.BooleanField(default=False)
    image = models.CharField(max_length=200, blank=True, null=True)
    image_urls = models.JSONField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.company.name})"

class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    sku = models.CharField(max_length=30)
    barcode = models.CharField(max_length=30, blank=True, null=True)
    additional_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dimensions = models.JSONField(null=True, blank=True)  # e.g., {"length": 30, "width": 20}
    image_url = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('product', 'size', 'color')
    
    def __str__(self):
        return f"{self.product.name} - {self.size.name} - {self.color.name}"