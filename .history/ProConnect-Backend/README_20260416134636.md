# ProConnect Backend - Flask + MongoDB

## Overview
Flask REST API backend for ProConnect application with MongoDB database integration.

## Technology Stack
- **Framework**: Flask 2.3.0
- **Database**: MongoDB (via PyMongo)
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **CORS**: Enabled for cross-origin requests

## Project Structure
```
ProConnect-Backend/
├── app.py                      # Main Flask application
├── config.py                   # Configuration & database connection
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── models/
│   ├── __init__.py
│   ├── faculty.py             # Faculty model
│   └── student.py             # Student model
├── routes/
│   ├── __init__.py
│   ├── auth.py                # Authentication endpoints
│   ├── students.py            # Student CRUD endpoints
│   └── faculty.py             # Faculty-specific endpoints
├── middleware/
│   ├── __init__.py
│   └── auth_middleware.py     # JWT authentication middleware
└── README.md                  # This file
```

## Prerequisites
- Python 3.8 or higher
- MongoDB connection (local or cloud)
- pip (Python package manager)

## Installation

### 1. Clone/Navigate to Backend Directory
```bash
cd ProConnect-Backend
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Edit the `.env` file with your MongoDB credentials:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here

# MongoDB Connection
MONGODB_URI=mongodb+srv://srijaaanandhan12_db_user:<db_password>@cluster0.hrjx0aa.mongodb.net/?appName=Cluster0

# Database Name
DB_NAME=proconnect

# JWT Configuration
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRATION_HOURS=24

# Server Configuration
HOST=localhost
PORT=5000
```

**Important**: Replace `<db_password>` with your actual MongoDB password.

### 5. Run the Backend
```bash
python app.py
```

You should see:
```
============================================================
🚀 ProConnect Backend Starting...
============================================================
✓ Database: Connected to 'proconnect'
✓ Environment: development
✓ Debug Mode: True
============================================================
🌐 Server running at http://localhost:5000
============================================================
```

## API Endpoints

### Authentication Routes (`/api/auth`)

#### Faculty Signup
```
POST /api/auth/signup
Content-Type: application/json

{
  "email": "faculty@psgitech.ac.in",
  "password": "password123",
  "employee_id": "EMP001",
  "name": "Faculty Name"
}

Response (201):
{
  "message": "Signup successful",
  "user_id": "507f1f77bcf86cd799439011"
}
```

#### Faculty Login
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "faculty@psgitech.ac.in",
  "password": "password123"
}

Response (200):
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "faculty@psgitech.ac.in",
    "name": "Faculty Name",
    "employee_id": "EMP001",
    "role": "faculty"
  }
}
```

#### Verify Token
```
POST /api/auth/verify-token
Content-Type: application/json

{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}

Response (200):
{
  "valid": true,
  "user": {
    "user_id": "507f1f77bcf86cd799439011",
    "email": "faculty@psgitech.ac.in",
    "role": "faculty",
    "exp": 1234567890,
    "iat": 1234567800
  }
}
```

#### Refresh Token
```
POST /api/auth/refresh-token
Content-Type: application/json

{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}

Response (200):
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Student Routes (`/api/students`)

#### Submit Student Form
```
POST /api/students/submit
Content-Type: application/json

{
  "basic_info": {
    "student_name": "John Doe",
    "roll_number": "19BCE001",
    "mobile_no": "9876543210",
    "parent_mobile": "9876543211",
    "personal_mail": "john@email.com",
    "college_mail": "john@psgtech.ac.in",
    "branch": "CSE",
    "section": "A",
    "year": "4"
  },
  "parent_details": {
    "mother": {...},
    "father": {...},
    "guardian": {...}
  },
  "siblings": [...],
  "relatives": [...]
}

Response (201):
{
  "message": "Form submitted successfully",
  "student_id": "507f1f77bcf86cd799439011",
  "is_update": false
}
```

#### Get All Students (Faculty Only)
```
GET /api/students?branch=CSE&section=A&page=1&limit=10
Authorization: Bearer <JWT_TOKEN>

Response (200):
{
  "students": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "basic_info": {...},
      "parent_details": {...},
      "siblings": [...],
      "relatives": [...],
      "created_at": "2024-04-16T10:30:00",
      "updated_at": "2024-04-16T10:30:00",
      "status": "submitted"
    }
  ],
  "total": 45,
  "page": 1,
  "limit": 10,
  "pages": 5
}
```

#### Get Single Student (Faculty Only)
```
GET /api/students/<student_id>
Authorization: Bearer <JWT_TOKEN>

Response (200):
{
  "_id": "507f1f77bcf86cd799439011",
  "basic_info": {...},
  "parent_details": {...},
  "siblings": [...],
  "relatives": [...],
  "created_at": "2024-04-16T10:30:00",
  "updated_at": "2024-04-16T10:30:00",
  "status": "submitted"
}
```

