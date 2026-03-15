import api from './api'

// Login
export const login = async (email, password) => {
  const response = await api.post('/auth/login', { email, password })
  
  if (response.data.success) {
    const { access_token, user } = response.data
    
    // Store in localStorage
    localStorage.setItem('token', access_token)
    localStorage.setItem('user', JSON.stringify(user))
    localStorage.setItem('userRole', user.role)
    
    return { success: true, user }
  }
  
  return { success: false, message: response.data.message }
}

// Register
export const register = async (userData) => {
  const response = await api.post('/auth/register', userData)
  return response.data
}

// Logout
export const logout = () => {
  try {
    api.post('/auth/logout')
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    // Clear localStorage
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('userRole')
  }
}

// Get current user
export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user')
  return userStr ? JSON.parse(userStr) : null
}

// Get user role
export const getUserRole = () => {
  return localStorage.getItem('userRole')
}

// Check if authenticated
export const isAuthenticated = () => {
  return !!localStorage.getItem('token')
}

// Get profile
export const getProfile = async () => {
  const response = await api.get('/auth/profile')
  return response.data
}
