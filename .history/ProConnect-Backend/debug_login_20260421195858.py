#!/usr/bin/env python
"""Debug login issue - list all faculties"""
from config import get_collections
import bcrypt

collections = get_collections()
faculties = collections['faculties']

# List all faculty accounts
all_faculties = list(faculties.find())
print(f'Total faculties in database: {len(all_faculties)}')
print()

for i, fac in enumerate(all_faculties, 1):
    print(f'{i}. Email: {fac.get("email")}')
    print(f'   Employee ID: {fac.get("employee_id")}')
    print(f'   Active: {fac.get("is_active", True)}')
    print(f'   Role: {fac.get("role")}')
    print(f'   Password hash length: {len(fac.get("password_hash", b""))}')
    print()
