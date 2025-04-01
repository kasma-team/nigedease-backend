import http.server
import socketserver
import json
import os
import sys
import pymongo
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/nigedease")
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_database()

# Port to listen on
PORT = 9000

class MongoDBAPIHandler(http.server.SimpleHTTPRequestHandler):
    """Handler for MongoDB API requests"""
    
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
    
    def _error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())
    
    def do_GET(self):
        """Handle GET requests"""
        
        # Parse URL and query parameters
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Serve index page
        if path == "/":
            self._set_headers("text/html")
            html = """
            <html>
            <head>
                <title>MongoDB Test API</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    h1 { color: #2c3e50; }
                    ul { list-style-type: none; padding: 0; }
                    li { margin-bottom: 10px; }
                    a { color: #3498db; text-decoration: none; }
                    a:hover { text-decoration: underline; }
                </style>
            </head>
            <body>
                <h1>MongoDB API Test</h1>
                <p>Use these endpoints to test the MongoDB implementation:</p>
                <ul>
                    <li><a href="/api/companies">/api/companies</a> - Get all companies</li>
                    <li><a href="/api/products?company_id=YOUR_COMPANY_ID">/api/products?company_id=YOUR_COMPANY_ID</a> - Get products for a specific company</li>
                    <li><a href="/api/inventory?company_id=YOUR_COMPANY_ID">/api/inventory?company_id=YOUR_COMPANY_ID</a> - Get inventory for a specific company</li>
                </ul>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            return
        
        # Companies endpoint
        if path == "/api/companies":
            self._set_headers()
            companies = list(db.companies.find({}, {'_id': 0}))
            self.wfile.write(json.dumps(companies).encode())
            return
        
        # Products endpoint
        if path == "/api/products":
            query_params = parse_qs(parsed_url.query)
            if "company_id" not in query_params:
                self._error_response(400, "company_id parameter required")
                return
            
            company_id = query_params["company_id"][0]
            products = list(db.products.find({"company_id": company_id}, {'_id': 0}))
            self._set_headers()
            self.wfile.write(json.dumps(products).encode())
            return
        
        # Inventory endpoint
        if path == "/api/inventory":
            query_params = parse_qs(parsed_url.query)
            if "company_id" not in query_params:
                self._error_response(400, "company_id parameter required")
                return
            
            company_id = query_params["company_id"][0]
            
            # Get all stores for this company
            stores = list(db.stores.find({"company_id": company_id}, {'_id': 0}))
            store_ids = [store['id'] for store in stores]
            
            # Get inventory for all company stores
            inventory = []
            for store_id in store_ids:
                store_inventory = list(db.inventory.find({"store_id": store_id}, {'_id': 0}))
                inventory.extend(store_inventory)
            
            self._set_headers()
            self.wfile.write(json.dumps(inventory).encode())
            return
        
        # If no endpoint matched, return 404
        self._error_response(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests"""
        
        # Parse URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Get request body
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
        except json.JSONDecodeError:
            self._error_response(400, "Invalid JSON")
            return
        
        # Create company endpoint
        if path == "/api/companies":
            if "name" not in data:
                self._error_response(400, "name parameter required")
                return
            
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
            self._set_headers()
            self.wfile.write(json.dumps(company).encode())
            return
        
        # If no endpoint matched, return 404
        self._error_response(404, "Endpoint not found")
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

if __name__ == "__main__":
    # Start the server
    with socketserver.TCPServer(("", PORT), MongoDBAPIHandler) as httpd:
        print(f"MongoDB API Test server running at http://localhost:{PORT}")
        httpd.serve_forever() 