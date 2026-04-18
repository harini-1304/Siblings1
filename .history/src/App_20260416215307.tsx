import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import Footer from './components/Footer';
import { ProtectedRoute } from './components/ProtectedRoute';

// Faculty pages
import FacultyLogin from './pages/FacultyLogin';
import FacultySignup from './pages/FacultySignup';
import FacultyDashboard from './pages/FacultyDashboard';
import ResetPassword from './pages/ResetPassword';

// Student pages
import StudentLogin from './pages/StudentLogin';
import StudentSignup from './pages/StudentSignup';
import StudentForm from './pages/StudentForm';

function App() {
  // This is the main component that defines all the routes (pages) in our app
  
  return (
    <Router>
      <div className="app-wrapper">
        <Header />
        <main className="app-main">
          {/* Router enables navigation between different pages */}
          <Routes>
            {/* Each Route represents a different page/URL */}
            
            {/* Default route - redirect to student login */}
            <Route path="/" element={<Navigate to="/student/login" replace />} />
            
            {/* Faculty routes */}
            <Route path="/faculty/login" element={<FacultyLogin />} />
            <Route path="/faculty/signup" element={<FacultySignup />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route 
              path="/faculty/dashboard" 
              element={
                <ProtectedRoute requiredRole="faculty">
                  <FacultyDashboard />
                </ProtectedRoute>
              } 
            />
            
            {/* Student routes - correct flow: login -> signup -> form */}
            <Route path="/student/login" element={<StudentLogin />} />
            <Route path="/student/signup" element={<StudentSignup />} />
            <Route path="/student/form" element={<StudentForm />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
