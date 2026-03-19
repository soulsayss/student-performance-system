import api from './api'

// Login
export const login = async (email, password) => {
  try {
    // Clear any existing auth data before new login
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('userRole')
    
    console.log('[authService] Login attempt:', email)
    
    const response = await api.post('/auth/login', { email, password })
    
    console.log('[authService] Login response:', response.data)
    
    if (response.data.success) {
      const { access_token, user } = response.data
      
      // Store in localStorage
      localStorage.setItem('token', access_token)
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('userRole', user.role)
      
      console.log('[authService] Login successful, stored token and user')
      return { success: true, user }
    }
    
    console.log('[authService] Login failed:', response.data.message)
    return { success: false, message: response.data.message }
  } catch (error) {
    console.error('[authService] Login error:', error)
    
    // Handle different error types
    if (error.response) {
      // Server responded with error
      const message = error.response.data?.message || error.response.data?.error || 'Login failed'
      console.error('[authService] Server error:', message)
      return { success: false, message }
    } else if (error.request) {
      // Request made but no response
      console.error('[authService] No response from server')
      return { success: false, message: 'No response from server. Please check your connection.' }
    } else {
      // Something else happened
      console.error('[authService] Unexpected error:', error.message)
      return { success: false, message: error.message }
    }
  }
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
    // Clear all localStorage data
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('userRole')
    
    // Redirect to login
    window.location.href = '/login'
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
