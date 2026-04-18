#!/usr/bin/env python
"""
Create a test faculty account for testing login functionality
"""
import bcrypt
from datetime import datetime
from config import get_collections

def create_test_faculty():
    """Create test faculty account in MongoDB"""
    collections = get_collections()
    faculties = collections['faculties']
    
    # Test credentials
    test_email = 'test@psgitech.ac.in'
    test_password = 'password123'
    test_employee_id = 'EMP001'
    
    # Check if account already exists
    existing = faculties.find_one({'email': test_email})
    if existing:
        print('✅ Faculty account already exists!')
        print(f'   Email: {test_email}')
        print(f'   Password: password123')
        print(f'   Employee ID: {test_employee_id}')
        return
    
    # Hash password
    password_hash = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt())
    
    # Insert faculty
    result = faculties.insert_one({
        'email': test_email,
        'password_hash': password_hash,
        'employee_id': test_employee_id,
        'name': 'Test Faculty',
        'role': 'faculty',
        'is_active': True,
        'created_at': datetime.utcnow()
    })
    
    print('✅ Faculty account created successfully!')
    print(f'   Email: {test_email}')
    print(f'   Password: {test_password}')
    print(f'   Employee ID: {test_employee_id}')
    print(f'   User ID: {result.inserted_id}')

if __name__ == '__main__':
    create_test_faculty()
