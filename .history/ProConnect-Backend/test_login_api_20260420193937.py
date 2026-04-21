"""Test the complete login flow for an existing account"""
import requests
import json

BASE_URL = 'http://localhost:5000/api'

# Test with existing account
test_email = '24z260@psgitech.ac.in'
test_password = '123456'  # Update with the actual password

print('🧪 Testing Faculty Login Flow')
print('=' * 60)

# Step 1: Try to login
print(f'\n1️⃣ Attempting login with email: {test_email}')
try:
    response = requests.post(
        f'{BASE_URL}/auth/login',
        json={
            'email': test_email,
            'password': test_password
        }
    )
    print(f'   Status Code: {response.status_code}')
    data = response.json()
    print(f'   Response: {json.dumps(data, indent=2)}')
    
    if response.status_code == 200:
        print('   ✅ LOGIN SUCCESSFUL!')
    else:
        print(f'   ❌ Login failed: {data.get("error")}')
        
except Exception as e:
    print(f'   ❌ Error: {e}')

print('\n' + '=' * 60)
