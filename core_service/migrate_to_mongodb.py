import os
import django
import pymongo
from django.conf import settings
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_service.settings')
django.setup()

# MongoDB connection
mongo_client = pymongo.MongoClient(
    host=settings.DATABASES['default']['CLIENT']['host'],
    port=settings.DATABASES['default']['CLIENT']['port'],
    username=settings.DATABASES['default']['CLIENT']['username'],
    password=settings.DATABASES['default']['CLIENT']['password']
)

# Get database
db = mongo_client[settings.DATABASES['default']['NAME']]

def migrate_financial_data():
    from financial.models import Transaction, Expense, Income
    print("Migrating financial data...")
    
    # Migrate Transactions
    transactions = Transaction.objects.all()
    for transaction in transactions:
        db.transactions.insert_one({
            'id': str(transaction.id),
            'amount': float(transaction.amount),
            'description': transaction.description,
            'date': transaction.date,
            'transaction_type': transaction.transaction_type,
            'created_at': transaction.created_at,
            'updated_at': transaction.updated_at
        })
    
    # Migrate Expenses
    expenses = Expense.objects.all()
    for expense in expenses:
        db.expenses.insert_one({
            'id': str(expense.id),
            'amount': float(expense.amount),
            'description': expense.description,
            'category': expense.category,
            'date': expense.date,
            'created_at': expense.created_at,
            'updated_at': expense.updated_at
        })
    
    # Migrate Income
    incomes = Income.objects.all()
    for income in incomes:
        db.incomes.insert_one({
            'id': str(income.id),
            'amount': float(income.amount),
            'description': income.description,
            'source': income.source,
            'date': income.date,
            'created_at': income.created_at,
            'updated_at': income.updated_at
        })

def migrate_product_data():
    from product.models import Product, Category
    print("Migrating product data...")
    
    # Migrate Categories
    categories = Category.objects.all()
    for category in categories:
        db.categories.insert_one({
            'id': str(category.id),
            'name': category.name,
            'description': category.description,
            'created_at': category.created_at,
            'updated_at': category.updated_at
        })
    
    # Migrate Products
    products = Product.objects.all()
    for product in products:
        db.products.insert_one({
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'category_id': str(product.category.id) if product.category else None,
            'created_at': product.created_at,
            'updated_at': product.updated_at
        })

def migrate_inventory_data():
    from inventory.models import Store, Stock
    print("Migrating inventory data...")
    
    # Migrate Stores
    stores = Store.objects.all()
    for store in stores:
        db.stores.insert_one({
            'id': str(store.id),
            'name': store.name,
            'location': store.location,
            'created_at': store.created_at,
            'updated_at': store.updated_at
        })
    
    # Migrate Stock
    stocks = Stock.objects.all()
    for stock in stocks:
        db.stocks.insert_one({
            'id': str(stock.id),
            'product_id': str(stock.product.id) if stock.product else None,
            'store_id': str(stock.store.id) if stock.store else None,
            'quantity': stock.quantity,
            'created_at': stock.created_at,
            'updated_at': stock.updated_at
        })

def main():
    print("Starting migration to MongoDB...")
    
    # Create indexes
    db.transactions.create_index('date')
    db.expenses.create_index('date')
    db.incomes.create_index('date')
    db.products.create_index('category_id')
    db.stocks.create_index([('product_id', 1), ('store_id', 1)])
    
    # Run migrations
    migrate_financial_data()
    migrate_product_data()
    migrate_inventory_data()
    
    print("Migration completed successfully!")

if __name__ == '__main__':
    main() 