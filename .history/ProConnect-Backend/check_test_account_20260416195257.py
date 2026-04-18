#!/usr/bin/env python
"""Check if test faculty account exists"""
from config import get_collections
import bcrypt

collections = get_collections()
faculties = collections['faculties']

user = faculties.find_one({'email': 'test@psgitech.ac.in'})
if user:
    print('✅ Test faculty account found:')
    print(f'   Email: {user["email"]}')
    print(f'   Employee ID: {user["employee_id"]}')
    print(f'   Password hash exists: {"password_hash" in user}')
    print(f'   Active: {user.get("is_active", True)}')
    
    # Test password verification
    test_password = 'password123'
    if bcrypt.checkpw(test_password.encode('utf-8'), user['password_hash']):
        print(f'   ✅ Password verification: SUCCESS with "password123"')
    else:
        print(f'   ❌ Password verification: FAILED with "password123"')
else:
    print('❌ Test faculty account NOT found')
    print('   Creating new test account...')
    
    password_hash = bcrypt.hashpw(b'password123', bcrypt.gensalt())
    result = faculties.insert_one({
        'email': 'test@psgitech.ac.in',
        'password_hash': password_hash,
        'employee_id': 'EMP001',
        'name': 'Test Faculty',
        'role': 'faculty',
        'is_active': True
    })
    print(f'   ✅ New account created with ID: {result.inserted_id}')
