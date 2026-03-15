import { AlertTriangle, Info, AlertCircle } from 'lucide-react';

const AlertCard = ({ alert }) => {
  // Handle null/undefined alert
  if (!alert) return null;

  const severityConfig = {
    critical: {
      bg: 'bg-red-50 dark:bg-red-900/20',
      border: 'border-red-200 dark:border-red-800',
      text: 'text-red-800 dark:text-red-300',
      icon: AlertTriangle,
      iconColor: 'text-red-600 dark:text-red-400'
    },
    warning: {
      bg: 'bg-yellow-50 dark:bg-yellow-900/20',
      border: 'border-yellow-200 dark:border-yellow-800',
      text: 'text-yellow-800 dark:text-yellow-300',
      icon: AlertCircle,
      iconColor: 'text-yellow-600 dark:text-yellow-400'
    },
    info: {
      bg: 'bg-blue-50 dark:bg-blue-900/20',
      border: 'border-blue-200 dark:border-blue-800',
      text: 'text-blue-800 dark:text-blue-300',
      icon: Info,
      iconColor: 'text-blue-600 dark:text-blue-400'
    }
  };

  const config = severityConfig[alert.severity] || severityConfig.info;
  const Icon = config.icon;
  
  const message = alert.message || 'No message';
  const createdAt = alert.created_at || new Date().toISOString();

  return (
    <div className={`${config.bg} ${config.border} border rounded-lg p-4 flex items-start space-x-3`}>
      <Icon className={`${config.iconColor} h-5 w-5 mt-0.5 flex-shrink-0`} />
      <div className="flex-1">
        <p className={`${config.text} font-medium text-sm`}>{message}</p>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
          {new Date(createdAt).toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
          })}
        </p>
      </div>
    </div>
  );
};

export default AlertCard;
