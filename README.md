# Nigedease Backend - MongoDB Transition

This repository contains the backend services for Nigedease, which have been transitioned from Django ORM to MongoDB for data persistence.

## Services

The backend consists of two main services:

1. **User Management Service** (Port 8000)
   - Handles user authentication, registration, and company management
   - Manages roles and permissions

2. **Core Service** (Port 8001)
   - Financial management (companies, expenses, payments, etc.)
   - Product management (products, categories, units)
   - Inventory management (stores, stock)

## MongoDB Transition

The application has been fully transitioned from Django ORM to MongoDB:

- Data is now stored in MongoDB collections instead of SQL tables
- Django models have been replaced with static classes containing CRUD methods
- Django's ModelViewSet classes have been replaced with ViewSet classes
- Serializers have been updated to work with MongoDB documents

## Setup and Installation

### Prerequisites

- Python 3.8+
- MongoDB (local or remote)
- pip (Python package manager)
- Docker and Docker Compose (recommended for easy setup)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/nigedease-backend.git
   cd nigedease-backend
   ```

2. Using Docker (recommended):
   ```
   docker-compose up -d
   ```
   
   This will start both services and MongoDB in containers.

3. Manual installation:
   ```
   pip install -r requirements.txt
   ```

4. Environment setup:
   - Create `.env` files in both service directories with your MongoDB connection string and other environment variables
   - Example for `.env` files:
     ```
     MONGODB_URI=mongodb://localhost:27017/nigedease
     SECRET_KEY=your-secret-key
     DEBUG=True
     ```

## Running the Services

### Using Docker (recommended)
```
docker-compose up -d
```

### Manual Start

#### User Management Service
```
cd user_management_service
python manage.py runserver 8000
```

#### Core Service
```
cd core_service
python manage.py runserver 8001
```

## API Documentation

Both services provide Swagger UI documentation for their APIs:

- User Management Service: `http://localhost:8000/api-docs/`
- Core Service: `http://localhost:8001/api-docs/`

## API Endpoints

### User Management Service

- `/auth/login/` - User login
- `/auth/verify-token/` - Token verification
- `/users/` - User CRUD operations
- `/roles/` - Role management
- `/permissions/` - Permission management

### Core Service

#### Financial Endpoints
- `/financial/banks/` - Bank account management
- `/financial/companies/` - Company operations
- `/financial/currencies/` - Currency management
- `/financial/paymentmodes/` - Payment mode management
- `/financial/paymentins/` - Payment in operations
- `/financial/paymentouts/` - Payment out operations
- `/financial/reports/` - Financial reports
- `/financial/subscriptionplans/` - Subscription plan management

#### Product Endpoints
- `/product/products/` - Product management
- `/product/categories/` - Product categories
- `/product/units/` - Product units

#### Inventory Endpoints
- `/inventory/stores/` - Store management
- `/inventory/inventory/` - Inventory tracking

## Notes on MongoDB Implementation

1. Each Django model has been converted to a class with static methods
2. Collections are defined at the top of each models.py file
3. Document IDs are stored as strings using ObjectId from MongoDB
4. Foreign key relationships are maintained via ID references
5. Each class implements standard CRUD operations:
   - `create()` - Creates a new document
   - `get_by_id()` - Retrieves a document by ID
   - `get_by_company()` - Gets documents for a specific company
   - `update()` - Updates a document
   - `delete()` - Removes a document

## Authentication

All endpoints except for the authentication endpoints and API documentation require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

You can obtain a token by sending a POST request to `/auth/login/` with valid credentials 