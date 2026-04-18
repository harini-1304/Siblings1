// Student Signup/Registration Page
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './FacultySignup.css'; // Reuse styling

function StudentSignup() {
  const navigate = useNavigate();
  
  // State for form fields
  const [rollNumber, setRollNumber] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Function to handle signup
  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    // Validation 1: Check if all fields are filled
    if (!rollNumber || !email) {
      setError('Please fill in all fields');
      return;
    }
    
    setLoading(true);
    
    try {
      // Store student info in sessionStorage for reference
      sessionStorage.setItem('studentRollNumber', rollNumber);
      sessionStorage.setItem('studentEmail', email);
      
      // Navigate to form
      navigate('/student/form');
      
    } catch (err: any) {
      console.error('Signup error:', err);
      setError('Failed to proceed. Please try again.');
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
