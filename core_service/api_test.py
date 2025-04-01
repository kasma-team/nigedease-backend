from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import yaml
import json
import os
import sys
from dotenv import load_dotenv
import uuid
from datetime import datetime
import pymongo

# Load environment variables
load_dotenv()

# Configure MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/nigedease")
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_database()

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)

# Create static folder if it doesn't exist
os.makedirs('static', exist_ok=True)

# Create Swagger spec
swagger_spec = {
    "openapi": "3.0.0",
    "info": {
        "title": "Nigedease MongoDB API",
        "description": "API for testing MongoDB transition",
        "version": "1.0.0"
    },
    "servers": [
        {
            "url": "http://localhost:8080",
            "description": "Development server"
        }
    ],
    "paths": {
        "/api/companies": {
            "get": {
                "summary": "Get all companies",
                "responses": {
                    "200": {
                        "description": "List of companies",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Company"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Create a new company",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/CompanyInput"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Company created",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Company"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/companies/{id}": {
            "get": {
                "summary": "Get company by ID",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Company details",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Company"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Company not found"
                    }
                }
            }
        },
        "/api/products": {
            "get": {
                "summary": "Get all products",
                "parameters": [
                    {
                        "name": "company_id",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "List of products",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Product"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/inventory": {
            "get": {
                "summary": "Get inventory for a company",
                "parameters": [
                    {
                        "name": "company_id",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "List of inventory items",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Inventory"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Company": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "address": {"type": "string"},
                    "email": {"type": "string"},
                    "phone_number": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            },
            "CompanyInput": {
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string"},
                    "address": {"type": "string"},
                    "email": {"type": "string"},
                    "phone_number": {"type": "string"}
                }
            },
            "Product": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "category_id": {"type": "string"},
                    "unit_id": {"type": "string"},
                    "company_id": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            },
            "Inventory": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "product_id": {"type": "string"},
                    "store_id": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        }
    }
}

# Write Swagger spec to file
with open('static/swagger.json', 'w') as f:
    json.dump(swagger_spec, f)

# Configure Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Nigedease MongoDB API"
    }
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Serve swagger.json
@app.route('/static/swagger.json')
def serve_swagger():
    return send_from_directory('static', 'swagger.json')

# API Routes
@app.route('/api/companies', methods=['GET'])
def get_companies():
    companies = list(db.companies.find({}, {'_id': 0}))
    return jsonify(companies)

@app.route('/api/companies', methods=['POST'])
def create_company():
    data = request.json
    company = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "address": data.get("address"),
        "email": data.get("email"),
        "phone_number": data.get("phone_number"),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    db.companies.insert_one(company)
    return jsonify(company), 201

@app.route('/api/companies/<id>', methods=['GET'])
def get_company(id):
    company = db.companies.find_one({"id": id}, {'_id': 0})
    if not company:
        return jsonify({"error": "Company not found"}), 404
    return jsonify(company)

@app.route('/api/products', methods=['GET'])
def get_products():
    company_id = request.args.get('company_id')
    if not company_id:
        return jsonify({"error": "company_id parameter required"}), 400
    products = list(db.products.find({"company_id": company_id}, {'_id': 0}))
    return jsonify(products)

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    company_id = request.args.get('company_id')
    if not company_id:
        return jsonify({"error": "company_id parameter required"}), 400
    
    # Get all stores for this company
    stores = list(db.stores.find({"company_id": company_id}, {'_id': 0}))
    store_ids = [store['id'] for store in stores]
    
    # Get inventory for all company stores
    inventory = []
    for store_id in store_ids:
        store_inventory = list(db.inventory.find({"store_id": store_id}, {'_id': 0}))
        inventory.extend(store_inventory)
    
    return jsonify(inventory)

@app.route('/')
def index():
    return """
    <h1>MongoDB API Test</h1>
    <p>Go to <a href='/swagger'>Swagger UI</a> to test the API</p>
    <h2>Available Endpoints:</h2>
    <ul>
        <li><a href='/api/companies'>/api/companies</a> - GET all companies</li>
        <li>/api/companies/{id} - GET a specific company</li>
        <li>/api/products?company_id={company_id} - GET products for a company</li>
        <li>/api/inventory?company_id={company_id} - GET inventory for a company</li>
    </ul>
    """

if __name__ == '__main__':
    app.run(debug=True, port=8080) 