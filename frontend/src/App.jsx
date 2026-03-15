import { Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { ThemeProvider } from './contexts/ThemeContext'

// Import pages
import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import StudentDashboard from './pages/StudentDashboard'
import TeacherDashboard from './pages/TeacherDashboard'
import ParentDashboard from './pages/ParentDashboard'
import AdminDashboard from './pages/AdminDashboard'

// Import components
import ProtectedRoute from './components/ProtectedRoute'

const NotFound = () => <div className="flex items-center justify-center min-h-screen dark:bg-dark-bg-primary"><h1 className="text-3xl font-bold dark:text-dark-text-primary">404 - Page Not Found</h1></div>
const Unauthorized = () => (
  <div className="flex flex-col items-center justify-center min-h-screen dark:bg-dark-bg-primary">
    <h1 className="text-3xl font-bold text-danger-600 mb-4">Unauthorized Access</h1>
    <p className="text-gray-600 dark:text-dark-text-secondary mb-4">You don't have permission to access this page.</p>
    <a href="/login" className="btn btn-primary">Go to Login</a>
  </div>
)

function App() {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-gray-50 dark:bg-dark-bg-primary transition-colors duration-200">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Protected Routes */}
          <Route
            path="/student/*"
            element={
              <ProtectedRoute allowedRoles={['student']}>
                <StudentDashboard />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/teacher/*"
            element={
              <ProtectedRoute allowedRoles={['teacher']}>
                <TeacherDashboard />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/parent/*"
            element={
              <ProtectedRoute allowedRoles={['parent']}>
                <ParentDashboard />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/*"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          
          {/* Default Routes */}
          <Route path="/unauthorized" element={<Unauthorized />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </ThemeProvider>
  )
}

export default App
