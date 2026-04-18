"""
Authentication Routes - Login, Signup, Password Reset
"""
from flask import request, jsonify
from flask_cors import cross_origin
import bcrypt
import jwt
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from config import get_collections, Config
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
        refresh_payload = {
            'user_id': str(faculty_doc['_id']),
            'email': faculty_doc['email'],
            'role': faculty_doc.get('role', 'faculty'),
            'type': 'refresh',  # Mark as refresh token
            'exp': datetime.utcnow() + timedelta(days=7),  # 7 days
            'iat': datetime.utcnow()
        }
        refresh_token_str = jwt.encode(refresh_payload, Config.JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'token': token,
            'refreshToken': refresh_token_str,
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
    Refresh JWT access token using refresh token
    
    Expected JSON:
    {
        "refreshToken": "REFRESH_TOKEN"
    }
    """
    try:
        data = request.get_json()
        refresh_token_str = data.get('refreshToken')
        
        if not refresh_token_str:
            return jsonify({'error': 'Refresh token is required'}), 400
        
        from middleware.auth_middleware import verify_token
        payload = verify_token(refresh_token_str)
        
        if payload is None:
            return jsonify({'error': 'Invalid or expired refresh token'}), 401
        
        # Check if this is actually a refresh token
        if payload.get('type') != 'refresh':
            return jsonify({'error': 'Invalid token type'}), 401
        
        # Generate new access token
        new_token = generate_token(
            user_id=payload['user_id'],
            email=payload['email'],
            role=payload['role']
        )
        
        return jsonify({
            'token': new_token,
            'refreshToken': refresh_token_str  # Return same refresh token
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/forgot-password', methods=['POST'])
@cross_origin()
def forgot_password():
    """
    Request password reset email
    
    Expected JSON:
    {
        "email": "faculty@psgitech.ac.in"
    }
    """
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        collections = get_collections()
        faculty_collection = collections['faculty']
        
        # Check if user exists
        user = faculty_collection.find_one({'email': email})
        
        if not user:
            # Don't reveal if email exists or not (security best practice)
            # Still return success to prevent email enumeration
            return jsonify({
                'message': 'If the email exists, a password reset link will be sent shortly.'
            }), 200
        
        # Generate password reset token (valid for 30 minutes)
        reset_token = jwt.encode({
            'user_id': str(user['_id']),
            'email': email,
            'type': 'password_reset',
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, Config.JWT_SECRET, algorithm='HS256')
        
        # Send reset email
        try:
            reset_link = f"http://localhost:5173/reset-password?token={reset_token}"
            
            # Get email configuration from environment
            sender_email = os.getenv('SENDER_EMAIL')
            sender_password = os.getenv('SENDER_PASSWORD')
            smtp_server_addr = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', 587))
            
            if not sender_email or not sender_password:
                print("⚠️ Email credentials not configured in .env file")
                # Still return success to user - don't send email if not configured
                return jsonify({
                    'message': 'If the email exists, a password reset link will be sent shortly.'
                }), 200
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = 'ProConnect - Password Reset Request'
            
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2 style="color: #2c3e50;">Password Reset Request</h2>
                    <p>Hi {user.get('name', 'Faculty Member')},</p>
                    <p>We received a request to reset your ProConnect password. Click the link below to reset it:</p>
                    
                    <p style="margin: 30px 0;">
                        <a href="{reset_link}" style="background-color: #3498db; color: white; padding: 12px 30px; text-decoration: none; border-radius: 4px; display: inline-block;">
                            Reset Password
                        </a>
                    </p>
                    
                    <p>Or copy this link in your browser:</p>
                    <p style="word-break: break-all; color: #7f8c8d;">{reset_link}</p>
                    
                    <p style="color: #e74c3c; font-size: 12px;">This link will expire in 30 minutes.</p>
                    
                    <hr style="border: none; border-top: 1px solid #ecf0f1; margin: 20px 0;">
                    
                    <p style="font-size: 12px; color: #7f8c8d;">
                        If you didn't request this, please ignore this email or contact support.
                    </p>
                    
                    <p style="font-size: 12px; color: #7f8c8d;">
                        Best regards,<br>
                        ProConnect Team
                    </p>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email via SMTP
            print(f"📧 Attempting to send reset email to {email}...")
            with smtplib.SMTP(smtp_server_addr, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            
            print(f"✅ Password reset email sent to {email}")
            
        except Exception as email_error:
            print(f"⚠️ Failed to send email: {str(email_error)}")
            # Still return success to user even if email fails
            # (in production, you'd want better logging/monitoring)
        
        return jsonify({
            'message': 'If the email exists, a password reset link will be sent shortly.'
        }), 200
    
    except Exception as e:
        print(f"❌ Error in forgot_password: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@auth_bp.route('/reset-password', methods=['POST'])
@cross_origin()
def reset_password():
    """
    Reset password using reset token
    
    Expected JSON:
    {
        "token": "RESET_TOKEN",
        "newPassword": "newpassword123"
    }
    """
    try:
        data = request.get_json()
        reset_token = data.get('token')
        new_password = data.get('newPassword')
        
        if not reset_token or not new_password:
            return jsonify({'error': 'Token and new password are required'}), 400
        
        if len(new_password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Verify reset token
        from middleware.auth_middleware import verify_token
        payload = verify_token(reset_token)
        
        if payload is None:
            return jsonify({'error': 'Invalid or expired reset token'}), 401
        
        # Check if this is a password reset token
        if payload.get('type') != 'password_reset':
            return jsonify({'error': 'Invalid token type'}), 401
        
        collections = get_collections()
        faculty_collection = collections['faculty']
        
        # Hash new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        # Update password
        result = faculty_collection.update_one(
            {'_id': ObjectId(payload['user_id'])},
            {'$set': {
                'password': hashed_password,
                'updated_at': datetime.utcnow()
            }}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'message': 'Password reset successful. Please login with your new password.'
        }), 200
    
    except Exception as e:
        print(f"Error in reset_password: {str(e)}")
        return jsonify({'error': str(e)}), 500
