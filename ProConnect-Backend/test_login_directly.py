#!/usr/bin/env python
"""Test login API directly"""
import requests
import json

BASE_URL = 'http://localhost:5000/api'

# Test credentials
test_emails = [
    '24z260@psgitech.ac.in',
    'test@psgitech.ac.in',
    '24z258@psgitech.ac.in'
]

passwords = ['password123', 'test123', 'Password@123']

print("Testing login endpoints...")
print("=" * 60)

for email in test_emails:
    print(f"\nTesting: {email}")
    for pwd in passwords:
        try:
            response = requests.post(
                f'{BASE_URL}/auth/login',
                json={
                    'email': email,
                    'password': pwd
                },
                timeout=5
            )
            
            print(f"  Password '{pwd}': {response.status_code}")
            data = response.json()
            if response.status_code == 200:
                print(f"    ✅ SUCCESS!")
            else:
                print(f"    Error: {data.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"  ❌ Exception: {e}")
