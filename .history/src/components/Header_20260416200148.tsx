import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI, isAuthenticated } from '../services/api';
import '../styles/Header.css';

function Header() {
  const navigate = useNavigate();
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [showDropdown, setShowDropdown] = useState(false);

  // Get user email from localStorage when component mounts
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Decode token to get user info
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        setUserEmail(payload.email);
      } catch (e) {
        console.error('Failed to decode token:', e);
      }
    }
  }, []);

  const handleLogout = () => {
    authAPI.logout();
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
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
