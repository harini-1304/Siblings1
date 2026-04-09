import { ReactNode, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { onAuthStateChanged, User } from 'firebase/auth';
import { doc, getDoc } from 'firebase/firestore';
import { auth, db } from '../config/firebase';

interface ProtectedRouteProps {
  children: ReactNode;
  requiredRole: 'faculty' | 'student';
}

export function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
  const [isAuthorized, setIsAuthorized] = useState<boolean | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user: User | null) => {
      if (!user) {
        // Not logged in - redirect to appropriate login
        if (requiredRole === 'faculty') {
          navigate('/faculty/login');
        } else {
          navigate('/student/form');
        }
        return;
      }

      try {
        // Check user role in Firestore
        const userDoc = await getDoc(doc(db, 'users', user.uid));
        
        if (userDoc.exists()) {
          const userData = userDoc.data();
          const userRole = userData.role; // 'faculty' or 'student'

          if (userRole === requiredRole) {
            setIsAuthorized(true);
          } else {
            // Wrong role - redirect to their proper page
            if (requiredRole === 'faculty') {
              navigate('/student/form');
            } else {
              navigate('/faculty/login');
            }
            setIsAuthorized(false);
          }
        } else {
          // User not found in database
          navigate('/');
          setIsAuthorized(false);
        }
      } catch (error) {
        console.error('Error checking user role:', error);
        navigate('/');
        setIsAuthorized(false);
      }
    });

    return () => unsubscribe();
  }, [requiredRole, navigate]);

  if (isAuthorized === null) {
    return <div style={{ padding: '20px', textAlign: 'center' }}>Loading...</div>;
  }

  if (!isAuthorized) {
    return <div style={{ padding: '20px', textAlign: 'center' }}>Unauthorized access</div>;
  }

  return <>{children}</>;
}
