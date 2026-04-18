# 🔄 Firebase to MongoDB Migration Guide

Complete step-by-step guide to update your React frontend from Firebase to MongoDB + Flask backend.

## Overview of Changes

| Aspect | Firebase | New (MongoDB + Flask) |
|--------|----------|----------------------|
| Authentication | Firebase Auth SDK | JWT Tokens + Axios |
| Database | Firestore | MongoDB |
| Backend | None (serverless) | Flask REST API |
| API Calls | Firebase SDK methods | HTTP requests |
| Data Storage | Client & Firestore | Server (MongoDB) |

---

## Phase 1: Setup Frontend Dependencies

### Step 1: Remove Firebase
```bash
cd path/to/your/frontend
npm uninstall firebase
```

### Step 2: Install Axios
```bash
npm install axios
```

---

## Phase 2: Create API Service Layer

Create file: `src/services/api.ts`

```typescript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const token = localStorage.getItem('authToken');
        if (token) {
          const response = await api.post('/api/auth/refresh-token', { token });
          const newToken = response.data.token;
          localStorage.setItem('authToken', newToken);
          
          api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
          originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
          
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        window.location.href = '/faculty/login';
      }
    }

    return Promise.reject(error);
  }
);

// ============================================================
// AUTHENTICATION APIS
// ============================================================

export const authAPI = {
  signup: (email: string, password: string, employeeId: string, name: string) =>
    api.post('/api/auth/signup', { email, password, employee_id: employeeId, name }),

  login: (email: string, password: string) =>
    api.post('/api/auth/login', { email, password }),

  verifyToken: (token: string) =>
    api.post('/api/auth/verify-token', { token }),

  refreshToken: (token: string) =>
    api.post('/api/auth/refresh-token', { token }),
};

// ============================================================
// STUDENT APIS
// ============================================================

export const studentAPI = {
  submitForm: (formData: any) =>
    api.post('/api/students/submit', formData),

  getAllStudents: (branch?: string, section?: string, page = 1, limit = 10) => {
    const params = new URLSearchParams();
    if (branch) params.append('branch', branch);
    if (section) params.append('section', section);
    params.append('page', page.toString());
    params.append('limit', limit.toString());
    
    return api.get(`/api/students?${params.toString()}`);
  },

  getStudent: (studentId: string) =>
    api.get(`/api/students/${studentId}`),

  updateStudent: (studentId: string, formData: any) =>
    api.put(`/api/students/${studentId}`, formData),

  deleteStudent: (studentId: string) =>
    api.delete(`/api/students/${studentId}`),
};

// ============================================================
// FACULTY APIS
// ============================================================

export const facultyAPI = {
  getProfile: () =>
    api.get('/api/faculty/profile'),

  changePassword: (currentPassword: string, newPassword: string) =>
    api.post('/api/faculty/change-password', { 
      current_password: currentPassword, 
      new_password: newPassword 
    }),

  getStats: () =>
    api.get('/api/faculty/stats'),
};

export default api;
```

### Step 3: Create `.env.local`

Add to your frontend's `.env.local`:
```
VITE_API_URL=http://localhost:5000
```

---

## Phase 3: Update Authentication Components

### Update `src/pages/FacultyLogin.tsx`

**BEFORE (Firebase):**
```typescript
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../config/firebase';

const handleLogin = async (e: React.FormEvent) => {
  e.preventDefault();
  const userCredential = await signInWithEmailAndPassword(auth, email, password);
  navigate('/faculty/dashboard');
};
```

**AFTER (API):**
```typescript
import { authAPI } from '../services/api';

const handleLogin = async (e: React.FormEvent) => {
  e.preventDefault();
  setError('');
  setLoading(true);
  
  try {
    const response = await authAPI.login(email, password);
    
    // Store token and user data
    localStorage.setItem('authToken', response.data.token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    
    navigate('/faculty/dashboard');
  } catch (err: any) {
    setError(err.response?.data?.error || 'Login failed');
  } finally {
    setLoading(false);
  }
};
```

