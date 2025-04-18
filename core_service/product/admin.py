from django.contrib import admin
from .models import (
    ProductUnit, ProductCategory, Product, 
    Season, Collection, Color, Size, SizeChart,
    ProductVariant
)

admin.site.register(ProductUnit)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Season)
admin.site.register(Collection)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(SizeChart)
admin.site.register(ProductVariant)
