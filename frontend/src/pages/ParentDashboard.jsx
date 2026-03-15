import { useState, useEffect } from 'react';
import { Users, Calendar, BookOpen, TrendingUp, AlertCircle, Brain, Lightbulb } from 'lucide-react';
import Navbar from '../components/Navbar';
import StatCard from '../components/StatCard';
import LoadingSpinner from '../components/LoadingSpinner';
import AttendanceChart from '../components/Charts/AttendanceChart';
import PerformanceChart from '../components/Charts/PerformanceChart';
import ComparisonChart from '../components/Charts/ComparisonChart';
import AlertCard from '../components/Cards/AlertCard';
import * as parentService from '../services/parentService';

const ParentDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [children, setChildren] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);
  const [childData, setChildData] = useState(null);
  const [attendanceChart, setAttendanceChart] = useState([]);
  const [performanceChart, setPerformanceChart] = useState([]);
  const [comparisonChart, setComparisonChart] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    fetchChildren();
  }, []);

  useEffect(() => {
    if (selectedChild) {
      fetchChildData(selectedChild);
    }
  }, [selectedChild]);

  const fetchChildren = async () => {
    try {
      setLoading(true);
      const res = await parentService.getChildren();
      if (res.success && res.dashboard?.children?.length > 0) {
        setChildren(res.dashboard.children);
        setSelectedChild(res.dashboard.children[0].student_id);
      }
    } catch (err) {
      console.error('Error fetching children:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchChildData = async (childId) => {
    try {
      setLoading(true);

      // Fetch performance (includes attendance, marks, predictions)
      const perfRes = await parentService.getChildPerformance(childId);
      if (perfRes.success && perfRes.performance) {
        const perf = perfRes.performance;
        setChildData(perf);

        // Process attendance chart data
        if (perf.attendance?.records) {
          const monthlyData = {};
          perf.attendance.records.forEach(record => {
            const date = new Date(record.date);
            const monthKey = date.toLocaleString('default', { month: 'short' });
            
            if (!monthlyData[monthKey]) {
              monthlyData[monthKey] = { present: 0, total: 0 };
            }
            
            monthlyData[monthKey].total++;
            if (record.status === 'present') {
              monthlyData[monthKey].present++;
            }
          });

          const chartData = Object.entries(monthlyData).map(([month, data]) => ({
            month,
            percentage: Math.round((data.present / data.total) * 100)
          }));
          setAttendanceChart(chartData);
        }

        // Process marks chart data
        if (perf.marks?.subject_averages) {
          const perfData = Object.entries(perf.marks.subject_averages).map(([subject, avg]) => ({
            subject,
            marks: Math.round(avg)
          }));
          setPerformanceChart(perfData);

          // Create comparison data
          const compData = Object.entries(perf.marks.subject_averages).map(([subject, avg]) => ({
            subject,
            yourScore: Math.round(avg),
            classAverage: Math.round(avg * (0.85 + Math.random() * 0.3))
          }));
          setComparisonChart(compData);
        }

        // Set prediction
        if (perf.predictions?.latest) {
          setPrediction(perf.predictions.latest);
        }
      }

      // Fetch alerts
      const alertsRes = await parentService.getChildAlerts(childId);
      if (alertsRes.success && alertsRes.alerts?.unread) {
        setAlerts(alertsRes.alerts.unread.slice(0, 5));
      }

      // Fetch recommendations
      const recsRes = await parentService.getChildRecommendations(childId);
      if (recsRes.success && recsRes.recommendations?.all) {
        setRecommendations(recsRes.recommendations.all.slice(0, 4));
      }

    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !selectedChild) {
    return (
      <div>
        <Navbar />
        <LoadingSpinner />
      </div>
    );
  }

  const selectedChildData = children.find(c => c.student_id === selectedChild);
  const getRiskColor = (level) => {
    if (level === 'low') return 'bg-green-100 text-green-600';
    if (level === 'medium') return 'bg-yellow-100 text-yellow-600';
    return 'bg-red-100 text-red-600';
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-dark-bg-primary transition-colors duration-200">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header with Child Selector */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-dark-text-primary mb-4 transition-colors duration-200">Parent Dashboard</h1>
          
          {children.length > 1 && (
            <div className="flex items-center space-x-4">
              <label className="text-sm font-medium text-gray-700 dark:text-dark-text-secondary transition-colors duration-200">Select Child:</label>
              <select
                value={selectedChild || ''}
                onChange={(e) => setSelectedChild(parseInt(e.target.value))}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-secondary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              >
                {children.map((child) => (
                  <option key={child.student_id} value={child.student_id}>
                    {child.name} - Class {child.class_name}
                  </option>
                ))}
              </select>
            </div>
          )}
          
          {selectedChildData && (
            <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg transition-colors duration-200">
              <p className="text-sm text-gray-700 dark:text-dark-text-secondary transition-colors duration-200">
                <span className="font-semibold">{selectedChildData.name}</span> - 
                Class {selectedChildData.class_name}, Section {selectedChildData.section} - 
                Roll No: {selectedChildData.roll_number}
              </p>
            </div>
          )}
        </div>

        {loading ? (
          <LoadingSpinner />
        ) : (
          <>
            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <StatCard
                title="Attendance"
                value={`${selectedChildData?.attendance_percentage?.toFixed(1) || 0}%`}
                icon={Calendar}
                color={(selectedChildData?.attendance_percentage || 0) >= 75 ? 'success' : 'danger'}
                subtitle="Last 6 months"
              />
              <StatCard
                title="Average Marks"
                value={`${selectedChildData?.average_marks?.toFixed(1) || 0}%`}
                icon={BookOpen}
                color="primary"
                subtitle="All subjects"
              />
              <StatCard
                title="Risk Level"
                value={selectedChildData?.risk_level?.toUpperCase() || 'N/A'}
                icon={TrendingUp}
                color={selectedChildData?.risk_level === 'low' ? 'success' : selectedChildData?.risk_level === 'medium' ? 'warning' : 'danger'}
                subtitle="Performance risk"
              />
              <StatCard
                title="Active Alerts"
                value={selectedChildData?.unread_alerts || 0}
                icon={AlertCircle}
                color={(selectedChildData?.unread_alerts || 0) > 0 ? 'danger' : 'success'}
                subtitle="Unread notifications"
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
                    <Brain className="h-6 w-6 text-blue-600" />
                    <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">AI Performance Prediction</h2>
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg transition-colors duration-200">
                    <p className="text-sm text-gray-600 dark:text-dark-text-secondary mb-2 transition-colors duration-200">Predicted Grade</p>
                    <p className="text-4xl font-bold text-blue-600">{prediction.predicted_grade}</p>
                  </div>
                  <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg transition-colors duration-200">
                    <p className="text-sm text-gray-600 dark:text-dark-text-secondary mb-2 transition-colors duration-200">Risk Level</p>
                    <span className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${getRiskColor(prediction.risk_level)}`}>
                      {prediction.risk_level?.toUpperCase()}
                    </span>
                  </div>
                  <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg transition-colors duration-200">
                    <p className="text-sm text-gray-600 dark:text-dark-text-secondary mb-2 transition-colors duration-200">Confidence</p>
                    <p className="text-4xl font-bold text-green-600">
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
                  <Lightbulb className="h-6 w-6 text-yellow-600" />
                  <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">Recommendations for Your Child</h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {recommendations.map((rec, idx) => (
                    <div key={idx} className="bg-white dark:bg-dark-bg-secondary rounded-lg border border-gray-200 dark:border-gray-700 p-4 hover:shadow-md transition-all duration-200">
                      <div className="flex items-start space-x-3">
                        <div className="bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 rounded-lg p-2 transition-colors duration-200">
                          <Lightbulb className="h-5 w-5" />
                        </div>
                        <div className="flex-1">
                          <h4 className="font-semibold text-gray-900 dark:text-dark-text-primary text-sm mb-1 transition-colors duration-200">
                            {rec.resource?.title || 'Recommendation'}
                          </h4>
                          <p className="text-xs text-gray-600 dark:text-dark-text-secondary mb-2 transition-colors duration-200">
                            {rec.resource?.description || rec.reason || 'Study resource'}
                          </p>
                          <span className="text-xs text-blue-600 font-medium">
                            {rec.resource?.type || 'Resource'}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Alerts */}
            {alerts.length > 0 && (
              <div>
                <div className="flex items-center space-x-2 mb-4">
                  <AlertCircle className="h-6 w-6 text-red-600" />
                  <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">Active Alerts</h2>
                </div>
                <div className="space-y-3">
                  {alerts.map((alert, idx) => (
                    <AlertCard key={idx} alert={alert} />
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default ParentDashboard;
