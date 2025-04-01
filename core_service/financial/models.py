import uuid
from datetime import datetime
from core_service.mongodb import db

# MongoDB Collections
companies_collection = db.companies
sales_collection = db.sales
purchases_collection = db.purchases
expense_categories_collection = db.expense_categories
expenses_collection = db.expenses
payment_modes_collection = db.payment_modes
payables_collection = db.payables
receivables_collection = db.receivables
banks_collection = db.banks
payments_out_collection = db.payments_out
payments_in_collection = db.payments_in
reports_collection = db.reports
currencies_collection = db.currencies
subscription_plans_collection = db.subscription_plans

class Company:
    @staticmethod
    def create(name, address=None, email=None, phone_number=None):
        """Create a new company"""
        company = {
            "id": str(uuid.uuid4()),
            "name": name,
            "address": address,
            "email": email,
            "phone_number": phone_number,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        companies_collection.insert_one(company)
        return company
    
    @staticmethod
    def get_by_id(company_id):
        """Get company by ID"""
        return companies_collection.find_one({"id": company_id})
    
    @staticmethod
    def get_by_email(email):
        """Get company by email"""
        return companies_collection.find_one({"email": email})
    
    @staticmethod
    def get_all():
        """Get all companies"""
        return list(companies_collection.find().sort("name", 1))
    
    @staticmethod
    def update(company_id, data):
        """Update a company"""
        data["updated_at"] = datetime.utcnow()
        companies_collection.update_one({"id": company_id}, {"$set": data})
        return companies_collection.find_one({"id": company_id})
    
    @staticmethod
    def delete(company_id):
        """Delete a company"""
        companies_collection.delete_one({"id": company_id})

class PaymentMode:
    @staticmethod
    def create(name, description=None):
        """Create a new payment mode"""
        payment_mode = {
            "id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        payment_modes_collection.insert_one(payment_mode)
        return payment_mode
    
    @staticmethod
    def get_by_id(payment_mode_id):
        """Get payment mode by ID"""
        return payment_modes_collection.find_one({"id": payment_mode_id})
    
    @staticmethod
    def get_all():
        """Get all payment modes"""
        return list(payment_modes_collection.find().sort("name", 1))
    
    @staticmethod
    def update(payment_mode_id, data):
        """Update a payment mode"""
        data["updated_at"] = datetime.utcnow()
        payment_modes_collection.update_one({"id": payment_mode_id}, {"$set": data})
        return payment_modes_collection.find_one({"id": payment_mode_id})
    
    @staticmethod
    def delete(payment_mode_id):
        """Delete a payment mode"""
        payment_modes_collection.delete_one({"id": payment_mode_id})

class Sale:
    @staticmethod
    def create(company_id, store_id, customer_id=None, items=None, total_amount=0, 
               payment_mode_id=None, payment_status="pending", notes=None):
        """Create a new sale"""
        sale = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "store_id": store_id,
            "customer_id": customer_id,
            "items": items or [],
            "total_amount": total_amount,
            "payment_mode_id": payment_mode_id,
            "payment_status": payment_status,
            "notes": notes,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        sales_collection.insert_one(sale)
        return sale
    
    @staticmethod
    def get_by_id(sale_id):
        """Get sale by ID"""
        return sales_collection.find_one({"id": sale_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all sales for a company"""
        return list(sales_collection.find({"company_id": company_id}).sort("created_at", -1))
    
    @staticmethod
    def update(sale_id, data):
        """Update a sale"""
        data["updated_at"] = datetime.utcnow()
        sales_collection.update_one({"id": sale_id}, {"$set": data})
        return sales_collection.find_one({"id": sale_id})
    
    @staticmethod
    def delete(sale_id):
        """Delete a sale"""
        sales_collection.delete_one({"id": sale_id})

class Purchase:
    @staticmethod
    def create(company_id, store_id, supplier_id=None, items=None, total_amount=0,
               payment_mode_id=None, payment_status="pending", notes=None):
        """Create a new purchase"""
        purchase = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "store_id": store_id,
            "supplier_id": supplier_id,
            "items": items or [],
            "total_amount": total_amount,
            "payment_mode_id": payment_mode_id,
            "payment_status": payment_status,
            "notes": notes,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        purchases_collection.insert_one(purchase)
        return purchase
    
    @staticmethod
    def get_by_id(purchase_id):
        """Get purchase by ID"""
        return purchases_collection.find_one({"id": purchase_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all purchases for a company"""
        return list(purchases_collection.find({"company_id": company_id}).sort("created_at", -1))
    
    @staticmethod
    def update(purchase_id, data):
        """Update a purchase"""
        data["updated_at"] = datetime.utcnow()
        purchases_collection.update_one({"id": purchase_id}, {"$set": data})
        return purchases_collection.find_one({"id": purchase_id})
    
    @staticmethod
    def delete(purchase_id):
        """Delete a purchase"""
        purchases_collection.delete_one({"id": purchase_id})

class ExpenseCategory:
    @staticmethod
    def create(company_id, name, description=None):
        """Create a new expense category"""
        category = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "name": name,
            "description": description,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        expense_categories_collection.insert_one(category)
        return category
    
    @staticmethod
    def get_by_id(category_id):
        """Get expense category by ID"""
        return expense_categories_collection.find_one({"id": category_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all expense categories for a company"""
        return list(expense_categories_collection.find({"company_id": company_id}).sort("name", 1))
    
    @staticmethod
    def update(category_id, data):
        """Update an expense category"""
        data["updated_at"] = datetime.utcnow()
        expense_categories_collection.update_one({"id": category_id}, {"$set": data})
        return expense_categories_collection.find_one({"id": category_id})
    
    @staticmethod
    def delete(category_id):
        """Delete an expense category"""
        expense_categories_collection.delete_one({"id": category_id})

class Currency:
    @staticmethod
    def create(code, name):
        """Create a new currency"""
        currency = {
            "id": str(uuid.uuid4()),
            "code": code,
            "name": name,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        currencies_collection.insert_one(currency)
        return currency
    
    @staticmethod
    def get_by_id(currency_id):
        """Get currency by ID"""
        return currencies_collection.find_one({"id": currency_id})
    
    @staticmethod
    def get_by_code(code):
        """Get currency by code"""
        return currencies_collection.find_one({"code": code})
    
    @staticmethod
    def get_all():
        """Get all currencies"""
        return list(currencies_collection.find().sort("code", 1))
    
    @staticmethod
    def update(currency_id, data):
        """Update a currency"""
        currencies_collection.update_one({"id": currency_id}, {"$set": data})
        return currencies_collection.find_one({"id": currency_id})
    
    @staticmethod
    def delete(currency_id):
        """Delete a currency"""
        currencies_collection.delete_one({"id": currency_id})

class SubscriptionPlan:
    @staticmethod
    def create(name, price, currency_id, description=None):
        """Create a new subscription plan"""
        plan = {
            "id": str(uuid.uuid4()),
            "name": name,
            "price": price,
            "currency_id": currency_id,
            "description": description,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        subscription_plans_collection.insert_one(plan)
        return plan
    
    @staticmethod
    def get_by_id(plan_id):
        """Get subscription plan by ID"""
        return subscription_plans_collection.find_one({"id": plan_id})
    
    @staticmethod
    def get_all():
        """Get all subscription plans"""
        return list(subscription_plans_collection.find().sort("name", 1))

class Expense:
    @staticmethod
    def create(company_id, category_id, amount, currency_id, payment_mode_id=None, description=None, is_credit=False):
        """Create a new expense"""
        expense = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "category_id": category_id,
            "amount": amount,
            "currency_id": currency_id,
            "payment_mode_id": payment_mode_id,
            "description": description,
            "is_credit": is_credit,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        expenses_collection.insert_one(expense)
        return expense
    
    @staticmethod
    def get_by_id(expense_id):
        """Get expense by ID"""
        return expenses_collection.find_one({"id": expense_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all expenses for a company"""
        return list(expenses_collection.find({"company_id": company_id}).sort("created_at", -1))
    
    @staticmethod
    def update(expense_id, data):
        """Update an expense"""
        data["updated_at"] = datetime.utcnow()
        expenses_collection.update_one({"id": expense_id}, {"$set": data})
        return expenses_collection.find_one({"id": expense_id})
    
    @staticmethod
    def delete(expense_id):
        """Delete an expense"""
        expenses_collection.delete_one({"id": expense_id})

class Payable:
    @staticmethod
    def create(company_id, type, amount, currency_id, due_date, purchase_id=None, expense_id=None):
        """Create a new payable"""
        payable = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "type": type,
            "purchase_id": purchase_id,
            "expense_id": expense_id,
            "amount": amount,
            "currency_id": currency_id,
            "due_date": due_date,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        payables_collection.insert_one(payable)
        return payable
    
    @staticmethod
    def get_by_id(payable_id):
        """Get payable by ID"""
        return payables_collection.find_one({"id": payable_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all payables for a company"""
        return list(payables_collection.find({"company_id": company_id}).sort("created_at", -1))
    
    @staticmethod
    def update(payable_id, data):
        """Update a payable"""
        data["updated_at"] = datetime.utcnow()
        payables_collection.update_one({"id": payable_id}, {"$set": data})
        return payables_collection.find_one({"id": payable_id})
    
    @staticmethod
    def delete(payable_id):
        """Delete a payable"""
        payables_collection.delete_one({"id": payable_id})

class Receivable:
    @staticmethod
    def create(company_id, sale_id, amount, currency_id, due_date):
        """Create a new receivable"""
        receivable = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "sale_id": sale_id,
            "amount": amount,
            "currency_id": currency_id,
            "due_date": due_date,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        receivables_collection.insert_one(receivable)
        return receivable
    
    @staticmethod
    def get_by_id(receivable_id):
        """Get receivable by ID"""
        return receivables_collection.find_one({"id": receivable_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all receivables for a company"""
        return list(receivables_collection.find({"company_id": company_id}).sort("created_at", -1))
    
    @staticmethod
    def update(receivable_id, data):
        """Update a receivable"""
        data["updated_at"] = datetime.utcnow()
        receivables_collection.update_one({"id": receivable_id}, {"$set": data})
        return receivables_collection.find_one({"id": receivable_id})
    
    @staticmethod
    def delete(receivable_id):
        """Delete a receivable"""
        receivables_collection.delete_one({"id": receivable_id})

class Bank:
    @staticmethod
    def create(company_id, account_name, account_number, bank_name):
        """Create a new bank"""
        bank = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "account_name": account_name,
            "account_number": account_number,
            "bank_name": bank_name,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        banks_collection.insert_one(bank)
        return bank
    
    @staticmethod
    def get_by_id(bank_id):
        """Get bank by ID"""
        return banks_collection.find_one({"id": bank_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all banks for a company"""
        return list(banks_collection.find({"company_id": company_id}).sort("account_name", 1))
    
    @staticmethod
    def update(bank_id, data):
        """Update a bank"""
        data["updated_at"] = datetime.utcnow()
        banks_collection.update_one({"id": bank_id}, {"$set": data})
        return banks_collection.find_one({"id": bank_id})
    
    @staticmethod
    def delete(bank_id):
        """Delete a bank"""
        banks_collection.delete_one({"id": bank_id})

class PaymentOut:
    @staticmethod
    def create(company_id, type, amount, currency_id, payment_mode_id, bank_id, payable_id=None, expense_id=None):
        """Create a new payment out"""
        payment_out = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "type": type,
            "payable_id": payable_id,
            "expense_id": expense_id,
            "amount": amount,
            "currency_id": currency_id,
            "payment_mode_id": payment_mode_id,
            "bank_id": bank_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        payments_out_collection.insert_one(payment_out)
        return payment_out
    
    @staticmethod
    def get_by_id(payment_out_id):
        """Get payment out by ID"""
        return payments_out_collection.find_one({"id": payment_out_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all payments out for a company"""
        return list(payments_out_collection.find({"company_id": company_id}).sort("created_at", -1))
    
    @staticmethod
    def update(payment_out_id, data):
        """Update a payment out"""
        data["updated_at"] = datetime.utcnow()
        payments_out_collection.update_one({"id": payment_out_id}, {"$set": data})
        return payments_out_collection.find_one({"id": payment_out_id})
    
    @staticmethod
    def delete(payment_out_id):
        """Delete a payment out"""
        payments_out_collection.delete_one({"id": payment_out_id})

class PaymentIn:
    @staticmethod
    def create(company_id, type, amount, currency_id, payment_mode_id, bank_id, receivable_id=None, sale_id=None):
        """Create a new payment in"""
        payment_in = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "type": type,
            "receivable_id": receivable_id,
            "sale_id": sale_id,
            "amount": amount,
            "currency_id": currency_id,
            "payment_mode_id": payment_mode_id,
            "bank_id": bank_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        payments_in_collection.insert_one(payment_in)
        return payment_in
    
    @staticmethod
    def get_by_id(payment_in_id):
        """Get payment in by ID"""
        return payments_in_collection.find_one({"id": payment_in_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all payments in for a company"""
        return list(payments_in_collection.find({"company_id": company_id}).sort("created_at", -1))
    
    @staticmethod
    def update(payment_in_id, data):
        """Update a payment in"""
        data["updated_at"] = datetime.utcnow()
        payments_in_collection.update_one({"id": payment_in_id}, {"$set": data})
        return payments_in_collection.find_one({"id": payment_in_id})
    
    @staticmethod
    def delete(payment_in_id):
        """Delete a payment in"""
        payments_in_collection.delete_one({"id": payment_in_id})

class Report:
    @staticmethod
    def create(company_id, report_type, data):
        """Create a new report"""
        report = {
            "id": str(uuid.uuid4()),
            "company_id": company_id,
            "report_type": report_type,
            "data": data,
            "generated_at": datetime.utcnow()
        }
        
        reports_collection.insert_one(report)
        return report
    
    @staticmethod
    def get_by_id(report_id):
        """Get report by ID"""
        return reports_collection.find_one({"id": report_id})
    
    @staticmethod
    def get_by_company(company_id):
        """Get all reports for a company"""
        return list(reports_collection.find({"company_id": company_id}).sort("generated_at", -1))
    
    @staticmethod
    def update(report_id, data):
        """Update a report"""
        data["updated_at"] = datetime.utcnow()
        reports_collection.update_one({"id": report_id}, {"$set": data})
        return reports_collection.find_one({"id": report_id})
    
    @staticmethod
    def delete(report_id):
        """Delete a report"""
        reports_collection.delete_one({"id": report_id})