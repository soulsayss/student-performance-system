import { useState, useEffect } from 'react'
import { AlertCircle, TrendingUp, TrendingDown, Zap, BookOpen, CheckCircle, Info } from 'lucide-react'
import api from '../services/api'

const StudentPredictions = () => {
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchPrediction()
  }, [])

  const fetchPrediction = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await api.get('/student/prediction')
      if (response.data.success) {
        setPrediction(response.data.prediction)
      } else {
        setError(response.data.message || 'Failed to fetch prediction')
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Error fetching prediction')
      console.error('Prediction error:', err)
    } finally {
      setLoading(false)
    }
  }

  const getGradeColor = (grade) => {
    if (['A+', 'A'].includes(grade)) return 'text-green-500 bg-green-50 dark:bg-green-900/20'
    if (['B+', 'B'].includes(grade)) return 'text-blue-500 bg-blue-50 dark:bg-blue-900/20'
    if (['C+', 'C'].includes(grade)) return 'text-yellow-500 bg-yellow-50 dark:bg-yellow-900/20'
    return 'text-red-500 bg-red-50 dark:bg-red-900/20'
  }

  const getRiskColor = (risk) => {
    if (risk === 'Low') return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
    if (risk === 'Medium') return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
    return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
  }

  const getTrendIcon = (trend) => {
    if (trend === 'Improving') return <TrendingUp className="w-5 h-5 text-green-500" />
    if (trend === 'Declining') return <TrendingDown className="w-5 h-5 text-red-500" />
    return <Zap className="w-5 h-5 text-yellow-500" />
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
        <div className="max-w-6xl mx-auto">
          <div className="animate-pulse space-y-6">
            <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
              <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
        <div className="max-w-6xl mx-auto">
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-6 h-6 text-red-600 dark:text-red-400" />
              <div>
                <h3 className="font-semibold text-red-900 dark:text-red-300">{error}</h3>
                <p className="text-sm text-red-700 dark:text-red-400 mt-1">
                  Prediction will be available after first month of data collection.
                </p>
              </div>
            </div>
            <button
              onClick={fetchPrediction}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (!prediction) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
        <div className="max-w-6xl mx-auto">
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
            <div className="flex items-center gap-3">
              <Info className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              <div>
                <h3 className="font-semibold text-blue-900 dark:text-blue-300">No Prediction Available</h3>
                <p className="text-sm text-blue-700 dark:text-blue-400 mt-1">
                  Predictions will be available after we collect enough data about your performance.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Performance Predictions</h1>
          <p className="text-gray-600 dark:text-gray-400">AI-powered insights based on your academic performance</p>
          <div className="flex items-center gap-2 mt-3 text-sm text-gray-500 dark:text-gray-400">
            <Info className="w-4 h-4" />
            <span>Predictions are based on Random Forest ML model analyzing your attendance, marks, and assignment completion</span>
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Card 1: Current Prediction */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Current Prediction</h2>
            
            <div className="flex items-center justify-between mb-8">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Predicted Grade</p>
                <div className={`text-5xl font-bold ${getGradeColor(prediction.predicted_grade)} px-6 py-4 rounded-lg inline-block`}>
                  {prediction.predicted_grade}
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Risk Level</p>
                <span className={`px-4 py-2 rounded-full font-semibold ${getRiskColor(prediction.risk_level)}`}>
                  {prediction.risk_level}
                </span>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Confidence Score</span>
                  <span className="text-sm font-semibold text-gray-900 dark:text-white">{prediction.confidence_score}%</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all"
                    style={{ width: `${prediction.confidence_score}%` }}
                  ></div>
                </div>
              </div>

              <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Last Updated: <span className="font-semibold text-gray-900 dark:text-white">{new Date(prediction.prediction_date).toLocaleDateString()}</span>
                </p>
              </div>
            </div>
          </div>

          {/* Card 2: Prediction Factors */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Prediction Factors</h2>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <BookOpen className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Attendance Impact</span>
                </div>
                <span className="text-lg font-bold text-gray-900 dark:text-white">{prediction.factors?.attendance || 0}%</span>
              </div>

              <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <Zap className="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Marks Impact</span>
                </div>
                <span className="text-lg font-bold text-gray-900 dark:text-white">{prediction.factors?.marks || 0}%</span>
              </div>

              <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400" />
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Assignment Completion</span>
                </div>
                <span className="text-lg font-bold text-gray-900 dark:text-white">{prediction.factors?.assignments || 0}%</span>
              </div>

              <div className="pt-4 border-t border-gray-200 dark:border-gray-700 flex items-center gap-2">
                {getTrendIcon(prediction.trend)}
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Trend: <span className="font-semibold text-gray-900 dark:text-white">{prediction.trend}</span>
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Card 3: Subject-wise Predictions */}
        {prediction.subject_predictions && prediction.subject_predictions.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700 mb-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Subject-wise Predictions</h2>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Subject</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Current Score</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Predicted Score</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Confidence</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {prediction.subject_predictions.map((subject, idx) => (
                    <tr key={idx} className="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50">
                      <td className="py-3 px-4 text-gray-900 dark:text-white font-medium">{subject.subject}</td>
                      <td className="py-3 px-4 text-gray-700 dark:text-gray-300">{subject.current_score}</td>
                      <td className="py-3 px-4 text-gray-700 dark:text-gray-300">{subject.predicted_score}</td>
                      <td className="py-3 px-4 text-gray-700 dark:text-gray-300">{subject.confidence}%</td>
                      <td className="py-3 px-4">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                          subject.status === 'On track'
                            ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
                            : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
                        }`}>
                          {subject.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Card 4: Recommendations */}
        {prediction.recommendations && prediction.recommendations.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Recommendations</h2>
            
            <div className="space-y-3">
              {prediction.recommendations.map((rec, idx) => (
                <div key={idx} className="flex items-start gap-3 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                  <CheckCircle className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                  <p className="text-gray-700 dark:text-gray-300">{rec}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default StudentPredictions
