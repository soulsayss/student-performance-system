import { LogOut, User, Bell, Moon, Sun } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { logout, getCurrentUser } from '../services/authService'
import { useTheme } from '../contexts/ThemeContext'
import toast from 'react-hot-toast'

const Navbar = () => {
  const navigate = useNavigate()
  const user = getCurrentUser()
  const { isDarkMode, toggleTheme } = useTheme()

  const handleLogout = () => {
    logout()
    toast.success('Logged out successfully')
    navigate('/login')
  }

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 dark:bg-dark-bg-secondary dark:border-gray-700 transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-primary-600 dark:text-primary-400 transition-colors duration-200">
              Student Academic System
            </h1>
          </div>

          {/* Right Side */}
          <div className="flex items-center space-x-4">
            {/* Dark Mode Toggle */}
            <button 
              onClick={toggleTheme}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-300 dark:hover:text-gray-100 dark:hover:bg-gray-700 rounded-lg transition-all duration-200"
              title={isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
              aria-label="Toggle theme"
            >
              {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>

            {/* Notifications */}
            <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-300 dark:hover:text-gray-100 dark:hover:bg-gray-700 rounded-lg transition-all duration-200">
              <Bell className="w-5 h-5" />
            </button>

            {/* User Info */}
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-primary-600 dark:bg-primary-500 rounded-full flex items-center justify-center transition-colors duration-200">
                  <User className="w-5 h-5 text-white" />
                </div>
                <div className="hidden md:block">
                  <p className="text-sm font-medium text-gray-900 dark:text-dark-text-primary transition-colors duration-200">{user?.name}</p>
                  <p className="text-xs text-gray-500 dark:text-dark-text-secondary capitalize transition-colors duration-200">{user?.role}</p>
                </div>
              </div>

              {/* Logout Button */}
              <button
                onClick={handleLogout}
                className="p-2 text-gray-600 hover:text-danger-600 hover:bg-danger-50 dark:text-gray-300 dark:hover:text-danger-400 dark:hover:bg-danger-900/20 rounded-lg transition-all duration-200"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
