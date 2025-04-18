import uuid
from django.db import models
from financial.models import Company
from product.models import Product
from inventory.models import Material

class BillOfMaterials(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overhead_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Bill of Materials"
        verbose_name_plural = "Bills of Materials"
    
    def __str__(self):
        return f"{self.name} - {self.product.name}"

class BOMItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bom = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE, related_name='items')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    waste_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "BOM Item"
        verbose_name_plural = "BOM Items"
    
    def __str__(self):
        return f"{self.material.name} - {self.quantity} {self.material.unit_of_measure}"

class ProductionStage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    sequence_number = models.IntegerField(default=0)
    estimated_time = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sequence_number']
    
    def __str__(self):
        return f"{self.sequence_number}. {self.name}"

class ProductionOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    planned_quantity = models.IntegerField()
    produced_quantity = models.IntegerField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bom = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"PO-{self.order_number} - {self.product.name} ({self.status})"

class ProductionOrderStage(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE, related_name='stages')
    production_stage = models.ForeignKey(ProductionStage, on_delete=models.CASCADE)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    quantity_processed = models.IntegerField(null=True, blank=True)
    quantity_passed = models.IntegerField(null=True, blank=True)
    quantity_rejected = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['production_stage__sequence_number']
    
    def __str__(self):
        return f"{self.production_order.order_number} - {self.production_stage.name} ({self.status})" 