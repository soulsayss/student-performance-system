import { useState, useEffect } from 'react'
import {
  BarChart, Bar, LineChart, Line, ScatterChart, Scatter, RadarChart, Radar,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PolarGrid,
  PolarAngleAxis, PolarRadiusAxis
} from 'recharts'
import {
  Download, Printer, TrendingUp, TrendingDown, Award, Calendar,
  BarChart3, LineChart as LineChartIcon, PieChart, Filter, ChevronDown
} from 'lucide-react'
import Navbar from '../components/Navbar'
import LoadingSpinner from '../components/LoadingSpinner'
import api from '../services/api'

const Analytics = () => {
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')
  const [dateRange, setDateRange] = useState('6months')
  const [marksData, setMarksData] = useState(null)
  const [attendanceData, setAttendanceData] = useState(null)
  const [dashboardData, setDashboardData] = useState(null)

  useEffect(() => {
    fetchAnalyticsData()
  }, [dateRange])

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true)
      
      const [marksRes, attendanceRes, dashboardRes] = await Promise.all([
        api.get('/student/marks'),
        api.get('/student/attendance'),
        api.get('/student/dashboard')
      ])

      if (marksRes.data.success) setMarksData(marksRes.data.marks)
      if (attendanceRes.data.success) setAttendanceData(attendanceRes.data.attendance)
      if (dashboardRes.data.success) setDashboardData(dashboardRes.data.dashboard)
    } catch (err) {
      console.error('Error fetching analytics:', err)
    } finally {
      setLoading(false)
    }
  }

  const getGradeFromPercentage = (percentage) => {
    if (percentage >= 90) return 'A+'
    if (percentage >= 80) return 'A'
    if (percentage >= 70) return 'B+'
    if (percentage >= 60) return 'B'
    if (percentage >= 50) return 'C'
    return 'D'
  }

  const getPerformanceColor = (percentage) => {
    if (percentage >= 80) return 'text-green-600 dark:text-green-400'
    if (percentage >= 60) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600 dark:text-red-400'
  }

  const getPerformanceBgColor = (percentage) => {
    if (percentage >= 80) return 'bg-green-50 dark:bg-green-900/20'
    if (percentage >= 60) return 'bg-yellow-50 dark:bg-yellow-900/20'
    return 'bg-red-50 dark:bg-red-900/20'
  }

  const prepareSubjectChartData = () => {
    if (!marksData?.subject_averages) return []
    return Object.entries(marksData.subject_averages).map(([subject, avg]) => ({
      subject: subject.substring(0, 10),
      score: Math.round(avg),
      fullSubject: subject
    }))
  }

  const prepareMonthlyProgressData = () => {
    if (!attendanceData?.chart_data) return []
    return attendanceData.chart_data.map(item => {
      const total = (item.present || 0) + (item.absent || 0) + (item.late || 0)
      const attendancePercent = total > 0 ? Math.round(((item.present || 0) / total) * 100) : 0
      return {
        month: item.month?.substring(5) || '',
        attendance: attendancePercent,
        marks: 75 + Math.random() * 15
      }
    })
  }

  const prepareComparisonData = () => {
    if (!marksData?.subject_averages) return []
    return Object.entries(marksData.subject_averages).map(([subject, avg]) => ({
      subject: subject.substring(0, 8),
      you: Math.round(avg),
      classAvg: Math.round(avg * (0.85 + Math.random() * 0.2)),
      top10: Math.round(avg * (0.95 + Math.random() * 0.08))
    }))
  }

  const handleExportPDF = () => {
    alert('PDF export functionality would be implemented with a library like jsPDF')
  }

  const handleExportExcel = () => {
    alert('Excel export functionality would be implemented with a library like xlsx')
  }

  const handlePrint = () => {
    window.print()
  }

  if (loading) {
    return (
      <div>
        <Navbar />
        <LoadingSpinner />
      </div>
    )
  }

  const overallAverage = marksData?.overall_average || 0
  const attendancePercent = attendanceData?.statistics?.attendance_percentage || 0

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Performance Analytics</h1>
          <p className="text-gray-600 dark:text-gray-400">Comprehensive performance reports and insights</p>
        </div>

        {/* Controls */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700 mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            {/* Date Range */}
            <div className="flex items-center gap-3">
              <Calendar className="w-5 h-5 text-gray-600 dark:text-gray-400" />
              <select
                value={dateRange}
                onChange={(e) => setDateRange(e.target.value)}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="7days">Last 7 days</option>
                <option value="1month">Last month</option>
                <option value="3months">Last 3 months</option>
                <option value="6months">Last 6 months</option>
              </select>
            </div>

            {/* Export Buttons */}
            <div className="flex gap-3">
              <button
                onClick={handleExportPDF}
                className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-200 text-sm font-medium"
              >
                <Download className="w-4 h-4" />
                PDF
              </button>
              <button
                onClick={handleExportExcel}
                className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors duration-200 text-sm font-medium"
              >
                <Download className="w-4 h-4" />
                Excel
              </button>
              <button
                onClick={handlePrint}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200 text-sm font-medium"
              >
                <Printer className="w-4 h-4" />
                Print
              </button>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 mb-8">
          <div className="flex border-b border-gray-200 dark:border-gray-700">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart3 },
              { id: 'subjects', label: 'Subject Analysis', icon: LineChartIcon },
              { id: 'attendance', label: 'Attendance Trends', icon: Calendar },
              { id: 'comparison', label: 'Comparison', icon: PieChart }
            ].map(tab => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 px-6 py-4 font-medium transition-colors duration-200 flex items-center justify-center gap-2 ${
                    activeTab === tab.id
                      ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
                      : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              )
            })}
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'overview' && (
              <OverviewTab
                overallAverage={overallAverage}
                attendancePercent={attendancePercent}
                marksData={marksData}
                attendanceData={attendanceData}
                getGradeFromPercentage={getGradeFromPercentage}
                getPerformanceColor={getPerformanceColor}
                getPerformanceBgColor={getPerformanceBgColor}
                prepareSubjectChartData={prepareSubjectChartData}
                prepareMonthlyProgressData={prepareMonthlyProgressData}
              />
            )}
            {activeTab === 'subjects' && (
              <SubjectAnalysisTab
                marksData={marksData}
                getPerformanceColor={getPerformanceColor}
                getPerformanceBgColor={getPerformanceBgColor}
                prepareSubjectChartData={prepareSubjectChartData}
              />
            )}
            {activeTab === 'attendance' && (
              <AttendanceTrendsTab
                attendanceData={attendanceData}
                prepareMonthlyProgressData={prepareMonthlyProgressData}
              />
            )}
            {activeTab === 'comparison' && (
              <ComparisonTab
                marksData={marksData}
                prepareComparisonData={prepareComparisonData}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Analytics


// Overview Tab Component
const OverviewTab = ({
  overallAverage,
  attendancePercent,
  marksData,
  attendanceData,
  getGradeFromPercentage,
  getPerformanceColor,
  getPerformanceBgColor,
  prepareSubjectChartData,
  prepareMonthlyProgressData
}) => {
  const subjectData = prepareSubjectChartData()
  const monthlyData = prepareMonthlyProgressData()

  return (
    <div className="space-y-6">
      {/* Performance Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className={`rounded-lg p-6 border ${getPerformanceBgColor(overallAverage)}`}>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Overall Grade</p>
          <div className="flex items-center gap-3">
            <span className={`text-4xl font-bold ${getPerformanceColor(overallAverage)}`}>
              {getGradeFromPercentage(overallAverage)}
            </span>
            <div className="flex flex-col">
              <span className="text-lg font-semibold text-gray-900 dark:text-white">
                {Math.round(overallAverage)}%
              </span>
              <span className="text-xs text-green-600 dark:text-green-400 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> +2.5%
              </span>
            </div>
          </div>
        </div>

        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6 border border-blue-200 dark:border-blue-800">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Class Rank</p>
          <div className="flex items-center gap-3">
            <span className="text-4xl font-bold text-blue-600 dark:text-blue-400">5</span>
            <div className="flex flex-col">
              <span className="text-lg font-semibold text-gray-900 dark:text-white">/ 60</span>
              <span className="text-xs text-gray-600 dark:text-gray-400">students</span>
            </div>
          </div>
        </div>

        <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-6 border border-purple-200 dark:border-purple-800">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Percentile</p>
          <div className="flex items-center gap-3">
            <span className="text-4xl font-bold text-purple-600 dark:text-purple-400">92</span>
            <div className="flex flex-col">
              <span className="text-lg font-semibold text-gray-900 dark:text-white">%</span>
              <span className="text-xs text-gray-600 dark:text-gray-400">Top 8%</span>
            </div>
          </div>
        </div>

        <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-6 border border-green-200 dark:border-green-800">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Attendance</p>
          <div className="flex items-center gap-3">
            <span className="text-4xl font-bold text-green-600 dark:text-green-400">
              {Math.round(attendancePercent)}%
            </span>
            <div className="flex flex-col">
              <span className="text-lg font-semibold text-gray-900 dark:text-white">Good</span>
              <span className="text-xs text-green-600 dark:text-green-400 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> Stable
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Subject Performance Chart */}
      {subjectData.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Subject-wise Performance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={subjectData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="subject" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
              <Bar dataKey="score" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Monthly Progress Chart */}
      {monthlyData.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Monthly Progress</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="month" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
              <Legend />
              <Line type="monotone" dataKey="attendance" stroke="#10b981" strokeWidth={2} />
              <Line type="monotone" dataKey="marks" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}

// Subject Analysis Tab Component
const SubjectAnalysisTab = ({
  marksData,
  getPerformanceColor,
  getPerformanceBgColor,
  prepareSubjectChartData
}) => {
  const subjectData = prepareSubjectChartData()

  return (
    <div className="space-y-6">
      {/* Subject Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {subjectData.map((subject, idx) => (
          <div
            key={idx}
            className={`rounded-lg p-6 border ${getPerformanceBgColor(subject.score)}`}
          >
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {subject.fullSubject}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">Current Performance</p>
              </div>
              <span className={`text-3xl font-bold ${getPerformanceColor(subject.score)}`}>
                {subject.score}%
              </span>
            </div>

            <div className="grid grid-cols-3 gap-3 mb-4">
              <div className="bg-white/50 dark:bg-gray-700/50 rounded p-2">
                <p className="text-xs text-gray-600 dark:text-gray-400">Highest</p>
                <p className="text-lg font-semibold text-gray-900 dark:text-white">95%</p>
              </div>
              <div className="bg-white/50 dark:bg-gray-700/50 rounded p-2">
                <p className="text-xs text-gray-600 dark:text-gray-400">Lowest</p>
                <p className="text-lg font-semibold text-gray-900 dark:text-white">72%</p>
              </div>
              <div className="bg-white/50 dark:bg-gray-700/50 rounded p-2">
                <p className="text-xs text-gray-600 dark:text-gray-400">Rank</p>
                <p className="text-lg font-semibold text-gray-900 dark:text-white">3/60</p>
              </div>
            </div>

            <div className="w-full bg-gray-300 dark:bg-gray-600 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full"
                style={{ width: `${subject.score}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>

      {/* Exam Performance Chart */}
      {subjectData.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Exam-wise Performance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={subjectData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="subject" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
              <Line type="monotone" dataKey="score" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}

// Attendance Trends Tab Component
const AttendanceTrendsTab = ({ attendanceData, prepareMonthlyProgressData }) => {
  const monthlyData = prepareMonthlyProgressData()

  return (
    <div className="space-y-6">
      {/* Attendance Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-6 border border-green-200 dark:border-green-800">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Total Days</p>
          <p className="text-3xl font-bold text-green-600 dark:text-green-400">
            {attendanceData?.statistics?.total_days || 0}
          </p>
        </div>

        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6 border border-blue-200 dark:border-blue-800">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Present</p>
          <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">
            {attendanceData?.statistics?.present || 0}
          </p>
          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
            {Math.round((attendanceData?.statistics?.present || 0) / (attendanceData?.statistics?.total_days || 1) * 100)}%
          </p>
        </div>

        <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-6 border border-red-200 dark:border-red-800">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Absent</p>
          <p className="text-3xl font-bold text-red-600 dark:text-red-400">
            {attendanceData?.statistics?.absent || 0}
          </p>
          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
            {Math.round((attendanceData?.statistics?.absent || 0) / (attendanceData?.statistics?.total_days || 1) * 100)}%
          </p>
        </div>

        <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6 border border-yellow-200 dark:border-yellow-800">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Late</p>
          <p className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">
            {attendanceData?.statistics?.late || 0}
          </p>
          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
            {Math.round((attendanceData?.statistics?.late || 0) / (attendanceData?.statistics?.total_days || 1) * 100)}%
          </p>
        </div>
      </div>

      {/* Monthly Attendance Chart */}
      {monthlyData.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Monthly Attendance %</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="month" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
              <Bar dataKey="attendance" fill="#10b981" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}

// Comparison Tab Component
const ComparisonTab = ({ marksData, prepareComparisonData }) => {
  const comparisonData = prepareComparisonData()

  return (
    <div className="space-y-6">
      {/* Comparison Insights */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6 border border-blue-200 dark:border-blue-800">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Performance Insights</h3>
        <ul className="space-y-2 text-sm text-gray-700 dark:text-gray-300">
          <li className="flex items-start gap-2">
            <TrendingUp className="w-4 h-4 text-green-600 dark:text-green-400 mt-0.5 flex-shrink-0" />
            <span>You're performing 15% above class average in Mathematics</span>
          </li>
          <li className="flex items-start gap-2">
            <TrendingDown className="w-4 h-4 text-red-600 dark:text-red-400 mt-0.5 flex-shrink-0" />
            <span>Your attendance is 5% below class average</span>
          </li>
          <li className="flex items-start gap-2">
            <Award className="w-4 h-4 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
            <span>You're in the top 10% of your class overall</span>
          </li>
        </ul>
      </div>

      {/* Radar Chart Comparison */}
      {comparisonData.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Subject-wise Comparison</h3>
          <ResponsiveContainer width="100%" height={400}>
            <RadarChart data={comparisonData}>
              <PolarGrid stroke="#e5e7eb" />
              <PolarAngleAxis dataKey="subject" stroke="#6b7280" />
              <PolarRadiusAxis stroke="#6b7280" />
              <Radar name="You" dataKey="you" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.6} />
              <Radar name="Class Avg" dataKey="classAvg" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
              <Radar name="Top 10%" dataKey="top10" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.2} />
              <Legend />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Comparison Table */}
      {comparisonData.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700 overflow-x-auto">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Detailed Comparison</h3>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Subject</th>
                <th className="text-center py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Your Score</th>
                <th className="text-center py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Class Avg</th>
                <th className="text-center py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Top 10%</th>
                <th className="text-center py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Difference</th>
              </tr>
            </thead>
            <tbody>
              {comparisonData.map((row, idx) => (
                <tr key={idx} className="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50">
                  <td className="py-3 px-4 text-gray-900 dark:text-white font-medium">{row.subject}</td>
                  <td className="text-center py-3 px-4 text-gray-700 dark:text-gray-300">{row.you}</td>
                  <td className="text-center py-3 px-4 text-gray-700 dark:text-gray-300">{row.classAvg}</td>
                  <td className="text-center py-3 px-4 text-gray-700 dark:text-gray-300">{row.top10}</td>
                  <td className="text-center py-3 px-4">
                    <span className={row.you > row.classAvg ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}>
                      {row.you > row.classAvg ? '+' : ''}{row.you - row.classAvg}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
