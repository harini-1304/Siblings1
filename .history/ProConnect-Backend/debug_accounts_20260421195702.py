#!/usr/bin/env python
"""Debug - Check all faculty accounts"""
from config import get_collections

collections = get_collections()
faculties = collections['faculties']

accounts = list(faculties.find({}))
print(f'Total accounts: {len(accounts)}')
for acc in accounts:
    print(f'  - Email: {acc.get("email")}, Name: {acc.get("name")}, Active: {acc.get("is_active", True)}')

if len(accounts) == 0:
    print("No accounts found in database!")
