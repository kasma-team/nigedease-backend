#!/bin/bash

# This script tests role-based authentication for different user roles
# It creates test users, authenticates them, and tests access to role-specific endpoints

HOST="http://localhost:8000"
BOLD="\e[1m"
GREEN="\e[32m"
RED="\e[31m"
BLUE="\e[34m"
YELLOW="\e[33m"
RESET="\e[0m"

# Role IDs from the database
SUPERADMIN_ROLE_ID="c27d70b4-548d-473c-8b7c-f807412cd0dd"
ADMIN_ROLE_ID="24911779-0d0e-4233-9827-6f959aac0d46"
SALES_ROLE_ID="ec3ad861-4250-41e6-bd76-9d420d96f1f7"
STOCK_MANAGER_ROLE_ID="7a78b133-f364-4729-bf21-06a0fc1c8d00"

echo -e "${BOLD}Role-based Authentication Testing${RESET}\n"

# Function to print colored messages
print_result() {
  if [ "$2" -eq 0 ]; then
    echo -e "${GREEN}✓ $1${RESET}"
  else
    echo -e "${RED}✗ $1${RESET}"
  fi
}

# Function to print section headers
print_section() {
  echo -e "\n${BOLD}${BLUE}$1${RESET}\n"
}

# Function to create a test user with a specific role
create_user() {
  local email=$1
  local password=$2
  local role_id=$3
  local first_name=$4
  local last_name=$5
  local company_id=$6

  print_section "Creating user: $email"

  # Create user
  RESPONSE=$(curl -s -X POST "$HOST/users/" \
    -H "Content-Type: application/json" \
    -d "{
      \"email\": \"$email\",
      \"password\": \"$password\",
      \"first_name\": \"$first_name\",
      \"last_name\": \"$last_name\",
      \"company_id\": \"$company_id\",
      \"role\": \"$role_id\"
    }")

  if echo "$RESPONSE" | grep -q "id"; then
    print_result "User $email created successfully" 0
  else
    print_result "Failed to create user $email" 1
    echo "$RESPONSE"
    return 1
  fi
}

# Function to authenticate a user and get token
authenticate() {
  local email=$1
  local password=$2
  
  echo -e "\e[1m\e[34mAuthenticating user: $email\e[0m"
  echo
  
  # Request OTP
  RESPONSE=$(curl -s -X POST "$HOST/auth/request-otp/" \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"$email\"}")
  
  if [ $? -eq 0 ]; then
    echo -e "\e[32m✓ Login successful, OTP sent\e[0m"
    echo -e "\e[33mPlease check the Docker logs for the OTP sent to $email\e[0m"
    echo -e "\e[33mDocker command: docker logs nigedease-backend-user_management_service-1 | grep 'Your OTP is' | tail -1\e[0m"
    echo
    
    # Read OTP from user input
    read -p "Enter the OTP: " OTP
    
    # Verify OTP
    RESPONSE=$(curl -s -X POST "$HOST/auth/verify-otp/" \
      -H "Content-Type: application/json" \
      -d "{
        \"email\": \"$email\",
        \"otp\": \"$OTP\"
      }")
    
    if [ $? -eq 0 ]; then
      # Extract tokens using jq
      ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access')
      REFRESH_TOKEN=$(echo "$RESPONSE" | jq -r '.refresh')
      
      echo -e "\e[32m✓ OTP verified, tokens received\e[0m"
      echo -e "Access Token: \e[33m$ACCESS_TOKEN\e[0m"
      echo "$ACCESS_TOKEN"
      return 0
    else
      echo -e "\e[31m✗ Failed to verify OTP\e[0m"
      echo "$RESPONSE"
      return 1
    fi
  else
    echo -e "\e[31m✗ Failed to request OTP\e[0m"
    echo "$RESPONSE"
    return 1
  fi
}

# Function to test access to a specific endpoint
test_endpoint() {
  local endpoint=$1
  local expected_status=$2
  local token=$3
  
  # Debug output
  echo "Using token: $token"
  echo "curl -s -X GET \"$HOST$endpoint\" -H \"Authorization: Bearer $token\" -H \"Content-Type: application/json\""
  
  # Make the request
  local response
  response=$(curl -s -X GET "$HOST$endpoint" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json")
  local status=$?
  
  # Get the HTTP status code
  local http_status=$(curl -s -o /dev/null -w "%{http_code}" "$HOST$endpoint" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json")
  
  if [ "$http_status" -eq "$expected_status" ]; then
    echo -e "\e[32m✓ Test passed\e[0m"
  else
    echo -e "\e[31m✗ Test failed (Expected status: $expected_status, Got: $http_status)\e[0m"
    echo "Response: $response"
  fi
}

# Main testing flow

# First test with existing super admin
print_section "Testing with Super Admin"
SUPERADMIN_TOKEN=$(authenticate "superadmin@example.com" "superadmin123")

if [ -n "$SUPERADMIN_TOKEN" ]; then
  # Test endpoints
  test_endpoint "/users/" 200 "$SUPERADMIN_TOKEN"
  test_endpoint "/roles/" 200 "$SUPERADMIN_TOKEN"
  test_endpoint "/permissions/" 200 "$SUPERADMIN_TOKEN"
fi

# Test with a Sales user
COMPANY_ID=$(uuidgen || python -c "import uuid; print(str(uuid.uuid4()))")
create_user "sales@example.com" "password123" "$SALES_ROLE_ID" "Sales" "User" "$COMPANY_ID"
SALES_TOKEN=$(authenticate "sales@example.com" "password123")

if [ -n "$SALES_TOKEN" ]; then
  # Test endpoints
  test_endpoint "/examples/admin-only/" 403 "$SALES_TOKEN"
  test_endpoint "/examples/sales-only/" 200 "$SALES_TOKEN"
  test_endpoint "/examples/stock-manager-only/" 403 "$SALES_TOKEN"
  test_endpoint "/examples/permission-based/" 403 "$SALES_TOKEN"
fi

# Test with a Stock Manager user
create_user "stockmanager@example.com" "password123" "$STOCK_MANAGER_ROLE_ID" "Stock" "Manager" "$COMPANY_ID"
STOCK_TOKEN=$(authenticate "stockmanager@example.com" "password123")

if [ -n "$STOCK_TOKEN" ]; then
  # Test endpoints
  test_endpoint "/examples/admin-only/" 403 "$STOCK_TOKEN"
  test_endpoint "/examples/sales-only/" 403 "$STOCK_TOKEN"
  test_endpoint "/examples/stock-manager-only/" 200 "$STOCK_TOKEN"
  test_endpoint "/examples/permission-based/" 200 "$STOCK_TOKEN"
fi

# Test with an Admin user
create_user "admin@example.com" "password123" "$ADMIN_ROLE_ID" "Admin" "User" "$COMPANY_ID"
ADMIN_TOKEN=$(authenticate "admin@example.com" "password123")

if [ -n "$ADMIN_TOKEN" ]; then
  # Test endpoints
  test_endpoint "/examples/admin-only/" 200 "$ADMIN_TOKEN"
  test_endpoint "/examples/sales-only/" 403 "$ADMIN_TOKEN"
  test_endpoint "/examples/stock-manager-only/" 403 "$ADMIN_TOKEN"
  test_endpoint "/examples/permission-based/" 200 "$ADMIN_TOKEN"
fi

echo -e "\n${BOLD}${GREEN}Testing completed!${RESET}" 