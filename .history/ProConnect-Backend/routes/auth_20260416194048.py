"""
Authentication Routes - Login, Signup, Password Reset
"""
from flask import request, jsonify
from flask_cors import cross_origin
import bcrypt
from bson.objectid import ObjectId
from datetime import datetime
from config import get_collections
from models.faculty import Faculty
from middleware.auth_middleware import generate_token
from . import auth_bp

@auth_bp.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    """
    Faculty Signup Endpoint
    
    Expected JSON:
    {
        "email": "faculty@psgitech.ac.in",
        "password": "password123",
        "employee_id": "EMP001",
        "name": "Faculty Name"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'employee_id']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        email = data.get('email').strip()
        password = data.get('password')
        employee_id = data.get('employee_id').strip()
        name = data.get('name', '').strip()
        
        # Validate email format
        if not email.endswith('@psgitech.ac.in'):
            return jsonify({'error': 'Please use your PSGiTech email address'}), 400
        
        # Validate password length
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        collections = get_collections()
        faculties = collections['faculties']
        
        # Check if email already exists
        existing_user = faculties.find_one({'email': email})
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Check if employee_id already exists
        existing_emp = faculties.find_one({'employee_id': employee_id})
        if existing_emp:
            return jsonify({'error': 'Employee ID already registered'}), 409
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create new faculty
        faculty = Faculty(
            email=email,
            password_hash=password_hash,
            employee_id=employee_id,
            name=name
        )
        
        # Insert into database
        result = faculties.insert_one(faculty.to_dict())
        
        return jsonify({
            'message': 'Signup successful',
            'user_id': str(result.inserted_id)
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    """
    Faculty Login Endpoint
    
    Expected JSON:
    {
        "email": "faculty@psgitech.ac.in",
        "password": "password123"
    }
    
    Returns:
    {
        "token": "JWT_TOKEN",
        "user": {
            "id": "USER_ID",
            "email": "faculty@psgitech.ac.in",
            "name": "Faculty Name",
            "role": "faculty"
        }
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data.get('email').strip()
        password = data.get('password')
        
        # Validate email format
        if not email.endswith('@psgitech.ac.in'):
            return jsonify({'error': 'Please use your PSGiTech email address'}), 400
        
        collections = get_collections()
        faculties = collections['faculties']
        
        # Find faculty by email
        faculty_doc = faculties.find_one({'email': email})
        if not faculty_doc:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), faculty_doc['password_hash']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if account is active
        if not faculty_doc.get('is_active', True):
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Generate JWT token
        token = generate_token(
            user_id=faculty_doc['_id'],
            email=faculty_doc['email'],
            role=faculty_doc.get('role', 'faculty')
        )
        
        # Update last login
        faculties.update_one(
            {'_id': faculty_doc['_id']},
            {'$set': {'last_login': datetime.utcnow()}}
        )
        
        # Generate refresh token (longer expiration)
        import datetime as dt
        refresh_payload = {
            'user_id': str(faculty_doc['_id']),
            'email': faculty_doc['email'],
            'role': faculty_doc.get('role', 'faculty'),
            'type': 'refresh',  # Mark as refresh token
            'exp': dt.datetime.utcnow() + dt.timedelta(days=7),  # 7 days
            'iat': dt.datetime.utcnow()
        }
        refresh_token = jwt.encode(refresh_payload, from config import Config; Config.JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'token': token,
            'refreshToken': refresh_token,
            'user': {
                'id': str(faculty_doc['_id']),
                'email': faculty_doc['email'],
                'name': faculty_doc.get('name', ''),
                'employee_id': faculty_doc.get('employee_id', ''),
                'role': faculty_doc.get('role', 'faculty')
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify-token', methods=['POST'])
@cross_origin()
def verify_token_route():
    """
    Verify JWT token validity
    
    Expects token in Authorization header:
    Authorization: Bearer <JWT_TOKEN>
    """
    try:
        token = None
        
        # Extract token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Format: "Bearer <token>"
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid authorization header'}), 401
        
        if not token:
            return jsonify({'error': 'Token is required'}), 401
        
        from middleware.auth_middleware import verify_token
        payload = verify_token(token)
        
        if payload is None:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        return jsonify({
            'valid': True,
            'user': payload
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/refresh-token', methods=['POST'])
@cross_origin()
def refresh_token():
    """
    Refresh JWT token
    
    Expected JSON:
    {
        "token": "JWT_TOKEN"
    }
    """
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Token is required'}), 400
        
        from middleware.auth_middleware import verify_token
        payload = verify_token(token)
        
        if payload is None:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Generate new token
        new_token = generate_token(
            user_id=payload['user_id'],
            email=payload['email'],
            role=payload['role']
        )
        
        return jsonify({
            'token': new_token
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
