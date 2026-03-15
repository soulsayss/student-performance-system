// Format date
export const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// Format datetime
export const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Format percentage
export const formatPercentage = (value, decimals = 2) => {
  if (value === null || value === undefined) return 'N/A'
  return `${Number(value).toFixed(decimals)}%`
}

// Get grade color
export const getGradeColor = (grade) => {
  const gradeColors = {
    'A+': 'text-success-600 bg-success-50',
    'A': 'text-success-600 bg-success-50',
    'B+': 'text-primary-600 bg-primary-50',
    'B': 'text-primary-600 bg-primary-50',
    'C+': 'text-warning-600 bg-warning-50',
    'C': 'text-warning-600 bg-warning-50',
    'D': 'text-danger-600 bg-danger-50',
    'F': 'text-danger-600 bg-danger-50',
  }
  return gradeColors[grade] || 'text-gray-600 bg-gray-50'
}

// Get risk level color
export const getRiskLevelColor = (level) => {
  const colors = {
    low: 'text-success-600 bg-success-50',
    medium: 'text-warning-600 bg-warning-50',
    high: 'text-danger-600 bg-danger-50',
  }
  return colors[level] || 'text-gray-600 bg-gray-50'
}

// Get alert severity color
export const getAlertSeverityColor = (severity) => {
  const colors = {
    info: 'text-primary-600 bg-primary-50 border-primary-200',
    warning: 'text-warning-600 bg-warning-50 border-warning-200',
    critical: 'text-danger-600 bg-danger-50 border-danger-200',
  }
  return colors[severity] || 'text-gray-600 bg-gray-50 border-gray-200'
}

// Calculate attendance percentage
export const calculateAttendancePercentage = (present, total) => {
  if (total === 0) return 0
  return ((present / total) * 100).toFixed(2)
}

// Get initials from name
export const getInitials = (name) => {
  if (!name) return '?'
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

// Truncate text
export const truncateText = (text, maxLength = 50) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}

// Debounce function
export const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Format number with commas
export const formatNumber = (num) => {
  if (num === null || num === undefined) return 'N/A'
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

// Get status badge class
export const getStatusBadgeClass = (status) => {
  const classes = {
    present: 'badge-success',
    absent: 'badge-danger',
    late: 'badge-warning',
    pending: 'badge-warning',
    submitted: 'badge-info',
    graded: 'badge-success',
  }
  return classes[status] || 'badge-info'
}
