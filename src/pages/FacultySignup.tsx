// Faculty Signup/Registration Page
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { doc, setDoc } from 'firebase/firestore';
import { auth, db } from '../config/firebase';
import './FacultySignup.css';

function FacultySignup() {
  const navigate = useNavigate();
  
  // State for form fields
  const [employeeId, setEmployeeId] = useState('');
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
    if (!employeeId || !email || !password || !confirmPassword) {
      setError('Please fill in all fields');
      return;
    }
    
    // Validation 2: Check if email ends with @psgitech.ac.in
    if (!email.endsWith('@psgitech.ac.in')) {
      setError('Email must end with @psgitech.ac.in');
      return;
    }
    
    // Validation 3: Check if passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    // Validation 4: Check password strength (minimum 6 characters)
    if (password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }
    
    setLoading(true);
    
    try {
      // Step 1: Create user account in Firebase Authentication
      // This creates login credentials
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      
      // Step 2: Store additional faculty information in Firestore database
      // doc() creates a reference to a document in the database
      // setDoc() saves data to that document
      await setDoc(doc(db, 'faculties', user.uid), {
        employeeId: employeeId,
        email: email,
        createdAt: new Date(),
        role: 'faculty'
      });
      
      // Step 3: Navigate to dashboard after successful signup
      navigate('/faculty/dashboard');
      
    } catch (err: any) {
      console.error('Signup error:', err);
      
      // Handle different error types
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
          <h1>Faculty Signup</h1>
          <p>Create your account to access the Student Portal</p>
        </div>

        <form onSubmit={handleSignup} className="signup-form">
          
          {/* Employee ID Field */}
          <div className="form-group">
            <label htmlFor="employeeId" className="form-label">
              Employee ID *
            </label>
            <input
              type="text"
              id="employeeId"
              className="form-input"
              placeholder="e.g., FAC001"
              value={employeeId}
              onChange={(e) => setEmployeeId(e.target.value)}
              disabled={loading}
            />
            <small className="form-hint">Your official employee ID</small>
          </div>

          {/* Email Field */}
          <div className="form-group">
            <label htmlFor="email" className="form-label">
              PSGiTech Email *
            </label>
            <input
              type="email"
              id="email"
              className="form-input"
              placeholder="yourname@psgitech.ac.in"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading}
            />
            <small className="form-hint">Must end with @psgitech.ac.in</small>
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

          {/* Error Message */}
          {error && <div className="error-message">{error}</div>}

          {/* Submit Button */}
          <button 
            type="submit" 
            className="btn btn-primary btn-full"
            disabled={loading}
          >
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>

          {/* Link to Login */}
          <div className="signup-footer">
            <p>
              Already have an account?{' '}
              <Link to="/faculty/login" className="link">
                Login
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}

export default FacultySignup;
