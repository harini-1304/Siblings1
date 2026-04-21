"""Debug script to check faculty accounts in MongoDB"""
from config import get_collections

try:
    collections = get_collections()
    faculties = collections['faculties']
    
    # Get all faculty records
    all_faculties = list(faculties.find({}))
    
    print('📊 All Faculty Accounts in Database:')
    print('=' * 60)
    for faculty in all_faculties:
        print(f'  Email: {faculty.get("email")}')
        print(f'  Name: {faculty.get("name")}')
        print(f'  Employee ID: {faculty.get("employee_id")}')
        print(f'  Is Active: {faculty.get("is_active")}')
        print(f'  Created: {faculty.get("created_at")}')
        print('-' * 60)
    
    print(f'Total: {len(all_faculties)} faculty records')
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
