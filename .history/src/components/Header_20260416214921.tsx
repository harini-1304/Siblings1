import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI, isAuthenticated } from '../services/api';
import '../styles/Header.css';

function Header() {
  const navigate = useNavigate();
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [showDropdown, setShowDropdown] = useState(false);

  // Function to extract email from token
  const extractEmailFromToken = () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.email;
      } catch (e) {
        console.error('Failed to decode token:', e);
        return null;
      }
    }
    return null;
  };

  // Get user email from localStorage when component mounts
  useEffect(() => {
    const email = extractEmailFromToken();
    setUserEmail(email);

    // Listen for auth token updates (happens when user logs in)
    const handleAuthTokenUpdated = () => {
      const newEmail = extractEmailFromToken();
      setUserEmail(newEmail);
      console.log('Auth token updated, new email:', newEmail);
    };

    window.addEventListener('authTokenUpdated', handleAuthTokenUpdated);
    
    // Also listen for storage changes (when login happens in another tab)
    const handleStorageChange = () => {
      const newEmail = extractEmailFromToken();
      setUserEmail(newEmail);
    };

    window.addEventListener('storage', handleStorageChange);
    
    return () => {
      window.removeEventListener('authTokenUpdated', handleAuthTokenUpdated);
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const handleLogout = () => {
    authAPI.logout();
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    setUserEmail(null); // Clear the UI immediately
    navigate('/faculty/login');
  };

  return (
    <header className="psg-header">
      <div className="header-container">
        <div className="header-content">
          <div className="logo-section">
            <img src="/images/logo.png" alt="PSG Institute Logo" className="psg-logo" />
          </div>
          <div className="title-section">
            <h1 className="app-title">ProConnect</h1>
            <p className="college-name">PSG INSTITUTE OF TECHNOLOGY AND APPLIED RESEARCH</p>
          </div>
          
          {/* User Menu */}
          {isAuthenticated() && userEmail && (
            <div className="user-menu">
              <button 
                className="user-button"
                onClick={() => setShowDropdown(!showDropdown)}
              >
                <span className="user-email">{userEmail}</span>
                <span className="dropdown-arrow">▼</span>
              </button>
              
              {showDropdown && (
                <div className="dropdown-menu">
                  <button 
                    className="logout-btn"
                    onClick={handleLogout}
                  >
                    Logout
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export default Header;
