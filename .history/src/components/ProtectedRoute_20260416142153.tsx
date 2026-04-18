import { ReactNode, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI, isAuthenticated } from '../services/api';

interface ProtectedRouteProps {
  children: ReactNode;
  requiredRole?: 'faculty' | 'student';
}

export function ProtectedRoute({ children, requiredRole = 'faculty' }: ProtectedRouteProps) {
  const [isAuthorized, setIsAuthorized] = useState<boolean | null>(null);
  const [userFound, setUserFound] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Check if token exists
        if (!isAuthenticated()) {
          console.log('No authentication token found');
          setIsAuthorized(false);
          setUserFound(true);
          navigate('/faculty/login');
          return;
        }

        // Verify token with backend
        const response = await authAPI.verifyToken();
        
        if (response && response.valid) {
          console.log('Token verified - authorized');
          setIsAuthorized(true);
        } else {
          console.log('Token invalid');
          setIsAuthorized(false);
          navigate('/faculty/login');
        }
      } catch (error) {
        console.error('Error checking auth:', error);
        // Token might have expired, try to refresh
        try {
          await authAPI.refreshToken();
          setIsAuthorized(true);
        } catch (refreshError) {
          console.error('Token refresh failed:', refreshError);
          setIsAuthorized(false);
          navigate('/faculty/login');
        }
      } finally {
        setUserFound(true);
      }
    };

    checkAuth();
  }, [navigate]);

  // Show loading while checking auth state
  if (!userFound) {
    return <div style={{ padding: '50px 20px', textAlign: 'center' }}>Checking access...</div>;
  }

  if (isAuthorized === null) {
    return <div style={{ padding: '50px 20px', textAlign: 'center' }}>Loading...</div>;
  }

  if (!isAuthorized) {
    return <div style={{ padding: '50px 20px', textAlign: 'center' }}>Unauthorized access. Redirecting...</div>;
  }

  return <>{children}</>;
}
