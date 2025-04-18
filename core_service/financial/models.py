import uuid
from django.db import models
from django.core.exceptions import ValidationError

class PaymentMode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Currency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class SubscriptionPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
 
class Company(models.Model):
    BUSINESS_TYPE_CHOICES = [
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('both', 'Both'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, default='example@example.com')
    short_name = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES, default='retail')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, default='123456(*Udfjio)')

    def __str__(self):
        return self.name

class Customer(models.Model):
    MEMBERSHIP_CHOICES = [
        ('standard', 'Standard'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loyalty_points = models.IntegerField(default=0)
    membership_level = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default='standard')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Supplier(models.Model):
    SUPPLIER_TYPE_CHOICES = [
        ('fabric', 'Fabric'),
        ('accessory', 'Accessory'),
        ('packaging', 'Packaging'),
        ('machinery', 'Machinery'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    supplier_type = models.CharField(max_length=20, choices=SUPPLIER_TYPE_CHOICES, default='other')
    lead_time_days = models.IntegerField(null=True, blank=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Sale(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    store = models.ForeignKey('inventory.Store', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=19, decimal_places=4)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.SET_NULL, null=True, blank=True)
    is_credit = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=20, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Sale {self.id} - {self.company.name}"

class SaleItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    product_variant = models.ForeignKey('product.ProductVariant', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=19, decimal_places=4)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        base_str = f"SaleItem {self.id} - {self.product.name}"
        if self.product_variant:
            return f"{base_str} ({self.product_variant.size.name}/{self.product_variant.color.name})"
        return base_str

class Purchase(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    store = models.ForeignKey('inventory.Store', on_delete=models.CASCADE)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=19, decimal_places=4)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.SET_NULL, null=True, blank=True)
    is_credit = models.BooleanField(default=False)
    purchase_number = models.CharField(max_length=20, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Purchase {self.id} - {self.company.name}"

class PurchaseItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    product_variant = models.ForeignKey('product.ProductVariant', on_delete=models.CASCADE, null=True, blank=True)
    material = models.ForeignKey('inventory.Material', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=19, decimal_places=4)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        """Ensure that either product_variant or material is provided, but not both"""
        if self.product_variant and self.material:
            raise ValidationError("A purchase item can be associated with either a product variant or a material, not both.")
    
    def __str__(self):
        if self.product_variant:
            return f"PurchaseItem {self.id} - {self.product.name} ({self.product_variant.size.name}/{self.product_variant.color.name})"
        elif self.material:
            return f"PurchaseItem {self.id} - Material: {self.material.name}"
        return f"PurchaseItem {self.id} - {self.product.name}"

class ExpenseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    is_credit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Expense {self.id} - {self.company.name}"

class Payable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    purchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True, blank=True)
    expense = models.ForeignKey(Expense, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Payable {self.id} - {self.company.name}"
    def clean(self):
        if self.purchase and self.expense:
            raise ValidationError("A payable can be associated with either a purchase or an expense, not both.")
        if not (self.purchase or self.expense):
            raise ValidationError("A payable must be associated with either a purchase or an expense.")

class Receivable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Receivable {self.id} - {self.company.name}"

class Bank(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.account_name} - {self.bank_name}"

class PaymentOut(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    payable = models.ForeignKey(Payable, on_delete=models.SET_NULL, null=True, blank=True)
    expense = models.ForeignKey(Expense, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.SET_NULL, null=True)
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"PaymentOut {self.id} - {self.company.name}"
    def clean(self):
        if self.payable and self.expense:
            raise ValidationError("A payment out can be associated with either a payable or an expense, not both.")
        if not (self.payable or self.expense):
            raise ValidationError("A payment out must be associated with either a payable or an expense.")

class PaymentIn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    receivable = models.ForeignKey(Receivable, on_delete=models.SET_NULL, null=True, blank=True)
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.SET_NULL, null=True)
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"PaymentIn {self.id} - {self.company.name}"
    def clean(self):
        if self.receivable and self.sale:
            raise ValidationError("A payment in can be associated with either a receivable or a sale, not both.")
        if not (self.receivable or self.sale):
            raise ValidationError("A payment in must be associated with either a receivable or a sale.")

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=100)
    data = models.JSONField()
    generated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Report {self.id} - {self.report_type} for {self.company.name}"