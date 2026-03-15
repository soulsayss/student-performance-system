import { Briefcase, TrendingUp, Target, Award } from 'lucide-react';

const ResourceCard = ({ resource }) => {
  // Handle null/undefined resource
  if (!resource) return null;

  // Handle both resource and career suggestion formats
  const isCareer = resource.career_path || resource.match_percentage;
  
  if (isCareer) {
    // Career suggestion format
    const careerField = resource.career_path || 'Career Path';
    const matchPercentage = resource.match_percentage || 0;
    const description = resource.description || 'Career path based on your strengths and interests';
    
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 hover:shadow-md transition-all hover:-translate-y-1">
        <div className="flex items-start space-x-3">
          <div className="bg-purple-100 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400 rounded-lg p-2">
            <Briefcase className="h-5 w-5" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-1">
              <h4 className="font-semibold text-gray-900 dark:text-gray-100 text-sm truncate">
                {careerField}
              </h4>
              <span className="bg-purple-100 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400 text-xs px-2 py-1 rounded-full font-medium">
                {matchPercentage}% Match
              </span>
            </div>
            <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2 mb-2">
              {description}
            </p>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500 dark:text-gray-400">Recommended</span>
              <span className="text-xs text-blue-600 dark:text-blue-400 font-medium">
                View Details →
              </span>
            </div>
          </div>
        </div>
      </div>
    );
  }
  
  // Original resource format
  const typeConfig = {
    video: {
      icon: TrendingUp,
      bg: 'bg-red-100 dark:bg-red-900/20',
      text: 'text-red-600 dark:text-red-400',
      label: 'Video'
    },
    article: {
      icon: Target,
      bg: 'bg-blue-100 dark:bg-blue-900/20',
      text: 'text-blue-600 dark:text-blue-400',
      label: 'Article'
    },
    book: {
      icon: Award,
      bg: 'bg-green-100 dark:bg-green-900/20',
      text: 'text-green-600 dark:text-green-400',
      label: 'Book'
    },
    link: {
      icon: Briefcase,
      bg: 'bg-purple-100 dark:bg-purple-900/20',
      text: 'text-purple-600 dark:text-purple-400',
      label: 'Link'
    }
  };

  const config = typeConfig[resource.type] || typeConfig.link;
  const Icon = config.icon;
  
  const title = resource.title || 'Resource';
  const description = resource.description || 'Learning resource';
  const subject = resource.subject || 'General';

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 hover:shadow-md transition-all hover:-translate-y-1">
      <div className="flex items-start space-x-3">
        <div className={`${config.bg} ${config.text} rounded-lg p-2`}>
          <Icon className="h-5 w-5" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-1">
            <h4 className="font-semibold text-gray-900 dark:text-gray-100 text-sm truncate">
              {title}
            </h4>
            <span className={`${config.bg} ${config.text} text-xs px-2 py-1 rounded-full font-medium`}>
              {config.label}
            </span>
          </div>
          <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2 mb-2">
            {description}
          </p>
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-500 dark:text-gray-400">{subject}</span>
            {resource.url && (
              <a 
                href={resource.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium"
              >
                View →
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResourceCard;
