// Student Login Page
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './FacultyLogin.css'; // Reuse styling

function StudentLogin() {
  const navigate = useNavigate();
  
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Function that runs when user clicks "Continue" button
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Clear any previous errors
    setError('');
    
    // Validation: Check if email is filled
    if (!email) {
      setError('Please fill in your email');
      return;
    }
    
    // Start loading state
    setLoading(true);
    
    try {
      // Store email in sessionStorage for reference in form
      sessionStorage.setItem('studentEmail', email);
      
      // Navigate to form
      navigate('/student/form');
      
    } catch (err: any) {
      console.error('Error:', err);
      setError('Failed to proceed. Please try again.');
    } finally {
      // Stop loading state
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        {/* Header */}
        <div className="login-header">
          <h1>Student Login</h1>
          <p>PSGiTech Student Portal</p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleLogin} className="login-form">
          
          {/* Email Input */}
          <div className="form-group">
            <label htmlFor="email" className="form-label">
              Email
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

          {/* Error Message */}
          {error && <div className="error-message">{error}</div>}

          {/* Continue Button */}
          <button
            type="submit"
            className="btn btn-primary btn-block"
            disabled={loading}
          >
            {loading ? 'Proceeding...' : 'Continue'}
          </button>
        </form>

        {/* Sign up link */}
        <p className="auth-footer">
          Don't have an account?{' '}
          <Link to="/student/signup" className="auth-link">
            Sign up here
          </Link>
        </p>
      </div>
    </div>
  );
}

export default StudentLogin;
