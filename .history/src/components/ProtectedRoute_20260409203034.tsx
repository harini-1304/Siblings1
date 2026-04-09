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
        // Not logged in
        console.log('No user logged in');
        navigate('/faculty/login');
        return;
      }

      try {
        // Check user role in Firestore 'users' collection
        const userDoc = await getDoc(doc(db, 'users', user.uid));
        
        if (userDoc.exists()) {
          const userData = userDoc.data();
          const userRole = userData.role;

          console.log('User role found:', userRole, 'Required role:', requiredRole);

          if (userRole === requiredRole) {
            setIsAuthorized(true);
          } else {
            // Wrong role
            console.log('Wrong role - redirecting');
            navigate('/faculty/login');
            setIsAuthorized(false);
          }
        } else {
          // If user doc doesn't exist, check 'faculties' collection (legacy)
          console.log('User not in users collection, checking faculties...');
          const facultyDoc = await getDoc(doc(db, 'faculties', user.uid));
          
          if (facultyDoc.exists() && requiredRole === 'faculty') {
            // Found in faculties collection
            setIsAuthorized(true);
          } else {
            console.log('User not found in any collection');
            navigate('/faculty/login');
            setIsAuthorized(false);
          }
        }
      } catch (error) {
        console.error('Error checking user role:', error);
        navigate('/faculty/login');
        setIsAuthorized(false);
      }
    });

    return () => unsubscribe();
  }, [requiredRole, navigate]);

  if (isAuthorized === null) {
    return <div style={{ padding: '20px', textAlign: 'center' }}>Loading...</div>;
  }

  if (!isAuthorized) {
    return <div style={{ padding: '20px', textAlign: 'center' }}>Unauthorized access. Redirecting...</div>;
  }

  return <>{children}</>;
}
