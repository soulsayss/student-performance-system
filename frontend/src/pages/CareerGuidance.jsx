import { useState, useEffect } from 'react'
import { 
  Compass, 
  Heart, 
  Share2, 
  ChevronDown, 
  ChevronUp,
  CheckCircle,
  AlertCircle,
  TrendingUp,
  Code,
  Briefcase,
  BookOpen,
  Award,
  Search,
  Filter
} from 'lucide-react'
import Navbar from '../components/Navbar'
import LoadingSpinner from '../components/LoadingSpinner'
import api from '../services/api'

const CareerGuidance = () => {
  const [loading, setLoading] = useState(true)
  const [careers, setCareers] = useState([])
  const [subjectStrengths, setSubjectStrengths] = useState({})
  const [expandedCard, setExpandedCard] = useState(null)
  const [favorites, setFavorites] = useState(new Set())
  const [filter, setFilter] = useState('all')
  const [sortBy, setSortBy] = useState('match')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchCareerData()
  }, [])

  const fetchCareerData = async () => {
    try {
      setLoading(true)
      
      // Fetch career suggestions
      const careerRes = await api.get('/student/career-suggestions')
      if (careerRes.data.success) {
        setCareers(careerRes.data.career_suggestions.all || [])
      }
      
      // Fetch marks for subject strengths
      const marksRes = await api.get('/student/marks')
      if (marksRes.data.success && marksRes.data.marks?.subject_averages) {
        setSubjectStrengths(marksRes.data.marks.subject_averages)
      }
    } catch (err) {
      console.error('Error fetching career data:', err)
    } finally {
      setLoading(false)
    }
  }

  const getMatchColor = (percentage) => {
    if (percentage >= 80) return 'text-green-600 dark:text-green-400'
    if (percentage >= 60) return 'text-blue-600 dark:text-blue-400'
    return 'text-gray-400 dark:text-gray-500'
  }

  const getMatchBgColor = (percentage) => {
    if (percentage >= 80) return 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
    if (percentage >= 60) return 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800'
    return 'bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700'
  }

  const getCareerIcon = (careerPath) => {
    const path = careerPath.toLowerCase()
    if (path.includes('engineer') || path.includes('developer') || path.includes('programmer')) return '💻'
    if (path.includes('doctor') || path.includes('medical')) return '🏥'
    if (path.includes('teacher') || path.includes('education')) return '📚'
    if (path.includes('business') || path.includes('manager')) return '💼'
    if (path.includes('artist') || path.includes('design')) return '🎨'
    if (path.includes('scientist') || path.includes('research')) return '🔬'
    if (path.includes('lawyer') || path.includes('legal')) return '⚖️'
    if (path.includes('architect')) return '🏗️'
    return '🎯'
  }

  const filteredCareers = careers
    .filter(career => {
      if (filter === 'high') return career.match_percentage >= 80
      if (filter === 'medium') return career.match_percentage >= 60 && career.match_percentage < 80
      if (filter === 'explore') return career.match_percentage < 60
      return true
    })
    .filter(career => career.career_path.toLowerCase().includes(searchTerm.toLowerCase()))
    .sort((a, b) => {
      if (sortBy === 'match') return b.match_percentage - a.match_percentage
      if (sortBy === 'alpha') return a.career_path.localeCompare(b.career_path)
      return 0
    })

  const topStrengths = Object.entries(subjectStrengths)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 3)

  const toggleFavorite = (careerPath) => {
    const newFavorites = new Set(favorites)
    if (newFavorites.has(careerPath)) {
      newFavorites.delete(careerPath)
    } else {
      newFavorites.add(careerPath)
    }
    setFavorites(newFavorites)
  }

  const shareCareer = (career) => {
    const text = `Check out this career path: ${career.career_path} (${career.match_percentage}% match) - Student Academic System`
    if (navigator.share) {
      navigator.share({
        title: 'Career Suggestion',
        text: text
      })
    } else {
      navigator.clipboard.writeText(text)
      alert('Career path copied to clipboard!')
    }
  }

  if (loading) {
    return (
      <div>
        <Navbar />
        <LoadingSpinner />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Compass className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Career Guidance</h1>
          </div>
          <p className="text-gray-600 dark:text-gray-400">Personalized career paths based on your academic strengths</p>
        </div>

        {/* Subject Strengths */}
        {topStrengths.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700 mb-8">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Your Top Strengths</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {topStrengths.map(([subject, score]) => (
                <div key={subject} className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-900/10 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-gray-900 dark:text-white">{subject}</h3>
                    <TrendingUp className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div className="flex items-end gap-2">
                    <span className="text-3xl font-bold text-blue-600 dark:text-blue-400">{Math.round(score)}</span>
                    <span className="text-sm text-gray-600 dark:text-gray-400 mb-1">%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-3">
                    <div
                      className="bg-blue-600 dark:bg-blue-400 h-2 rounded-full"
                      style={{ width: `${score}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Filters and Search */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search careers..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Filter */}
            <div className="flex gap-2">
              <Filter className="w-5 h-5 text-gray-600 dark:text-gray-400 mt-2" />
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Careers</option>
                <option value="high">High Match (80%+)</option>
                <option value="medium">Medium Match (60-80%)</option>
                <option value="explore">Explore (&lt;60%)</option>
              </select>
            </div>

            {/* Sort */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="match">Sort by Match %</option>
              <option value="alpha">Sort Alphabetically</option>
            </select>
          </div>
        </div>

        {/* Career Cards */}
        {filteredCareers.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCareers.map((career) => (
              <div
                key={career.suggestion_id}
                className={`rounded-lg shadow-md border transition-all duration-200 overflow-hidden ${getMatchBgColor(career.match_percentage)}`}
              >
                {/* Card Header */}
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-start gap-3 flex-1">
                      <span className="text-4xl">{getCareerIcon(career.career_path)}</span>
                      <div className="flex-1">
                        <h3 className="text-lg font-bold text-gray-900 dark:text-white">{career.career_path}</h3>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => toggleFavorite(career.career_path)}
                        className="p-2 hover:bg-white/50 dark:hover:bg-gray-700/50 rounded-lg transition"
                      >
                        <Heart
                          className={`w-5 h-5 ${
                            favorites.has(career.career_path)
                              ? 'fill-red-500 text-red-500'
                              : 'text-gray-400 dark:text-gray-500'
                          }`}
                        />
                      </button>
                      <button
                        onClick={() => shareCareer(career)}
                        className="p-2 hover:bg-white/50 dark:hover:bg-gray-700/50 rounded-lg transition"
                      >
                        <Share2 className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                      </button>
                    </div>
                  </div>

                  {/* Match Percentage */}
                  <div className="flex items-center gap-4 mb-4">
                    <div className="relative w-20 h-20">
                      <svg className="w-20 h-20 transform -rotate-90">
                        <circle
                          cx="40"
                          cy="40"
                          r="36"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          className="text-gray-300 dark:text-gray-600"
                        />
                        <circle
                          cx="40"
                          cy="40"
                          r="36"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeDasharray={`${(career.match_percentage / 100) * 226} 226`}
                          className={getMatchColor(career.match_percentage)}
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className={`text-xl font-bold ${getMatchColor(career.match_percentage)}`}>
                          {Math.round(career.match_percentage)}%
                        </span>
                      </div>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Match Score</p>
                      <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                        {career.match_percentage >= 80
                          ? 'Excellent fit'
                          : career.match_percentage >= 60
                          ? 'Good potential'
                          : 'Explore option'}
                      </p>
                    </div>
                  </div>

                  {/* Required Skills */}
                  {career.required_skills && career.required_skills.length > 0 && (
                    <div className="mb-4">
                      <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Key Skills</p>
                      <div className="flex flex-wrap gap-2">
                        {career.required_skills.slice(0, 3).map((skill, idx) => (
                          <span
                            key={idx}
                            className="px-3 py-1 bg-white/50 dark:bg-gray-700/50 text-xs font-medium text-gray-700 dark:text-gray-300 rounded-full"
                          >
                            {skill}
                          </span>
                        ))}
                        {career.required_skills.length > 3 && (
                          <span className="px-3 py-1 bg-white/50 dark:bg-gray-700/50 text-xs font-medium text-gray-700 dark:text-gray-300 rounded-full">
                            +{career.required_skills.length - 3}
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Description */}
                  {career.description && (
                    <p className="text-sm text-gray-700 dark:text-gray-300 mb-4 line-clamp-2">
                      {career.description}
                    </p>
                  )}

                  {/* Expand Button */}
                  <button
                    onClick={() => setExpandedCard(expandedCard === career.suggestion_id ? null : career.suggestion_id)}
                    className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600 text-white rounded-lg transition flex items-center justify-center gap-2 text-sm font-medium"
                  >
                    {expandedCard === career.suggestion_id ? (
                      <>
                        <ChevronUp className="w-4 h-4" />
                        Show Less
                      </>
                    ) : (
                      <>
                        <ChevronDown className="w-4 h-4" />
                        Learn More
                      </>
                    )}
                  </button>
                </div>

                {/* Expanded Content */}
                {expandedCard === career.suggestion_id && (
                  <div className="border-t border-current/20 p-6 bg-white/30 dark:bg-gray-700/30">
                    <div className="space-y-4">
                      {/* All Skills */}
                      {career.required_skills && career.required_skills.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                            <Code className="w-4 h-4" />
                            All Required Skills
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {career.required_skills.map((skill, idx) => (
                              <span
                                key={idx}
                                className="px-3 py-1 bg-white/70 dark:bg-gray-600/70 text-xs font-medium text-gray-700 dark:text-gray-200 rounded-full"
                              >
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Skill Development */}
                      <div>
                        <h4 className="font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                          <Award className="w-4 h-4" />
                          Skill Development
                        </h4>
                        <div className="space-y-2">
                          <div className="flex items-center gap-2">
                            <CheckCircle className="w-4 h-4 text-green-600 dark:text-green-400" />
                            <span className="text-sm text-gray-700 dark:text-gray-300">Skills you have</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <AlertCircle className="w-4 h-4 text-yellow-600 dark:text-yellow-400" />
                            <span className="text-sm text-gray-700 dark:text-gray-300">Skills to develop</span>
                          </div>
                        </div>
                      </div>

                      {/* Next Steps */}
                      <div>
                        <h4 className="font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                          <BookOpen className="w-4 h-4" />
                          Next Steps
                        </h4>
                        <ul className="text-sm text-gray-700 dark:text-gray-300 space-y-1">
                          <li>• Focus on strengthening your core subjects</li>
                          <li>• Take relevant online courses and certifications</li>
                          <li>• Build projects to showcase your skills</li>
                          <li>• Network with professionals in this field</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-12 border border-gray-200 dark:border-gray-700 text-center">
            <Briefcase className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No careers found</h3>
            <p className="text-gray-600 dark:text-gray-400">Try adjusting your filters or search terms</p>
          </div>
        )}

        {/* Stats */}
        {careers.length > 0 && (
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 border border-gray-200 dark:border-gray-700 text-center">
              <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">{careers.length}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Total Careers</p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 border border-gray-200 dark:border-gray-700 text-center">
              <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                {careers.filter(c => c.match_percentage >= 80).length}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">High Match</p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 border border-gray-200 dark:border-gray-700 text-center">
              <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">{favorites.size}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Favorites</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default CareerGuidance
