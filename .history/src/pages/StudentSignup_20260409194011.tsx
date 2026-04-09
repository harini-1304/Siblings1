// Student Signup/Registration Page
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { doc, setDoc } from 'firebase/firestore';
import { auth, db } from '../config/firebase';
import './FacultySignup.css'; // Reuse styling

function StudentSignup() {
  const navigate = useNavigate();
  
  // State for form fields
  const [rollNumber, setRollNumber] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Function to handle signup
  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    // Validation 1: Check if all fields are filled
    if (!rollNumber || !email || !password || !confirmPassword) {
      setError('Please fill in all fields');
      return;
    }
    
    // Validation 2: Check password strength (minimum 6 characters)
    if (password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }
    
    // Validation 3: Check if passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    setLoading(true);
    
    try {
      // Step 1: Create user account in Firebase Authentication
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      
      // Step 2: Store user role and info in 'users' collection
      await setDoc(doc(db, 'users', user.uid), {
        role: 'student',
        email: email,
        rollNumber: rollNumber,
        createdAt: new Date()
      });
      
      // Step 3: Navigate to form after successful signup
      navigate('/student/form');
      
    } catch (err: any) {
      console.error('Signup error:', err);
      
      if (err.code === 'auth/email-already-in-use') {
        setError('This email is already registered. Please login instead.');
      } else if (err.code === 'auth/weak-password') {
        setError('Password is too weak. Please use a stronger password.');
      } else if (err.code === 'auth/invalid-email') {
        setError('Invalid email format.');
      } else {
        setError('Signup failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-card">
        <div className="signup-header">
          <h1>Student Registration</h1>
          <p>Create your account to fill the student form</p>
        </div>

        <form onSubmit={handleSignup} className="signup-form">
          
          {/* Roll Number Field */}
          <div className="form-group">
            <label htmlFor="rollNumber" className="form-label">
              Roll Number *
            </label>
            <input
              type="text"
              id="rollNumber"
              className="form-input"
              placeholder="e.g., 22B001"
              value={rollNumber}
              onChange={(e) => setRollNumber(e.target.value)}
              disabled={loading}
            />
          </div>

          {/* Email Field */}
          <div className="form-group">
            <label htmlFor="email" className="form-label">
              Email *
            </label>
            <input
              type="email"
              id="email"
              className="form-input"
              placeholder="your.email@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading}
            />
          </div>

          {/* Password Field */}
          <div className="form-group">
            <label htmlFor="password" className="form-label">
              Password *
            </label>
            <input
              type="password"
              id="password"
              className="form-input"
              placeholder="Minimum 6 characters"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
            />
          </div>

          {/* Confirm Password Field */}
          <div className="form-group">
            <label htmlFor="confirmPassword" className="form-label">
              Confirm Password *
            </label>
            <input
              type="password"
              id="confirmPassword"
              className="form-input"
              placeholder="Re-enter your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              disabled={loading}
            />
          </div>

          {/* Error Message Display */}
          {error && <div className="error-message">{error}</div>}

          {/* Submit Button */}
          <button
            type="submit"
            className="btn btn-primary btn-block"
            disabled={loading}
          >
            {loading ? 'Creating account...' : 'Register & Continue'}
          </button>
        </form>

        {/* Link to login */}
        <p className="auth-footer">
          Already have an account?{' '}
          <Link to="/student/login" className="auth-link">
            Student Login
          </Link>
        </p>
      </div>
    </div>
  );
}

export default StudentSignup;
