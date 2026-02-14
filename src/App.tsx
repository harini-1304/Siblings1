import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

// We'll create these components next
import FacultyLogin from './pages/FacultyLogin';
import FacultySignup from './pages/FacultySignup';
import FacultyDashboard from './pages/FacultyDashboard';
import StudentForm from './pages/StudentForm';

function App() {
  // This is the main component that defines all the routes (pages) in our app
  
  return (
    <Router>
      {/* Router enables navigation between different pages */}
      <Routes>
        {/* Each Route represents a different page/URL */}
        
        {/* Default route - redirect to login */}
        <Route path="/" element={<Navigate to="/faculty/login" replace />} />
        
        {/* Faculty routes */}
        <Route path="/faculty/login" element={<FacultyLogin />} />
        <Route path="/faculty/signup" element={<FacultySignup />} />
        <Route path="/faculty/dashboard" element={<FacultyDashboard />} />
        
        {/* Student form route - this will be like Google Forms */}
        <Route path="/student/form" element={<StudentForm />} />
      </Routes>
    </Router>
  );
}

export default App;
