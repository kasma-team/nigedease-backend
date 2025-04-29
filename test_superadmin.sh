#!/bin/bash

# A simple script to test the superadmin access to role-specific endpoints

HOST="http://localhost:8000"
BOLD="\e[1m"
GREEN="\e[32m"
RED="\e[31m"
BLUE="\e[34m"
YELLOW="\e[33m"
RESET="\e[0m"

echo -e "${BOLD}Testing Super Admin Role Access${RESET}\n"

# Function to print colored messages
print_result() {
  if [ "$2" -eq 0 ]; then
    echo -e "${GREEN}✓ $1${RESET}"
  else
    echo -e "${RED}✗ $1${RESET}"
  fi
}

# Login with superadmin
echo -e "${BLUE}Logging in as superadmin@example.com${RESET}"
RESPONSE=$(curl -s -X POST "$HOST/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "superadmin@example.com",
    "password": "superadmin123"
  }')

if echo "$RESPONSE" | grep -q "OTP sent"; then
  echo -e "${GREEN}Login successful, OTP sent to email${RESET}"
  echo -e "${YELLOW}Check Docker logs: docker logs nigedease-backend-user_management_service-1 | grep 'Your OTP is' | tail -1${RESET}"
  
  read -p "Enter the OTP: " OTP
  
  # Verify OTP
  echo -e "${BLUE}Verifying OTP...${RESET}"
  RESPONSE=$(curl -s -X POST "$HOST/auth/verify-otp/" \
    -H "Content-Type: application/json" \
    -d "{
      \"email\": \"superadmin@example.com\",
      \"otp\": \"$OTP\"
    }")
  
  if echo "$RESPONSE" | grep -q "access"; then
    ACCESS_TOKEN=$(echo "$RESPONSE" | grep -oP "\"access\":\s*\"\K[^\"]+")
    echo -e "${GREEN}OTP verified, access token received${RESET}"
    
    # Test endpoints
    echo -e "\n${BOLD}Testing endpoints with Superadmin token:${RESET}"
    
    # Admin endpoint
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
      -X GET "$HOST/examples/admin-only/" \
      -H "Authorization: Bearer $ACCESS_TOKEN")
    print_result "Superadmin accessing Admin endpoint (status: $STATUS)" $([[ $STATUS -eq 200 ]] && echo 0 || echo 1)
    
    # Sales endpoint
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
      -X GET "$HOST/examples/sales-only/" \
      -H "Authorization: Bearer $ACCESS_TOKEN")
    print_result "Superadmin accessing Sales endpoint (status: $STATUS)" $([[ $STATUS -eq 200 ]] && echo 0 || echo 1)
    
    # Stock Manager endpoint
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
      -X GET "$HOST/examples/stock-manager-only/" \
      -H "Authorization: Bearer $ACCESS_TOKEN")
    print_result "Superadmin accessing Stock Manager endpoint (status: $STATUS)" $([[ $STATUS -eq 200 ]] && echo 0 || echo 1)
    
    # Permission-based endpoint
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
      -X GET "$HOST/examples/permission-based/" \
      -H "Authorization: Bearer $ACCESS_TOKEN")
    print_result "Superadmin accessing Permission-based endpoint (status: $STATUS)" $([[ $STATUS -eq 200 ]] && echo 0 || echo 1)
    
  else
    echo -e "${RED}Failed to verify OTP${RESET}"
    echo "$RESPONSE"
  fi
else
  echo -e "${RED}Login failed${RESET}"
  echo "$RESPONSE"
fi 