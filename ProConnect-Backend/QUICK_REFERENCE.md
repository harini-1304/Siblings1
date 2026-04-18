# 🚀 ProConnect Backend - Quick Reference Card

## ⚡ Quick Start (5 minutes)

```bash
# 1. Edit .env - Add your MongoDB password
# Replace <PASSWORD> with actual password

# 2. Run setup
setup.bat          # Windows
./setup.sh         # macOS/Linux

# 3. Start backend
python app.py

# 4. Test health
curl http://localhost:5000/api/health
```

---

## 🔑 Key Commands

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

# Run with Gunicorn (production)
pip install gunicorn
gunicorn app:app

# Deactivate environment
deactivate
```

---

## 📡 API Endpoints

### Authentication
```
POST   /api/auth/signup          Register new faculty
POST   /api/auth/login           Login & get JWT token
POST   /api/auth/verify-token    Check token validity
POST   /api/auth/refresh-token   Get new token
```

### Students
```
POST   /api/students/submit      Submit student form
GET    /api/students             Get all students (faculty)
GET    /api/students/<id>        Get single student (faculty)
PUT    /api/students/<id>        Update student (faculty)
DELETE /api/students/<id>        Delete student (faculty)
```

### Faculty
```
GET    /api/faculty/profile              Get faculty profile
POST   /api/faculty/change-password      Change password
GET    /api/faculty/stats                Get statistics
```

### Health
```
GET    /api/health               Health check
```

---

## 🔐 Authentication Header

```bash
Authorization: Bearer <JWT_TOKEN_HERE>

# Example:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📤 Example Requests

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "faculty@psgitech.ac.in",
    "password": "password123"
  }'
```

### Submit Student Form
```bash
curl -X POST http://localhost:5000/api/students/submit \
  -H "Content-Type: application/json" \
  -d '{
    "basic_info": {
      "student_name": "John Doe",
      "roll_number": "19BCE001"
    },
    "parent_details": {...},
    "siblings": [],
    "relatives": []
  }'
```

### Get All Students (with auth)
```bash
curl http://localhost:5000/api/students \
  -H "Authorization: Bearer <TOKEN>"
```

---

## 🗄️ MongoDB Collections

```
proconnect
├── faculties          Faculty user accounts
├── students           Student form submissions
└── users              (Reserved for future)
```

---

## 🔧 Environment Variables

```env
MONGODB_URI=mongodb+srv://user:pass@cluster...  # Connection string
DB_NAME=proconnect                              # Database name
JWT_SECRET=your-secret-key                      # Token key
FLASK_ENV=development                           # Environment
FLASK_DEBUG=True                                # Debug mode
HOST=localhost                                  # Server host
PORT=5000                                       # Server port
```

---

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| MongoDB connection failed | Check .env MONGODB_URI and password |
| Port 5000 in use | `netstat -ano \| findstr :5000` then kill process |
| Module not found | Run `pip install -r requirements.txt` |
| CORS errors | Ensure frontend URL matches in app.py |
| Token expired | Use `/api/auth/refresh-token` endpoint |

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| app.py | Start here - Main Flask app |
| config.py | Database connection |
| routes/auth.py | Login & signup endpoints |
| routes/students.py | Student form endpoints |
| routes/faculty.py | Faculty operations |
| .env | Configuration (UPDATE THIS!) |
| requirements.txt | Python dependencies |

---

## 🧪 Testing

### Using REST Client Extension
1. Install "REST Client" in VS Code
2. Open `API_TESTS.rest`
3. Click "Send Request"

### Using Postman
1. Create new request
2. Set method and URL
3. Add headers: `Content-Type: application/json`
4. For protected routes: `Authorization: Bearer <TOKEN>`
5. Add JSON body
6. Send request

### Using cURL
```bash
curl -X GET http://localhost:5000/api/health
```

---

## 🚀 Deployment

### Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### AWS
```bash
# Use Gunicorn + Nginx + Supervisor
gunicorn app:app --bind 0.0.0.0:5000
```

### Local Server
```bash
python app.py
```

---

## 📊 Database Backup

### MongoDB Atlas
1. Go to https://cloud.mongodb.com
2. Navigate to your cluster
3. Click "Backup" tab
4. Create backup snapshot

### Local Export
```bash
mongodump --uri "mongodb+srv://user:pass@cluster..."
mongorestore --uri "mongodb+srv://user:pass@cluster..." dump/
```

---

## 🔍 Debug Mode

### Enable Logging
```python
# In Flask app
app.logger.info("Message")
app.logger.error("Error")
```

### Check MongoDB
1. Use MongoDB Compass GUI
2. View collections and documents
3. Run queries directly

### View Flask Logs
```
[2024-04-16 10:30:00] GET /api/students - 200 OK
[2024-04-16 10:31:00] POST /api/auth/login - 401 Unauthorized
```

---

## 📋 Setup Checklist

- [ ] Extract backend files
- [ ] Edit .env with MongoDB password
- [ ] Run setup.bat or setup.sh
- [ ] Run python app.py
- [ ] See "Server running" message
- [ ] Test /api/health endpoint
- [ ] Test /api/auth/login endpoint
- [ ] Check MongoDB Compass for data
- [ ] Ready for frontend migration!

---

## 🎯 Next Steps

1. **Backend Ready** ✅
   - Run `python app.py`
   - Test endpoints

2. **Frontend Migration** (See MIGRATION_GUIDE.md)
   - Remove Firebase
   - Install Axios
   - Create API service
   - Update components

3. **Deploy**
   - Deploy backend to cloud
   - Deploy frontend to Netlify/Vercel
   - Point frontend to backend URL

---

## 📚 Documentation

- **README.md** - Complete documentation
- **MIGRATION_GUIDE.md** - Frontend update guide
- **SETUP_COMPLETE.md** - Setup instructions
- **FILE_SUMMARY.md** - File reference

---

## 💡 Tips

- Keep .env secure (don't commit to Git)
- JWT tokens expire in 24 hours
- Use HTTPS in production
- Monitor MongoDB usage
- Enable production mode for deployment
- Use Gunicorn for production (not Flask dev server)

---

## 📞 Help

**Backend not starting?**
1. Check Python version: `python --version`
2. Check MongoDB connection in .env
3. Check .env file exists in correct location
4. Check port 5000 is not in use

**API returning 401?**
1. Check token in localStorage
2. Verify token format: `Authorization: Bearer <TOKEN>`
3. Check token expiration
4. Use refresh-token endpoint

**CORS errors?**
1. Check frontend URL in app.py CORS config
2. Ensure correct headers sent from frontend
3. Check browser console for exact error

---

## ⚡ Performance Tips

- MongoDB indexes on frequently searched fields
- Pagination for large result sets
- Caching for statistics endpoint
- Use Gunicorn with multiple workers
- Enable gzip compression
- Monitor slow queries

---

**Version**: 1.0.0  
**Last Updated**: April 16, 2024  
**Status**: ✅ Production Ready
