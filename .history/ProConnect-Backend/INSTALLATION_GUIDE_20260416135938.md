# 🚀 COMPLETE SETUP & RUN INSTRUCTIONS

## ✅ Installation Status: COMPLETE!

All required Python packages have been successfully installed:

```
✓ Flask                2.3.0    - Web framework
✓ Flask-CORS           4.0.0    - Cross-Origin Resource Sharing
✓ pymongo              4.6.0    - MongoDB driver
✓ python-dotenv        1.0.0    - Environment variables
✓ PyJWT                2.8.0    - JWT tokens
✓ bcrypt               4.1.2    - Password hashing
+ All dependencies     14 total packages installed
```

---

## 📋 STEP-BY-STEP INSTRUCTIONS TO RUN

### STEP 1: Verify MongoDB Connection String (IMPORTANT!)

**File to Edit:** `.env` in `d:\Siblings1-1\ProConnect-Backend\`

**What to do:**
1. Open `.env` file with any text editor
2. Find this line:
   ```
   MONGODB_URI=mongodb+srv://srijaaanandhan12_db_user:<db_password>@cluster0.hrjx0aa.mongodb.net/?appName=Cluster0
   ```
3. Replace `<db_password>` with your actual MongoDB password
4. Save the file

**Example (after update):**
```
MONGODB_URI=mongodb+srv://srijaaanandhan12_db_user:MyActualPassword123@cluster0.hrjx0aa.mongodb.net/?appName=Cluster0
```

⚠️ **CRITICAL**: If you don't update this, the backend won't connect to MongoDB!

---

### STEP 2: Open Terminal/PowerShell

**On Windows:**
1. Press `WIN + R`
2. Type `powershell`
3. Press Enter

Or open VS Code and use integrated terminal (Ctrl + `)

---

### STEP 3: Navigate to Backend Folder

**Type this command:**
```bash
cd d:\Siblings1-1\ProConnect-Backend
```

**Press Enter**

You should see:
```
PS D:\Siblings1-1\ProConnect-Backend>
```

---

### STEP 4: Activate Virtual Environment

**Type this command:**
```bash
venv\Scripts\activate
```

**Press Enter**

You should see the prompt change to:
```
(venv) PS D:\Siblings1-1\ProConnect-Backend>
```

Notice the `(venv)` at the beginning - this means the virtual environment is active ✓

---

### STEP 5: Verify Packages Are Installed

**Type this command:**
```bash
pip list
```

**Press Enter**

You should see all 16 packages listed (Flask, pymongo, PyJWT, bcrypt, etc.)

If you see all packages → You're good to go! ✓

---

### STEP 6: Start the Backend Server

**Type this command:**
```bash
python app.py
```

**Press Enter**

---

### 🎉 EXPECTED OUTPUT:

You should see something like this:

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

API Endpoints:
  POST   /api/auth/signup              - Faculty signup
  POST   /api/auth/login               - Faculty login
  POST   /api/auth/verify-token        - Verify JWT token
  POST   /api/auth/refresh-token       - Refresh JWT token
  POST   /api/students/submit          - Submit student form
  GET    /api/students                 - Get all students
  GET    /api/students/<id>            - Get single student
  PUT    /api/students/<id>            - Update student
  DELETE /api/students/<id>            - Delete student
  GET    /api/faculty/profile          - Get faculty profile
  POST   /api/faculty/change-password  - Change password
  GET    /api/faculty/stats            - Get statistics
  GET    /api/health                   - Health check
============================================================
```

✅ **If you see this, the backend is running!**

---

## ✅ VERIFY IT'S WORKING

### Method 1: Test Health Endpoint (Recommended)

**In another PowerShell/Terminal window, type:**

```bash
curl http://localhost:5000/api/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "message": "ProConnect Backend is running",
  "version": "1.0.0"
}
```

If you see this → Backend is working! ✓

---

### Method 2: Use Browser

1. Open any web browser
2. Go to: `http://localhost:5000/api/health`
3. You should see JSON response

---

### Method 3: Test Login Endpoint

**In PowerShell, type:**
```powershell
$body = @{
    email = "test@psgitech.ac.in"
    password = "testpass"
} | ConvertTo-Json

curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -Body $body
```

