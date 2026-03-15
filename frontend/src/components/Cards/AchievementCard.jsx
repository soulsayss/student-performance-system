import { Trophy, Award, Star, Target } from 'lucide-react';

const AchievementCard = ({ achievement }) => {
  // Handle null/undefined achievement
  if (!achievement) return null;

  const iconMap = {
    trophy: Trophy,
    award: Award,
    star: Star,
    target: Target
  };

  const Icon = iconMap[achievement.icon] || Trophy;

  const colorClasses = {
    gold: 'bg-yellow-100 text-yellow-600 border-yellow-200 dark:bg-yellow-900/20 dark:text-yellow-400 dark:border-yellow-800',
    silver: 'bg-gray-100 text-gray-600 border-gray-200 dark:bg-gray-700 dark:text-gray-400 dark:border-gray-600',
    bronze: 'bg-orange-100 text-orange-600 border-orange-200 dark:bg-orange-900/20 dark:text-orange-400 dark:border-orange-800',
    blue: 'bg-blue-100 text-blue-600 border-blue-200 dark:bg-blue-900/20 dark:text-blue-400 dark:border-blue-800',
    green: 'bg-green-100 text-green-600 border-green-200 dark:bg-green-900/20 dark:text-green-400 dark:border-green-800',
    purple: 'bg-purple-100 text-purple-600 border-purple-200 dark:bg-purple-900/20 dark:text-purple-400 dark:border-purple-800'
  };

  const colorClass = colorClasses[achievement.color] || colorClasses.blue;

  // Use badge_name if title doesn't exist (API returns badge_name)
  const title = achievement.title || achievement.badge_name || 'Achievement';
  const description = achievement.description || 'Well done!';
  const points = achievement.points || 0;
  const earnedAt = achievement.earned_at || new Date().toISOString();

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start space-x-3">
        <div className={`${colorClass} border rounded-lg p-3`}>
          <Icon className="h-6 w-6" />
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-gray-900 dark:text-gray-100 text-sm">{title}</h4>
          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">{description}</p>
          <div className="flex items-center justify-between mt-2">
            <span className="text-xs font-medium text-blue-600 dark:text-blue-400">
              +{points} points
            </span>
            <span className="text-xs text-gray-500 dark:text-gray-400">
              {new Date(earnedAt).toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric' 
              })}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AchievementCard;
