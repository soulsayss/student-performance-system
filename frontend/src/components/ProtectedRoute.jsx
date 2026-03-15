import { Navigate } from 'react-router-dom'
import { isAuthenticated, getUserRole } from '../services/authService'

const ProtectedRoute = ({ children, allowedRoles }) => {
  const authenticated = isAuthenticated()
  const userRole = getUserRole()
  
  // Check if user is authenticated
  if (!authenticated) {
    return <Navigate to="/login" replace />
  }
  
  // Check if user has required role
  if (allowedRoles && !allowedRoles.includes(userRole)) {
    return <Navigate to="/unauthorized" replace />
  }
  
  return children
}

export default ProtectedRoute
