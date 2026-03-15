import { FileQuestion, Inbox, AlertCircle, BookOpen } from 'lucide-react';

const EmptyState = ({ 
  icon: Icon = Inbox, 
  title = "No data available", 
  description = "There's nothing to show here yet.",
  action = null 
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center animate-fadeIn">
      <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mb-4">
        <Icon className="w-8 h-8 text-gray-400 dark:text-gray-500" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">{title}</h3>
      <p className="text-gray-500 dark:text-gray-400 mb-6 max-w-sm">{description}</p>
      {action && (
        <div className="mt-4">
          {action}
        </div>
      )}
    </div>
  );
};

export default EmptyState;
