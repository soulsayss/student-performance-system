import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend, ResponsiveContainer, Tooltip } from 'recharts';
import { useTheme } from '../../contexts/ThemeContext';

const ComparisonChart = ({ data }) => {
  const { isDarkMode } = useTheme();

  return (
    <div className="bg-white dark:bg-dark-bg-secondary p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-dark-text-primary mb-4 transition-colors duration-200">
        Performance Comparison
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <RadarChart data={data}>
          <PolarGrid stroke={isDarkMode ? '#374151' : '#e5e7eb'} />
          <PolarAngleAxis 
            dataKey="subject" 
            stroke={isDarkMode ? '#b8b8b8' : '#000'}
            style={{ fontSize: '12px', fill: isDarkMode ? '#b8b8b8' : '#000' }}
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 100]}
            stroke={isDarkMode ? '#b8b8b8' : '#000'}
            style={{ fontSize: '10px', fill: isDarkMode ? '#b8b8b8' : '#000' }}
          />
          <Radar 
            name="Your Score" 
            dataKey="yourScore" 
            stroke="#3b82f6" 
            fill="#3b82f6" 
            fillOpacity={0.6} 
          />
          <Radar 
            name="Class Average" 
            dataKey="classAverage" 
            stroke="#f59e0b" 
            fill="#f59e0b" 
            fillOpacity={0.6} 
          />
          <Legend 
            wrapperStyle={{
              color: isDarkMode ? '#f1f1f1' : '#000'
            }}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: isDarkMode ? '#16213e' : '#fff',
              color: isDarkMode ? '#f1f1f1' : '#000',
              border: `1px solid ${isDarkMode ? '#374151' : '#e5e7eb'}`,
              borderRadius: '8px'
            }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ComparisonChart;
