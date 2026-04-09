import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import Footer from './components/Footer';
import { ProtectedRoute } from './components/ProtectedRoute';

// Faculty pages
import FacultyLogin from './pages/FacultyLogin';
import FacultySignup from './pages/FacultySignup';
import FacultyDashboard from './pages/FacultyDashboard';

// Student page
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
            
            {/* Default route - redirect to student form */}
            <Route path="/" element={<Navigate to="/student/form" replace />} />
            
            {/* Faculty routes */}
            <Route path="/faculty/login" element={<FacultyLogin />} />
            <Route path="/faculty/signup" element={<FacultySignup />} />
            <Route 
              path="/faculty/dashboard" 
              element={
                <ProtectedRoute requiredRole="faculty">
                  <FacultyDashboard />
                </ProtectedRoute>
              } 
            />
            
            {/* Student form - public access, no authentication needed */}
            <Route path="/student/form" element={<StudentForm />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
