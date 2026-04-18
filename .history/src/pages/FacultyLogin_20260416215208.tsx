// Faculty Login Page
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import './FacultyLogin.css';

function FacultyLogin() {
  // useNavigate: Hook to programmatically navigate to other pages
  const navigate = useNavigate();
  
  // useState: Hook to store and update data in the component
  // Syntax: const [variableName, functionToUpdateIt] = useState(initialValue);
  
  const [employeeId, setEmployeeId] = useState('');  // Stores employee ID input
  const [password, setPassword] = useState('');      // Stores password input
  const [error, setError] = useState('');            // Stores error messages
  const [loading, setLoading] = useState(false);     // Shows loading state during login
  const [showForgotPassword, setShowForgotPassword] = useState(false);  // Toggle forgot password modal
  const [resetEmail, setResetEmail] = useState('');  // Stores email for password reset
  const [resetMessage, setResetMessage] = useState('');  // Success message
  const [resetError, setResetError] = useState('');  // Reset error message
  const [resetLoading, setResetLoading] = useState(false);  // Loading state for password reset

  // Function that runs when user clicks "Login" button
  const handleLogin = async (e: React.FormEvent) => {
    // Prevent the form from refreshing the page (default browser behavior)
    e.preventDefault();
    
    // Clear any previous errors
    setError('');
    
    // Validation: Check if fields are filled
    if (!employeeId || !password) {
      setError('Please fill in all fields');
      return;  // Stop here if validation fails
    }
    
    // Validation: Check if email ends with @psgitech.ac.in
    const email = employeeId.includes('@') ? employeeId : `${employeeId}@psgitech.ac.in`;
    
    if (!email.endsWith('@psgitech.ac.in')) {
      setError('Please use your PSGiTech email address');
      return;
    }
    
    // Start loading state
    setLoading(true);
    
    try {
      // Call backend API to login
      const response = await authAPI.facultyLogin(email, password);
      
      console.log('Login successful:', response);
      
      // Dispatch a custom event to notify other components that login happened
      // This helps the Header component update without requiring a refresh
      window.dispatchEvent(new Event('authTokenUpdated'));
      
      // Navigate to faculty dashboard
      navigate('/faculty/dashboard');
      
    } catch (err: any) {
      // If login fails, show error message
      console.error('Login error:', err);
      
      // Show user-friendly error messages based on error response
      const errorMsg = err.response?.data?.message || err.message;
      
      if (errorMsg.includes('not found')) {
        setError('No account found with this email. Please sign up first.');
      } else if (errorMsg.includes('password') || errorMsg.includes('credentials')) {
        setError('Incorrect password. Please try again.');
      } else if (errorMsg.includes('email')) {
        setError('Invalid email format.');
      } else {
        setError(errorMsg || 'Login failed. Please try again.');
      }
    } finally {
      // Stop loading state (runs whether success or failure)
      setLoading(false);
    }
  };

  // Function to handle password reset
  const handleForgotPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setResetError('');
    setResetMessage('');
    
    // Validation: Check if email is filled
    if (!resetEmail) {
      setResetError('Please enter your email');
      return;
    }
    
    // Format email with domain if not already present
    const email = resetEmail.includes('@') ? resetEmail : `${resetEmail}@psgitech.ac.in`;
    
    try {
      setResetLoading(true);
      setResetError('');
      setResetMessage('');
      
      // Call API to request password reset
      await authAPI.requestPasswordReset(email);
      
      // Show success message
      setResetMessage('✅ Password reset email sent! Check your inbox for the reset link.');
      setResetEmail('');
      
      // Close modal after 4 seconds
      setTimeout(() => setShowForgotPassword(false), 4000);
    } catch (err: any) {
      console.error('Reset error:', err);
      const errorMsg = err.response?.data?.error || 'Error processing reset request. Please try again.';
      setResetError(errorMsg);
    } finally {
      setResetLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        {/* Header */}
        <div className="login-header">
          <h1>Faculty Login</h1>
          <p>PSGiTech Student Portal</p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleLogin} className="login-form">
          
          {/* Employee ID / Email Input */}
          <div className="form-group">
            <label htmlFor="employeeId" className="form-label">
              Email
            </label>
            <input
              type="text"
              id="employeeId"
              className="form-input"
              placeholder="e.g name@psgitech.ac.in"
              value={employeeId}
              onChange={(e) => setEmployeeId(e.target.value)}
              disabled={loading}
            />
          </div>

          {/* Password Input */}
          <div className="form-group">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              id="password"
              className="form-input"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
            />
          </div>

          {/* Error Message (only shows if there's an error) */}
          {error && <div className="error-message">{error}</div>}

          {/* Submit Button */}
          <button 
            type="submit" 
            className="btn btn-primary btn-full"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>

          {/* Forgot Password Link */}
          <button
            type="button"
            className="forgot-password-link"
            onClick={() => setShowForgotPassword(true)}
          >
            Forgot Password?
          </button>

          {/* Link to signup page */}
          <div className="login-footer">
            <p>
              Don't have an account?{' '}
              <Link to="/faculty/signup" className="link">
                Sign Up
              </Link>
            </p>
          </div>
        </form>

        {/* Forgot Password Modal */}
        {showForgotPassword && (
          <div className="modal-overlay" onClick={() => setShowForgotPassword(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <h2>Reset Password</h2>
              <p className="modal-subtitle">Enter your email to receive a password reset link</p>
              <form onSubmit={handleForgotPassword}>
                <div className="form-group">
                  <input
                    type="text"
                    placeholder="Enter your email or employee ID"
                    value={resetEmail}
                    onChange={(e) => setResetEmail(e.target.value)}
                    className="form-input"
                    disabled={resetLoading}
                  />
                </div>
                {resetError && <p className="reset-error-message">{resetError}</p>}
                {resetMessage && <p className="reset-success-message">{resetMessage}</p>}
                <button 
                  type="submit" 
                  className="btn-reset"
                  disabled={resetLoading}
                  style={{ opacity: resetLoading ? 0.6 : 1, cursor: resetLoading ? 'not-allowed' : 'pointer' }}
                >
                  {resetLoading ? 'Sending...' : 'Send Reset Email'}
                </button>
                <button 
                  type="button" 
                  className="btn-cancel"
                  onClick={() => setShowForgotPassword(false)}
                  disabled={resetLoading}
                >
                  Cancel
                </button>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default FacultyLogin;
