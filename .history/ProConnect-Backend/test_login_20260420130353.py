"""Test faculty login with existing account"""
from config import get_collections, Config
import bcrypt
from datetime import datetime, timedelta
import jwt

try:
    collections = get_collections()
    faculties = collections['faculties']
    
    # Test with existing account
    test_email = '24z260@psgitech.ac.in'
    test_password = '123456'  # Change this to the actual password used
    
    print(f'🔍 Testing login for: {test_email}')
    print('=' * 60)
    
    # Find by email (case-insensitive) - same as login endpoint
    user = faculties.find_one({'email': {'$regex': f'^{test_email}$', '$options': 'i'}})
    
    if not user:
        print('❌ Account NOT found in database!')
    else:
        print('✅ Account FOUND in database!')
        print(f'   Email in DB: {user.get("email")}')
        print(f'   Name: {user.get("name")}')
        print(f'   Employee ID: {user.get("employee_id")}')
        
        # Try to verify password
        stored_hash = user.get('password_hash')
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')
        
        try:
            is_correct = bcrypt.checkpw(test_password.encode('utf-8'), stored_hash)
            if is_correct:
                print(f'   ✅ Password CORRECT')
            else:
                print(f'   ❌ Password INCORRECT')
        except Exception as e:
            print(f'   ⚠️ Password verification error: {e}')
            print(f'   Stored hash type: {type(stored_hash)}')

except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