### Update `src/pages/FacultySignup.tsx`

**BEFORE (Firebase):**
```typescript
import { createUserWithEmailAndPassword } from 'firebase/auth';

const handleSignup = async (e: React.FormEvent) => {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
};
```

**AFTER (API):**
```typescript
import { authAPI } from '../services/api';

const handleSignup = async (e: React.FormEvent) => {
  e.preventDefault();
  setError('');
  setLoading(true);
  
  try {
    await authAPI.signup(email, password, employeeId, name);
    // Show success message
    alert('Signup successful! Please login.');
    navigate('/faculty/login');
  } catch (err: any) {
    setError(err.response?.data?.error || 'Signup failed');
  } finally {
    setLoading(false);
  }
};
```

---

## Phase 4: Update Student Form

### Update `src/pages/StudentForm.tsx`

**BEFORE (Firebase):**
```typescript
import { collection, addDoc } from 'firebase/firestore';
import { db } from '../config/firebase';

const handleSubmit = async () => {
  const docRef = await addDoc(collection(db, 'students'), formData);
  console.log('Document written with ID:', docRef.id);
};
```

**AFTER (API):**
```typescript
import { studentAPI } from '../services/api';

const handleSubmit = async () => {
  setLoading(true);
  try {
    const response = await studentAPI.submitForm({
      basic_info: {
        student_name: studentName,
        roll_number: rollNumber,
        // ... other fields
      },
      parent_details: {
        mother: mother,
        father: father,
        guardian: guardian,
      },
      siblings: siblings,
      relatives: relativesInIT,
    });
    
    console.log('Form submitted with ID:', response.data.student_id);
    // Show success message and redirect
    setCurrentStep(4); // Success step
  } catch (err: any) {
    setError(err.response?.data?.error || 'Failed to submit form');
  } finally {
    setLoading(false);
  }
};
```

---

## Phase 5: Update Dashboard

### Update `src/pages/FacultyDashboard.tsx`

**BEFORE (Firebase):**
```typescript
import { collection, query, getDocs } from 'firebase/firestore';
import { db } from '../config/firebase';

const fetchStudents = async () => {
  const q = query(collection(db, 'students'));
  const querySnapshot = await getDocs(q);
  const data = querySnapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data()
  }));
  setStudents(data);
};
```

**AFTER (API):**
```typescript
import { studentAPI } from '../services/api';

const fetchStudents = async (branch?: string, section?: string) => {
  setLoading(true);
  try {
    const response = await studentAPI.getAllStudents(branch, section, currentPage, itemsPerPage);
    setStudents(response.data.students);
    setTotal(response.data.total);
  } catch (err) {
    setError('Failed to fetch students');
  } finally {
    setLoading(false);
  }
};

const handleDeleteStudent = async (studentId: string) => {
  if (!window.confirm('Are you sure?')) return;
  
  try {
    await studentAPI.deleteStudent(studentId);
    fetchStudents(); // Refresh list
  } catch (err) {
    setError('Failed to delete student');
  }
};
```

---

## Phase 6: Update Protected Route

### Update `src/components/ProtectedRoute.tsx`

**BEFORE (Firebase):**
```typescript
import { onAuthStateChanged } from 'firebase/auth';
import { auth, db } from '../config/firebase';

useEffect(() => {
  const unsubscribe = onAuthStateChanged(auth, async (user) => {
    if (!user) {
      navigate('/faculty/login');
      return;
    }
    // Check role in Firestore
  });
}, []);
```

**AFTER (API):**
```typescript
import { authAPI } from '../services/api';

useEffect(() => {
  const checkAuth = async () => {
    const token = localStorage.getItem('authToken');
    const user = localStorage.getItem('user');
    
    if (!token || !user) {
      navigate('/faculty/login');
      return;
    }
    
    try {
      // Verify token is still valid
      await authAPI.verifyToken(token);
      const userData = JSON.parse(user);
      
      if (userData.role === requiredRole) {
        setIsAuthorized(true);
      } else {
        setIsAuthorized(false);
        navigate('/faculty/login');
      }
    } catch (err) {
      navigate('/faculty/login');
    }
  };
  
  checkAuth();
}, [navigate, requiredRole]);
```

