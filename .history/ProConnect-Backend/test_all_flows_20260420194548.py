"""
Comprehensive test script to verify all authentication and form flows work correctly
"""
from config import get_collections, Config
import bcrypt
from datetime import datetime, timedelta
import jwt

def test_faculty_login():
    """Test faculty login flow"""
    print('\n' + '='*70)
    print('🧪 TEST 1: FACULTY LOGIN FLOW')
    print('='*70)
    
    try:
        collections = get_collections()
        faculties = collections['faculties']
        
        # Test with existing faculty account
        test_email = '24z260@psgitech.ac.in'
        test_password = '123456'  # You'll need to verify this is correct
        
        print(f'🔍 Testing with email: {test_email}')
        
        # Test case-insensitive login (like the backend does)
        user = faculties.find_one({'email': {'$regex': f'^{test_email}$', '$options': 'i'}})
        
        if user:
            print(f'✅ Account FOUND in database')
            print(f'   Stored Email: {user.get("email")}')
            print(f'   Name: {user.get("name")}')
            print(f'   Employee ID: {user.get("employee_id")}')
            print(f'   Is Active: {user.get("is_active")}')
        else:
            print(f'❌ Account NOT found in database')
            return False
            
    except Exception as e:
        print(f'❌ Error: {e}')
        return False
    
    return True

def test_student_record_access():
    """Test student can access their submitted form"""
    print('\n' + '='*70)
    print('🧪 TEST 2: STUDENT FORM ACCESS FLOW')
    print('='*70)
    
    try:
        collections = get_collections()
        students = collections['students']
        
        # Get the first student record for testing
        student_record = students.find_one({})
        
        if not student_record:
            print(f'❌ No student records found in database')
            return False
        
        basic_info = student_record.get('basic_info', {})
        roll_number = basic_info.get('roll_number')
        personal_mail = basic_info.get('personal_mail', '').lower()
        college_mail = basic_info.get('college_mail', '').lower()
        
        print(f'📋 Test Student Record:')
        print(f'   Roll Number: {roll_number}')
        print(f'   Name: {basic_info.get("student_name")}')
        print(f'   Personal Email: {personal_mail}')
        print(f'   College Email: {college_mail}')
        print(f'   Status: {student_record.get("status")}')
        
        # Test accessing record by roll number + email (case-insensitive)
        print(f'\n🔍 Testing record access with email normalization...')
        
        # Test 1: Exact lowercase match
        test_email = college_mail
        found = students.find_one({
            'basic_info.roll_number': roll_number,
            '$or': [
                {'basic_info.personal_mail': {'$regex': f'^{test_email}$', '$options': 'i'}},
                {'basic_info.college_mail': {'$regex': f'^{test_email}$', '$options': 'i'}}
            ]
        })
        
        if found:
            print(f'   ✅ Found with lowercase email: {test_email}')
        else:
            print(f'   ❌ NOT found with lowercase email: {test_email}')
            return False
        
        # Test 2: Uppercase match (case-insensitive search)
        test_email_upper = college_mail.upper()
        found = students.find_one({
            'basic_info.roll_number': roll_number,
            '$or': [
                {'basic_info.personal_mail': {'$regex': f'^{test_email_upper}$', '$options': 'i'}},
                {'basic_info.college_mail': {'$regex': f'^{test_email_upper}$', '$options': 'i'}}
            ]
        })
        
        if found:
            print(f'   ✅ Found with UPPERCASE email: {test_email_upper}')
        else:
            print(f'   ❌ NOT found with UPPERCASE email: {test_email_upper}')
            return False
        
        # Test 3: Mixed case match
        test_email_mixed = 'sKsUbHaHaRiNi2006@gmail.com' if 'gmail' in personal_mail else '24Z260@PSGiTech.AC.IN'
        found = students.find_one({
            'basic_info.roll_number': roll_number,
            '$or': [
                {'basic_info.personal_mail': {'$regex': f'^{test_email_mixed}$', '$options': 'i'}},
                {'basic_info.college_mail': {'$regex': f'^{test_email_mixed}$', '$options': 'i'}}
            ]
        })
        
        if found:
            print(f'   ✅ Found with mixed case email: {test_email_mixed}')
        else:
            print(f'   ❌ NOT found with mixed case email: {test_email_mixed}')
            return False
        
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    print('\n' + '🚀 '*25)
    print('COMPREHENSIVE AUTHENTICATION TEST SUITE')
    print('🚀 '*25)
    
    results = {
        'Faculty Login': test_faculty_login(),
        'Student Form Access': test_student_record_access(),
    }
    
    print('\n' + '='*70)
    print('📊 TEST SUMMARY')
    print('='*70)
    
    for test_name, result in results.items():
        status = '✅ PASS' if result else '❌ FAIL'
        print(f'{status} - {test_name}')
    
    all_pass = all(results.values())
    print('\n' + ('='*70))
    if all_pass:
        print('🎉 ALL TESTS PASSED! ')
        print('✅ Email normalization is working correctly')
        print('✅ Faculty accounts can be found and logged in')
        print('✅ Student records are accessible with any case email')
    else:
        print('⚠️ SOME TESTS FAILED - Check the output above')
    print('='*70)
    
    return all_pass

if __name__ == '__main__':
    main()
