from django.db import models
import uuid


class Size(models.Model):
    """
    Defines available size options for clothing items (XS, S, M, L, XL, numeric sizes)
    Stores measurement specifications for each size by gender/category
    Used to create product variants and maintain size consistency
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    size_code = models.CharField(max_length=10)
    category = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, null=True, blank=True)
    order_sequence = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sizes'
        unique_together = ('name', 'category', 'gender') 