---

## Phase 7: Update Header Component (Logout)

### Update `src/components/Header.tsx`

**BEFORE (Firebase):**
```typescript
import { signOut } from 'firebase/auth';
import { auth } from '../config/firebase';

const handleLogout = async () => {
  await signOut(auth);
  navigate('/faculty/login');
};
```

**AFTER (API):**
```typescript
const handleLogout = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('user');
  navigate('/faculty/login');
};
```

---

## Phase 8: Delete Firebase Config

### Remove `src/config/firebase.ts`

This file is no longer needed. You can delete it safely.

---

## Phase 9: Update package.json Scripts

In your main `package.json`, you might want to add a script to run both frontend and backend:

```json
{
  "scripts": {
    "dev": "vite",
    "dev:all": "concurrently \"npm run dev\" \"npm --prefix ../ProConnect-Backend run dev\"",
    "build": "tsc && vite build",
    "preview": "vite preview"
  }
}
```

Then install concurrently:
```bash
npm install --save-dev concurrently
```

---

## Complete Code Example

### Full Updated FacultyLogin.tsx

```typescript
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import './FacultyLogin.css';

function FacultyLogin() {
  const navigate = useNavigate();
  const [employeeId, setEmployeeId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!employeeId || !password) {
      setError('Please fill in all fields');
      return;
    }

    const email = employeeId.includes('@') 
      ? employeeId 
      : `${employeeId}@psgitech.ac.in`;

    if (!email.endsWith('@psgitech.ac.in')) {
      setError('Please use your PSGiTech email address');
      return;
    }

    setLoading(true);

    try {
      const response = await authAPI.login(email, password);
      
      // Store token and user info
      localStorage.setItem('authToken', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      navigate('/faculty/dashboard');
    } catch (err: any) {
      const errorMsg = err.response?.data?.error;
      setError(errorMsg || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <h2>Faculty Login</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email or Employee ID"
          value={employeeId}
          onChange={(e) => setEmployeeId(e.target.value)}
          disabled={loading}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p>
        Don't have an account? <Link to="/faculty/signup">Sign up</Link>
      </p>
    </div>
  );
}

export default FacultyLogin;
```

---

## Testing Checklist

- [ ] Remove Firebase imports from all files
- [ ] Install axios
- [ ] Create API service layer
- [ ] Update all API calls
- [ ] Test faculty login
- [ ] Test student form submission
- [ ] Test faculty dashboard
- [ ] Test logout functionality
- [ ] Test token refresh
- [ ] Remove firebase.ts config file
- [ ] Update .env with backend URL

---

## Common Issues & Solutions

### CORS Errors
**Problem:** `No 'Access-Control-Allow-Origin'` header
**Solution:** Backend already has CORS enabled. Ensure frontend URL matches allowed origins in `app.py`

### Token Not Sent
**Problem:** API returns 401 Unauthorized
**Solution:** Check localStorage.getItem('authToken') has correct token

### API Not Found
**Problem:** `404 Not Found`
**Solution:** Verify backend is running on `http://localhost:5000`

### Data Not Saving
**Problem:** Student form submits but data doesn't appear
**Solution:** Check MongoDB connection in backend logs

---

## Summary

You've successfully migrated from Firebase to MongoDB + Flask! 

**Old Stack:**
- ❌ Firebase Authentication
- ❌ Firestore Database
- ❌ Client-side data storage

**New Stack:**
- ✅ JWT Token Authentication
- ✅ MongoDB Database
- ✅ Flask REST API Backend
- ✅ Axios HTTP Client

Your application is now ready for production deployment!

