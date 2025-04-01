from rest_framework import serializers
# Remove model imports since we are using MongoDB directly

class PaymentModeSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

class CurrencySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    code = serializers.CharField(required=True, max_length=3)
    name = serializers.CharField(required=True, max_length=255)
    created_at = serializers.DateTimeField(read_only=True)

class SubscriptionPlanSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True, max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    currency = serializers.CharField(read_only=True)
    currency_id = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

class CompanySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True, max_length=255)
    subscription_plan = serializers.CharField(read_only=True)
    subscription_plan_id = serializers.CharField(required=False)
    payment_mode = serializers.CharField(read_only=True)
    payment_mode_id = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

class SaleItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    sale_id = serializers.CharField(required=False)
    product_id = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

class SaleSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    company_id = serializers.CharField()
    store_id = serializers.CharField(required=True)
    customer_id = serializers.CharField(required=False, allow_null=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    currency = serializers.CharField(read_only=True)
    currency_id = serializers.CharField(required=True)
    payment_mode = serializers.CharField(read_only=True)
    payment_mode_id = serializers.CharField()
    is_credit = serializers.BooleanField(default=False)
    items = SaleItemSerializer(many=True, required=True)
    created_at = serializers.DateTimeField(read_only=True)

class PurchaseItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    purchase = serializers.CharField(read_only=True)
    product_id = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)
    unit_cost = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    created_at = serializers.DateTimeField(read_only=True)

class PurchaseSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    company_id = serializers.CharField()
    store_id = serializers.CharField(required=True)
    supplier_id = serializers.CharField(required=False, allow_null=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    currency = serializers.CharField(read_only=True)
    currency_id = serializers.CharField(required=True)
    payment_mode = serializers.CharField(read_only=True)
    payment_mode_id = serializers.CharField()
    is_credit = serializers.BooleanField(default=False)
    items = PurchaseItemSerializer(many=True, required=True)
    created_at = serializers.DateTimeField(read_only=True)

class ExpenseCategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    company_id = serializers.CharField()
    name = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

class ExpenseSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    company_id = serializers.CharField()
    category = serializers.CharField(read_only=True)
    category_id = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    currency = serializers.CharField(read_only=True)
    currency_id = serializers.CharField(required=True)
    payment_mode = serializers.CharField(read_only=True)
    payment_mode_id = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True)
    is_credit = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)

class PayableSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    company_id = serializers.CharField()
    type = serializers.CharField(required=True, max_length=50)
    purchase_id = serializers.CharField(required=False)
    expense_id = serializers.CharField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    currency = serializers.CharField(read_only=True)
    currency_id = serializers.CharField(required=True)
    due_date = serializers.DateField(required=True)
    created_at = serializers.DateTimeField(read_only=True)

class ReceivableSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    company_id = serializers.CharField()
    sale_id = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    currency = serializers.CharField(read_only=True)
    currency_id = serializers.CharField(required=True)
    due_date = serializers.DateField(required=True)
    created_at = serializers.DateTimeField(read_only=True)

class BankSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    company_id = serializers.CharField()
    account_name = serializers.CharField(required=True, max_length=255)
    account_number = serializers.CharField(required=True, max_length=50)
    bank_name = serializers.CharField(required=True, max_length=255)
    created_at = serializers.DateTimeField(read_only=True)

class PaymentOutSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    company_id = serializers.CharField()
    type = serializers.CharField(max_length=50, required=True)
    payable_id = serializers.CharField(required=False)
    expense_id = serializers.CharField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    currency = serializers.CharField(read_only=True)
    currency_id = serializers.CharField(required=True)
    payment_mode = serializers.CharField(read_only=True)
    payment_mode_id = serializers.CharField(required=True)
    bank_id = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True)

class PaymentInSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    company_id = serializers.CharField()
    type = serializers.CharField(max_length=50, required=True)
    receivable_id = serializers.CharField(required=False)
    sale_id = serializers.CharField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    currency = serializers.CharField(read_only=True)
    currency_id = serializers.CharField(required=True)
    payment_mode = serializers.CharField(read_only=True)
    payment_mode_id = serializers.CharField(required=True)
    bank_id = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True)

class ReportSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    company_id = serializers.CharField()
    report_type = serializers.CharField(max_length=100, required=True)
    data = serializers.JSONField(required=True)
    generated_at = serializers.DateTimeField(read_only=True)