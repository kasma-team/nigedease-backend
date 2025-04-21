from django.db import models
import uuid


class Season(models.Model):
    """
    Represents fashion seasons and collection periods (Spring/Summer, Fall/Winter)
    Organizes product planning, manufacturing, and merchandising by time periods
    Helps with inventory planning and markdown scheduling
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'seasons' 