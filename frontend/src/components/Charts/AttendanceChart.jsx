import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useTheme } from '../../contexts/ThemeContext';

const AttendanceChart = ({ data }) => {
  const { isDarkMode } = useTheme();

  return (
    <div className="bg-white dark:bg-dark-bg-secondary p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-dark-text-primary mb-4 transition-colors duration-200">
        Attendance Trend
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid 
            strokeDasharray="3 3" 
            stroke={isDarkMode ? '#374151' : '#f0f0f0'} 
          />
          <XAxis 
            dataKey="month" 
            stroke={isDarkMode ? '#b8b8b8' : '#6b7280'}
            style={{ fontSize: '12px' }}
          />
          <YAxis 
            stroke={isDarkMode ? '#b8b8b8' : '#6b7280'}
            style={{ fontSize: '12px' }}
            domain={[0, 100]}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: isDarkMode ? '#16213e' : '#fff',
              color: isDarkMode ? '#f1f1f1' : '#000',
              border: `1px solid ${isDarkMode ? '#374151' : '#e5e7eb'}`,
              borderRadius: '8px'
            }}
          />
          <Legend 
            wrapperStyle={{
              color: isDarkMode ? '#f1f1f1' : '#000'
            }}
          />
          <Line 
            type="monotone" 
            dataKey="percentage" 
            stroke="#3b82f6" 
            strokeWidth={2}
            dot={{ fill: '#3b82f6', r: 4 }}
            activeDot={{ r: 6 }}
            name="Attendance %"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AttendanceChart;
