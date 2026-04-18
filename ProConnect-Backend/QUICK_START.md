# 🎯 QUICK START - RUN BACKEND IN 3 STEPS

## ⚡ ULTRA QUICK START (2 minutes)

### Step 1️⃣: Edit .env File

Location: `d:\Siblings1-1\ProConnect-Backend\.env`

Find this line:
```
MONGODB_URI=mongodb+srv://srijaaanandhan12_db_user:<PASSWORD>@cluster0.hrjx0aa.mongodb.net/?appName=Cluster0
```

Replace `<PASSWORD>` with your actual MongoDB password and save.

---

### Step 2️⃣: Open PowerShell

Press `WIN + R` → Type `powershell` → Press Enter

Navigate to backend:
```powershell
cd d:\Siblings1-1\ProConnect-Backend
```

---

### Step 3️⃣: Activate & Run

Copy-paste this entire block:
```powershell
venv\Scripts\activate
python app.py
```

---

## ✅ YOU'RE DONE!

When you see this:
```
✓ Database: Connected to 'proconnect'
🌐 Server running at http://localhost:5000
```

**The backend is running!** 🎉

---

## 🧪 TEST IT (In New PowerShell)

```powershell
curl http://localhost:5000/api/health
```

Should see:
```json
{"status": "healthy", "message": "ProConnect Backend is running"}
```

---

## 📊 INSTALLATION VERIFICATION

```powershell
# Show all installed packages
venv\Scripts\pip list

# Should show:
# bcrypt              4.1.2
# Flask               2.3.0
# Flask-Cors          4.0.0
# PyJWT               2.8.0
# pymongo             4.6.0
# python-dotenv       1.0.0
# (+ 10 more)
```

---

## 🛑 TO STOP THE BACKEND

In the terminal running the backend:
```
Press Ctrl + C
```

The server will stop gracefully.

---

## 📱 FRONTEND + BACKEND TOGETHER

**Terminal 1 - Backend:**
```powershell
cd d:\Siblings1-1\ProConnect-Backend
venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```powershell
cd d:\Siblings1-1
npm run dev
```

---

## 🎓 WHAT EACH COMMAND DOES

| Command | Purpose |
|---------|---------|
| `venv\Scripts\activate` | Activate Python environment |
| `python app.py` | Start Flask server |
| `pip list` | Show installed packages |
| `pip install -r requirements.txt` | Install dependencies |
| `Ctrl + C` | Stop the server |
| `deactivate` | Exit virtual environment |

---

## ⚠️ COMMON MISTAKES TO AVOID

❌ **DON'T** forget to update .env with MongoDB password

❌ **DON'T** close the terminal running the backend

❌ **DON'T** skip activating virtual environment

❌ **DON'T** use Python from system directly

✅ **DO** activate virtual environment first

✅ **DO** keep terminal open while working

✅ **DO** check /api/health if unsure if it's running

---

## 🚨 IF SOMETHING GOES WRONG

### Backend won't start?
```
Error: Could not connect to MongoDB
```
→ Check .env file has correct MongoDB password

### Port already in use?
```
Address already in use
```
→ Change PORT in .env to 5001 or 5002

### Module not found?
```
ModuleNotFoundError: No module named 'flask'
```
→ Run: `pip install -r requirements.txt`

---

## ✨ FINAL CHECKLIST

Before running, verify:

- [ ] .env file exists in ProConnect-Backend folder
- [ ] MongoDB password updated in .env
- [ ] PowerShell terminal open
- [ ] Current folder is ProConnect-Backend

After running, verify:

- [ ] No error messages in terminal
- [ ] Server running message appears
- [ ] Health check endpoint works
- [ ] Backend stays running (don't close terminal)

---

**You're ready!** Type `python app.py` and go! 🚀
