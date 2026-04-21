"""Debug script to check student records in MongoDB"""
from config import get_collections

try:
    collections = get_collections()
    students = collections['students']
    
    # Get all student records
    all_students = list(students.find({}))
    
    print('📊 All Student Records in Database:')
    print('=' * 60)
    for student in all_students:
        basic_info = student.get('basic_info', {})
        print(f'  Student Name: {basic_info.get("student_name")}')
        print(f'  Roll Number: {basic_info.get("roll_number")}')
        print(f'  Email (Personal): {basic_info.get("personal_mail")}')
        print(f'  Email (College): {basic_info.get("college_mail")}')
        print(f'  Status: {student.get("status")}')
        print(f'  Created: {student.get("created_at")}')
        print('-' * 60)
    
    print(f'Total: {len(all_students)} student records')
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
