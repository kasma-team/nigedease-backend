from django.db import models
from django.utils import timezone
from product.models import Product

class Store(models.Model):
    name = models.CharField(max_length=200)
    location = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['product', 'store']),
        ]
        unique_together = ['product', 'store']

    def __str__(self):
        return f"{self.product.name} - {self.store.name} - {self.quantity}"