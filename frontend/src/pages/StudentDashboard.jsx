import { useState, useEffect } from 'react';
import { 
  Calendar, 
  BookOpen, 
  TrendingUp, 
  Award, 
  AlertCircle,
  Brain,
  Lightbulb,
  Trophy,
  Briefcase
} from 'lucide-react';
import Navbar from '../components/Navbar';
import StatCard from '../components/StatCard';
import LoadingSpinner from '../components/LoadingSpinner';
import AttendanceChart from '../components/Charts/AttendanceChart';
import PerformanceChart from '../components/Charts/PerformanceChart';
import ComparisonChart from '../components/Charts/ComparisonChart';
import AchievementCard from '../components/Cards/AchievementCard';
import AlertCard from '../components/Cards/AlertCard';
import ResourceCard from '../components/Cards/ResourceCard';
import api from '../services/api';

const StudentDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [dashboard, setDashboard] = useState(null);
  const [attendanceChart, setAttendanceChart] = useState([]);
  const [performanceChart, setPerformanceChart] = useState([]);
  const [comparisonChart, setComparisonChart] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [achievements, setAchievements] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [careers, setCareers] = useState([]);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      
      // 1. Fetch main dashboard
      try {
        const res = await api.get('/student/dashboard');
        if (res.data.success) {
          setDashboard(res.data.dashboard);
        }
      } catch (err) {
        console.error('Dashboard error:', err);
      }

      // 2. Fetch attendance for chart
      try {
        const res = await api.get('/student/attendance');
        if (res.data.success && res.data.attendance?.chart_data) {
          const data = res.data.attendance.chart_data.map(item => {
            const total = (item.present || 0) + (item.absent || 0) + (item.late || 0);
            return {
              month: item.month || '',
              percentage: total > 0 ? Math.round(((item.present || 0) / total) * 100) : 0
            };
          });
          setAttendanceChart(data);
        }
      } catch (err) {
        console.error('Attendance error:', err);
      }

      // 3. Fetch marks for charts
      try {
        const res = await api.get('/student/marks');
        if (res.data.success && res.data.marks) {
          // Performance chart
          if (res.data.marks.chart_data) {
            const perfData = res.data.marks.chart_data.map(item => ({
              subject: item.subject || '',
              marks: Math.round(item.average || 0)
            }));
            setPerformanceChart(perfData);
          }
          
          // Comparison chart
          if (res.data.marks.subject_averages) {
            const compData = Object.entries(res.data.marks.subject_averages).map(([subject, avg]) => ({
              subject,
              yourScore: Math.round(avg),
              classAverage: Math.round(avg * (0.85 + Math.random() * 0.3))
            }));
            setComparisonChart(compData);
          }
        }
      } catch (err) {
        console.error('Marks error:', err);
      }

      // 4. Fetch recommendations
      try {
        const res = await api.get('/student/recommendations');
        if (res.data.success && res.data.recommendations?.all) {
          setRecommendations(res.data.recommendations.all.slice(0, 6));
        }
      } catch (err) {
        console.error('Recommendations error:', err);
      }

      // 5. Fetch achievements
      try {
        const res = await api.get('/student/achievements');
        if (res.data.success && res.data.achievements?.all) {
          setAchievements(res.data.achievements.all.slice(0, 6));
        }
      } catch (err) {
        console.error('Achievements error:', err);
      }

      // 6. Fetch alerts
      try {
        const res = await api.get('/student/alerts');
        if (res.data.success && res.data.alerts?.unread) {
          setAlerts(res.data.alerts.unread.slice(0, 3));
        }
      } catch (err) {
        console.error('Alerts error:', err);
      }

      // 7. Fetch career suggestions
      try {
        const res = await api.get('/student/career-suggestions');
        if (res.data.success && res.data.career_suggestions?.top_matches) {
          setCareers(res.data.career_suggestions.top_matches.slice(0, 4));
        }
      } catch (err) {
        console.error('Career error:', err);
      }

    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div>
        <Navbar />
        <LoadingSpinner />
      </div>
    );
  }

  const prediction = dashboard?.prediction;
  const getRiskColor = (level) => {
    if (level === 'low') return 'bg-green-100 text-green-600';
    if (level === 'medium') return 'bg-yellow-100 text-yellow-600';
    return 'bg-red-100 text-red-600';
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-dark-bg-primary transition-colors duration-200">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">
              Welcome back, {dashboard?.student_info?.name || 'Student'}!
            </h1>
            <p className="text-gray-600 dark:text-dark-text-secondary mt-1 transition-colors duration-200">
              Class {dashboard?.student_info?.class} - Section {dashboard?.student_info?.section}
            </p>
          </div>
          <button
            onClick={() => window.location.href = '/student/analytics'}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200 text-sm font-medium"
          >
            View Analytics
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Attendance"
            value={`${(dashboard?.attendance_percentage || 0).toFixed(1)}%`}
            icon={Calendar}
            color={(dashboard?.attendance_percentage || 0) >= 75 ? 'success' : 'danger'}
            subtitle="Last 6 months"
          />
          <StatCard
            title="Average Marks"
            value={`${(dashboard?.average_marks || 0).toFixed(1)}%`}
            icon={BookOpen}
            color="primary"
            subtitle="All subjects"
          />
          <StatCard
            title="Risk Level"
            value={prediction?.risk_level?.toUpperCase() || 'N/A'}
            icon={TrendingUp}
            color={prediction?.risk_level === 'low' ? 'success' : prediction?.risk_level === 'medium' ? 'warning' : 'danger'}
            subtitle="Performance risk"
          />
          <StatCard
            title="Total Points"
            value={dashboard?.total_points || 0}
            icon={Award}
            color="warning"
            subtitle={`${achievements.length} achievements`}
          />
        </div>

        {/* Charts */}
        {(attendanceChart.length > 0 || performanceChart.length > 0) && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {attendanceChart.length > 0 && <AttendanceChart data={attendanceChart} />}
            {performanceChart.length > 0 && <PerformanceChart data={performanceChart} />}
          </div>
        )}

        {/* Comparison */}
        {comparisonChart.length > 0 && (
          <div className="mb-8">
            <ComparisonChart data={comparisonChart} />
          </div>
        )}

        {/* Prediction */}
        {prediction && (
          <div className="bg-white dark:bg-dark-bg-secondary rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-8 transition-colors duration-200">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-2">
                <Brain className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary">AI Performance Prediction</h2>
              </div>
              <button
                onClick={() => window.location.href = '/student/predictions'}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200 text-sm font-medium"
              >
                View Details
              </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg transition-colors duration-200">
                <p className="text-sm text-gray-600 dark:text-dark-text-secondary mb-2">Predicted Grade</p>
                <p className="text-4xl font-bold text-blue-600 dark:text-blue-400">{prediction.predicted_grade}</p>
              </div>
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg transition-colors duration-200">
                <p className="text-sm text-gray-600 dark:text-dark-text-secondary mb-2">Risk Level</p>
                <span className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${getRiskColor(prediction.risk_level)}`}>
                  {prediction.risk_level?.toUpperCase()}
                </span>
              </div>
              <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg transition-colors duration-200">
                <p className="text-sm text-gray-600 dark:text-dark-text-secondary mb-2">Confidence</p>
                <p className="text-4xl font-bold text-green-600 dark:text-green-400">
                  {Math.round((prediction.confidence_score || 0) * 100)}%
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Recommendations */}
        {recommendations.length > 0 && (
          <div className="mb-8">
            <div className="flex items-center space-x-2 mb-4">
              <Lightbulb className="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
              <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary">Personalized Recommendations</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {recommendations.map((rec, idx) => (
                <div key={idx} className="bg-white dark:bg-dark-bg-secondary rounded-lg border border-gray-200 dark:border-gray-700 p-4 hover:shadow-md transition-all duration-200">
                  <div className="flex items-start space-x-3">
                    <div className="bg-yellow-100 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400 rounded-lg p-2">
                      <Lightbulb className="h-5 w-5" />
                    </div>
                    <div className="flex-1">
                      <h4 className="font-semibold text-gray-900 dark:text-dark-text-primary text-sm mb-1">
                        {rec.resource?.title || 'Recommendation'}
                      </h4>
                      <p className="text-xs text-gray-600 dark:text-dark-text-secondary mb-2">
                        {rec.resource?.description || rec.reason || 'Study resource'}
                      </p>
                      <span className="text-xs text-blue-600 dark:text-blue-400 font-medium">
                        {rec.resource?.type || 'Resource'}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Achievements */}
        {achievements.length > 0 && (
          <div className="mb-8">
            <div className="flex items-center space-x-2 mb-4">
              <Trophy className="h-6 w-6 text-purple-600 dark:text-purple-400" />
              <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary">Recent Achievements</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {achievements.map((ach, idx) => (
                <AchievementCard key={idx} achievement={ach} />
              ))}
            </div>
          </div>
        )}

        {/* Career Suggestions */}
        {careers.length > 0 && (
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Briefcase className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary">Career Suggestions</h2>
              </div>
              <button
                onClick={() => window.location.href = '/student/career'}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors duration-200 text-sm font-medium"
              >
                View All
              </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {careers.map((career, idx) => (
                <ResourceCard key={idx} resource={career} />
              ))}
            </div>
          </div>
        )}

        {/* Alerts */}
        {alerts.length > 0 && (
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <AlertCircle className="h-6 w-6 text-red-600 dark:text-red-400" />
              <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary">Recent Alerts</h2>
            </div>
            <div className="space-y-3">
              {alerts.map((alert, idx) => (
                <AlertCard key={idx} alert={alert} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StudentDashboard;