#### Update Student (Faculty Only)
```
PUT /api/students/<student_id>
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "basic_info": {...},
  "parent_details": {...},
  "siblings": [...],
  "relatives": [...]
}

Response (200):
{
  "message": "Student record updated successfully"
}
```

#### Delete Student (Faculty Only)
```
DELETE /api/students/<student_id>
Authorization: Bearer <JWT_TOKEN>

Response (200):
{
  "message": "Student record deleted successfully"
}
```

### Faculty Routes (`/api/faculty`)

#### Get Faculty Profile
```
GET /api/faculty/profile
Authorization: Bearer <JWT_TOKEN>

Response (200):
{
  "id": "507f1f77bcf86cd799439011",
  "email": "faculty@psgitech.ac.in",
  "name": "Faculty Name",
  "employee_id": "EMP001",
  "role": "faculty",
  "is_active": true,
  "created_at": "2024-04-16T10:30:00",
  "last_login": "2024-04-16T11:30:00"
}
```

#### Change Password
```
POST /api/faculty/change-password
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "current_password": "oldpassword",
  "new_password": "newpassword"
}

Response (200):
{
  "message": "Password changed successfully"
}
```

#### Get Statistics
```
GET /api/faculty/stats
Authorization: Bearer <JWT_TOKEN>

Response (200):
{
  "total_students": 150,
  "by_branch": [
    {
      "_id": "CSE",
      "count": 45
    },
    {
      "_id": "ECE",
      "count": 30
    }
  ],
  "by_year": [
    {
      "_id": "4",
      "count": 40
    },
    {
      "_id": "3",
      "count": 35
    }
  ],
  "recent_submissions": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "basic_info": {
        "student_name": "John Doe",
        "roll_number": "19BCE001"
      },
      "created_at": "2024-04-16T11:30:00"
    }
  ]
}
```

### Health Check
```
GET /api/health

Response (200):
{
  "status": "healthy",
  "message": "ProConnect Backend is running",
  "version": "1.0.0"
}
```

## Authentication

### How JWT Works

1. **Login**: User sends credentials → Server returns JWT token
2. **Store Token**: Client stores token in localStorage
3. **Send Requests**: Client includes token in Authorization header
4. **Verify**: Server verifies token before processing request

### Authorization Header Format
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## MongoDB Collections

### Collections Created Automatically

#### `faculties` Collection
```json
{
  "_id": ObjectId,
  "email": "faculty@psgitech.ac.in",
  "password_hash": "bcrypt_hashed_password",
  "employee_id": "EMP001",
  "name": "Faculty Name",
  "role": "faculty",
  "is_active": true,
  "created_at": ISODate,
  "last_login": ISODate
}
```

#### `students` Collection
```json
{
  "_id": ObjectId,
  "basic_info": {
    "student_name": "John Doe",
    "roll_number": "19BCE001",
    "branch": "CSE",
    "section": "A",
    "year": "4",
    "mobile_no": "9876543210",
    "personal_mail": "john@email.com",
    "college_mail": "john@psgtech.ac.in"
  },
  "parent_details": {
    "mother": {...},
    "father": {...},
    "guardian": {...}
  },
  "siblings": [...],
  "relatives": [...],
  "created_at": ISODate,
  "updated_at": ISODate,
  "status": "submitted"
}
```

## Development Tips

### 1. Testing Endpoints
Use Postman or VS Code REST Client:

```http
### Health Check
GET http://localhost:5000/api/health

### Faculty Login
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "email": "faculty@psgitech.ac.in",
  "password": "password123"
}
```

### 2. Enable Debug Mode
Set `FLASK_DEBUG=True` in `.env` for auto-reload on file changes.

### 3. View MongoDB Data
Use MongoDB Compass or Atlas UI to inspect collections and documents.

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 app:app
```

### Environment Variables for Production
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<strong-random-key>
JWT_SECRET=<strong-random-key>
```

### Deploy to Heroku
```bash
# Install Heroku CLI
# Then:
heroku create proconnect-backend
git push heroku main
```

## Troubleshooting

### MongoDB Connection Failed
- Check your connection string in `.env`
- Verify MongoDB password (no special characters without escaping)
- Check IP whitelist in MongoDB Atlas

### CORS Errors
- Add your frontend URL to the CORS configuration in `app.py`
- Ensure proper headers are sent from frontend

### JWT Token Expired
- Token expires after 24 hours (configurable in `.env`)
- Use `/api/auth/refresh-token` to get a new token

## Next Steps

1. ✅ Backend created
2. **Next**: Update React frontend to use this API
3. **Then**: Remove Firebase dependencies from React
4. **Finally**: Deploy backend and frontend

## Support

For issues or questions, check the project documentation or logs.

---

**Last Updated**: April 16, 2024
**Version**: 1.0.0
