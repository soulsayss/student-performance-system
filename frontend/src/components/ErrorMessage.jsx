import { AlertCircle } from 'lucide-react'

const ErrorMessage = ({ message = 'An error occurred', onRetry }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <AlertCircle className="w-12 h-12 text-danger-600 dark:text-danger-400 mb-4" />
      <p className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Oops!</p>
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">{message}</p>
      {onRetry && (
        <button onClick={onRetry} className="btn btn-primary">
          Try Again
        </button>
      )}
    </div>
  )
}

export default ErrorMessage
