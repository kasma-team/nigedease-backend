from django.db import models
import uuid


class Collection(models.Model):
    """
    Groups products into cohesive fashion lines or collections
    Ties products to specific design themes, seasonal releases, or campaigns
    Facilitates merchandising, marketing, and coordinated releases
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    season = models.ForeignKey('clothing.Season', on_delete=models.SET_NULL, null=True, blank=True)
    launch_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'collections' 