Expected: Error (account doesn't exist yet) OR success with token

---

## 📊 COMPLETE INSTALLATION CHECKLIST

- [x] Python 3.11.9 installed ✓
- [x] Virtual environment created ✓
- [x] All 16 packages installed ✓
  - Flask 2.3.0 ✓
  - Flask-CORS 4.0.0 ✓
  - pymongo 4.6.0 ✓
  - PyJWT 2.8.0 ✓
  - bcrypt 4.1.2 ✓
  - python-dotenv 1.0.0 ✓
  - + 10 other dependencies ✓
- [ ] .env file updated with MongoDB password (DO THIS NOW!)
- [ ] Backend started with `python app.py`
- [ ] Health check endpoint tested

---

## 🔧 TROUBLESHOOTING

### Problem 1: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
1. Make sure virtual environment is activated: `(venv)` should be visible
2. Run: `pip install -r requirements.txt`

---

### Problem 2: "Port 5000 is already in use"

**Solution:**
1. Close any other application using port 5000
2. Or change PORT in `.env` to `5001` or `5002`

---

### Problem 3: "Cannot connect to MongoDB"

**Solution:**
1. Check `.env` file - MONGODB_URI must have correct password
2. Verify MongoDB password is correct
3. Check Internet connection
4. Check MongoDB Atlas IP whitelist (allow 0.0.0.0/0)

---

### Problem 4: Virtual environment won't activate

**Solution:**
```bash
# Try this instead:
venv\Scripts\python.exe -m pip list
```

---

## 🎯 QUICK COMMANDS REFERENCE

```bash
# Activate virtual environment
venv\Scripts\activate

# Deactivate virtual environment
deactivate

# Start backend
python app.py

# Install a new package
pip install package_name

# List installed packages
pip list

# View backend logs
# (They appear automatically in terminal)

# Stop backend
Ctrl + C

# Check Python version
python --version
```

---

## 📡 API TESTING

### Using REST Client Extension (VS Code)

1. Install "REST Client" extension in VS Code
2. Open file: `API_TESTS.rest`
3. Click "Send Request" above any endpoint

### Using Postman

1. Open Postman
2. Import `API_TESTS.rest` file
3. Select any request
4. Click "Send"

### Using Browser

Visit: `http://localhost:5000/api/health`

---

## 🎓 UNDERSTANDING THE SETUP

### What is a Virtual Environment?

A virtual environment is an isolated Python workspace where:
- Packages are installed separately
- Different projects can have different versions
- Doesn't affect system Python

Think of it like: Creating a sandbox just for this project.

### What are the Packages?

| Package | Purpose |
|---------|---------|
| Flask | Web framework (creates the API) |
| Flask-CORS | Allows frontend to talk to backend |
| pymongo | Connects to MongoDB database |
| PyJWT | Creates and validates authentication tokens |
| bcrypt | Securely hashes passwords |
| python-dotenv | Reads .env configuration file |

---

## 🚀 NEXT STEPS AFTER BACKEND IS RUNNING

1. ✅ **Backend is running** (you are here!)

2. **Test the API** (10 minutes)
   - Use API_TESTS.rest to test endpoints
   - Create a faculty account
   - Test login
   - Submit a student form

3. **Update React Frontend** (1-2 hours)
   - Read MIGRATION_GUIDE.md
   - Remove Firebase
   - Install Axios
   - Update components

4. **Deploy** (30 minutes)
   - Deploy backend to cloud
   - Deploy frontend to Netlify/Vercel

---

## ✨ SUCCESS SIGNS

✅ Backend is working correctly if:

1. Terminal shows no error messages
2. Server running message appears
3. `http://localhost:5000/api/health` returns JSON
4. No red/error text in terminal

❌ Something's wrong if:

1. Terminal shows "Error", "ModuleNotFoundError", or "Exception"
2. Server doesn't start
3. Health check returns "Connection refused"

---

## 📝 ENVIRONMENT VARIABLES EXPLAINED

Located in `.env` file:

```env
# Flask Settings
FLASK_ENV=development          # development or production
FLASK_DEBUG=True              # Enable debug mode (restart on file change)
SECRET_KEY=...                # Secret key for Flask

# MongoDB Settings
MONGODB_URI=...               # Connection string to MongoDB
DB_NAME=proconnect           # Database name

# Authentication Settings
JWT_SECRET=...                # Secret key for JWT tokens
JWT_EXPIRATION_HOURS=24       # How long token lasts

# Server Settings
HOST=localhost               # Server address
PORT=5000                    # Server port
```

---

## 🔐 SECURITY NOTES

- Never commit `.env` to Git (already in .gitignore)
- Keep MongoDB password secret
- Change JWT_SECRET and SECRET_KEY for production
- Don't share these credentials

---

## 📚 DOCUMENTATION FILES

| File | Purpose |
|------|---------|
| README.md | Complete API documentation |
| MIGRATION_GUIDE.md | How to update React frontend |
| QUICK_REFERENCE.md | Commands cheat sheet |
| API_TESTS.rest | API test examples |

---

## 🎉 YOU'RE ALL SET!

**Current Status:**
- ✅ Python 3.11.9 installed
- ✅ Virtual environment created
- ✅ All 16 packages installed
- ✅ Backend ready to run

**Next Action:**
1. Update `.env` with MongoDB password
2. Run: `python app.py`
3. Test: `curl http://localhost:5000/api/health`

---

## 💡 PRO TIPS

1. **Keep terminal open** while backend is running
2. **Don't close** the terminal - it stops the backend
3. **Activate venv every time** you open new terminal
4. **Changes to code** auto-reload in debug mode
5. **Use Ctrl+C** to stop the server gracefully

---

**Created:** April 16, 2024
**Status:** ✅ Installation Complete - Ready to Run
**Version:** 1.0.0

---

**Ready to start? Type:** `python app.py` in the terminal! 🚀
