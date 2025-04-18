from django.contrib import admin
from .models import (
    PaymentMode, Currency, SubscriptionPlan, Company,
    Customer, Supplier, Sale, SaleItem, 
    Purchase, PurchaseItem
)

admin.site.register(PaymentMode)
admin.site.register(Currency)
admin.site.register(SubscriptionPlan)
admin.site.register(Company)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
