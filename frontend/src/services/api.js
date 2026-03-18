import axios from 'axios'
import toast from 'react-hot-toast'

// API URL from environment variable or fallback to localhost
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

// Create axios instance
const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - Add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      const message = error.response.data?.message || 'An error occurred'
      
      if (error.response.status === 401) {
        // Unauthorized - clear token and redirect to login
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        localStorage.removeItem('userRole')
        window.location.href = '/login'
        toast.error('Session expired. Please login again.')
      } else if (error.response.status === 403) {
        toast.error('Access denied')
      } else if (error.response.status >= 500) {
        // Only show toast for server errors
        toast.error(message)
      }
      // Don't show toast for 4xx errors (except 401/403) - let components handle them
    } else if (error.request) {
      // Request made but no response - likely CORS or network issue
      // Don't show toast here as it might be a transient error
      console.error('Network error:', error.message)
    } else {
      // Something else happened
      console.error('Request error:', error.message)
    }
    
    return Promise.reject(error)
  }
)

export default api
