#!/usr/bin/env python
"""List all faculty accounts"""
from config import get_collections

collections = get_collections()
faculties = collections['faculties']

all_faculty = list(faculties.find())
print('All Faculty Accounts:')
print('=' * 60)
if all_faculty:
    for faculty in all_faculty:
        email = faculty.get('email', 'N/A')
        emp_id = faculty.get('employee_id', 'N/A')
        active = faculty.get('is_active', True)
        created = faculty.get('created_at', 'N/A')
        print(f'Email: {email}')
        print(f'Employee ID: {emp_id}')
        print(f'Active: {active}')
        print(f'Created: {created}')
        print('-' * 60)
else:
    print('❌ No faculty accounts found')
