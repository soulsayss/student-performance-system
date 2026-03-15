import { Link } from 'react-router-dom';
import { 
  Brain, 
  AlertTriangle, 
  Lightbulb, 
  Briefcase, 
  Trophy, 
  BarChart3,
  UserPlus,
  Upload,
  TrendingUp,
  Target,
  Facebook,
  Twitter,
  Linkedin,
  Instagram,
  ArrowRight,
  CheckCircle,
  Users,
  Award,
  BookOpen,
  Clock,
  Zap,
  DollarSign,
  FileText,
  Shield,
  Database,
  Code,
  Activity,
  Star,
  TrendingDown,
  Bell,
  Sparkles
} from 'lucide-react';
import { useState, useEffect } from 'react';

const Landing = () => {
  const [counters, setCounters] = useState({
    students: 0,
    accuracy: 0,
    timeSaved: 0,
    roi: 0
  });

  const [legalModal, setLegalModal] = useState({
    isOpen: false,
    title: '',
    content: ''
  });

  const openLegalModal = (type) => {
    const legalContent = {
      privacy: {
        title: 'Privacy Policy',
        content: `
          <h3 class="text-lg font-semibold mb-3">Information Collection and Use</h3>
          <p class="mb-4">This is a demo educational application. We collect minimal personal information necessary for the application to function, including:</p>
          <ul class="list-disc ml-6 mb-4">
            <li>Name and email address for account creation</li>
            <li>Academic records (attendance, marks, assignments)</li>
            <li>User role and profile information</li>
          </ul>
          
          <h3 class="text-lg font-semibold mb-3">Data Security</h3>
          <p class="mb-4">We implement industry-standard security measures to protect your data. All passwords are encrypted, and sensitive information is stored securely.</p>
          
          <h3 class="text-lg font-semibold mb-3">Data Usage</h3>
          <p class="mb-4">Your data is used solely for:</p>
          <ul class="list-disc ml-6 mb-4">
            <li>Providing academic performance tracking</li>
            <li>Generating AI-powered predictions and recommendations</li>
            <li>Facilitating communication between students, teachers, and parents</li>
          </ul>
          
          <p class="text-sm text-gray-600 mt-4">Last updated: February 2026</p>
        `
      },
      terms: {
        title: 'Terms of Service',
        content: `
          <h3 class="text-lg font-semibold mb-3">Acceptance of Terms</h3>
          <p class="mb-4">By accessing and using this Student Academic Performance System, you accept and agree to be bound by the terms and conditions of this agreement.</p>
          
          <h3 class="text-lg font-semibold mb-3">Use License</h3>
          <p class="mb-4">This is an educational demo application. Permission is granted to:</p>
          <ul class="list-disc ml-6 mb-4">
            <li>Access and use the platform for educational purposes</li>
            <li>Create an account and manage academic data</li>
            <li>Utilize AI-powered features and recommendations</li>
          </ul>
          
          <h3 class="text-lg font-semibold mb-3">User Responsibilities</h3>
          <p class="mb-4">Users agree to:</p>
          <ul class="list-disc ml-6 mb-4">
            <li>Provide accurate information</li>
            <li>Maintain the confidentiality of account credentials</li>
            <li>Use the platform responsibly and ethically</li>
            <li>Not attempt to compromise system security</li>
          </ul>
          
          <h3 class="text-lg font-semibold mb-3">Disclaimer</h3>
          <p class="mb-4">This application is provided "as is" for educational and demonstration purposes. While we strive for accuracy, AI predictions should be used as guidance only.</p>
          
          <p class="text-sm text-gray-600 mt-4">Last updated: February 2026</p>
        `
      },
      cookies: {
        title: 'Cookie Policy',
        content: `
          <h3 class="text-lg font-semibold mb-3">What Are Cookies</h3>
          <p class="mb-4">Cookies are small text files stored on your device that help us provide a better user experience.</p>
          
          <h3 class="text-lg font-semibold mb-3">How We Use Cookies</h3>
          <p class="mb-4">This application uses minimal cookies for:</p>
          <ul class="list-disc ml-6 mb-4">
            <li><strong>Authentication:</strong> To keep you logged in securely</li>
            <li><strong>Session Management:</strong> To maintain your session state</li>
            <li><strong>Security:</strong> To protect against unauthorized access</li>
          </ul>
          
          <h3 class="text-lg font-semibold mb-3">Types of Cookies We Use</h3>
          <p class="mb-4"><strong>Essential Cookies:</strong> Required for authentication and core functionality. These cannot be disabled.</p>
          
          <h3 class="text-lg font-semibold mb-3">Managing Cookies</h3>
          <p class="mb-4">You can control cookies through your browser settings. However, disabling cookies may affect the functionality of this application.</p>
          
          <h3 class="text-lg font-semibold mb-3">Third-Party Cookies</h3>
          <p class="mb-4">This application does not use third-party tracking cookies or analytics services.</p>
          
          <p class="text-sm text-gray-600 mt-4">Last updated: February 2026</p>
        `
      }
    };

    setLegalModal({
      isOpen: true,
      title: legalContent[type].title,
      content: legalContent[type].content
    });
  };

  const closeLegalModal = () => {
    setLegalModal({
      isOpen: false,
      title: '',
      content: ''
    });
  };

  // Animated counter effect
  useEffect(() => {
    const duration = 2000;
    const steps = 60;
    const interval = duration / steps;

    const targets = {
      students: 150,
      accuracy: 85,
      timeSaved: 96,
      roi: 1000
    };

    let step = 0;
    const timer = setInterval(() => {
      step++;
      setCounters({
        students: Math.floor((targets.students / steps) * step),
        accuracy: Math.floor((targets.accuracy / steps) * step),
        timeSaved: Math.floor((targets.timeSaved / steps) * step),
        roi: Math.floor((targets.roi / steps) * step)
      });

      if (step >= steps) {
        clearInterval(timer);
        setCounters(targets);
      }
    }, interval);

    return () => clearInterval(timer);
  }, []);

  const features = [
    {
      icon: Brain,
      title: 'Performance Prediction',
      description: 'Random Forest ML model predicts final grades with 85%+ accuracy. Classifies students as LOW/MEDIUM/HIGH risk for early intervention.',
      color: 'blue',
      stats: '85% accuracy'
    },
    {
      icon: AlertTriangle,
      title: 'Early Warning Alerts',
      description: 'Automatic alerts when attendance drops below 75% or marks drop 20%+. Real-time notifications to teachers and parents.',
      color: 'red',
      stats: 'Real-time alerts'
    },
    {
      icon: Briefcase,
      title: 'Career Guidance',
      description: 'Analyzes subject strengths to suggest top 5 career paths with match percentages. Includes required skills and education paths.',
      color: 'green',
      stats: 'Top 5 matches'
    },
    {
      icon: BarChart3,
      title: 'Analytics & Reports',
      description: 'Class-wise performance heatmaps, subject comparison charts, downloadable PDF/CSV reports for 150 students and 3,750 exam marks.',
      color: 'indigo',
      stats: '3,750+ marks tracked'
    },
    {
      icon: Trophy,
      title: 'Gamification',
      description: 'Earn points for attendance, good marks, and improvement. Unlock 8 different badges. Track leaderboard rankings.',
      color: 'purple',
      stats: '8 unique badges'
    },
    {
      icon: Lightbulb,
      title: 'Smart Recommendations',
      description: 'Personalized learning resources based on weak subjects. AI-generated study plans and improvement strategies.',
      color: 'yellow',
      stats: 'Personalized plans'
    }
  ];

  const steps = [
    {
      icon: UserPlus,
      title: 'Register',
      description: 'Create account as Student, Teacher, Parent, or Admin with role-based access control.'
    },
    {
      icon: Upload,
      title: 'Upload Data',
      description: 'Teachers upload marks via CSV (100 students in 30 seconds). Bulk import saves 96% time.'
    },
    {
      icon: TrendingUp,
      title: 'Get Predictions',
      description: 'ML model analyzes 3,750 marks and 19,800 attendance records to predict performance.'
    },
    {
      icon: Target,
      title: 'Improve',
      description: 'Follow personalized recommendations and career guidance to boost academic outcomes.'
    }
  ];

  const testimonials = [
    {
      name: 'Aarav Sharma',
      role: 'Student, Class 10th',
      avatar: 'AS',
      quote: 'This system identified my weak subjects and gave me personalized resources. My marks improved by 15%!',
      color: 'bg-blue-500'
    },
    {
      name: 'Ms. Priya Patel',
      role: 'Mathematics Teacher',
      avatar: 'PP',
      quote: 'CSV upload saves me hours every week. The at-risk alerts help me intervene early before students fall behind.',
      color: 'bg-green-500'
    },
    {
      name: 'Rajesh Kumar',
      role: 'Parent',
      avatar: 'RK',
      quote: 'I can track my child\'s progress 24/7. The career guidance feature helped us plan his future education path.',
      color: 'bg-purple-500'
    }
  ];

  const stats = [
    { icon: Users, label: 'Students', value: counters.students, suffix: '+' },
    { icon: Target, label: 'Accuracy', value: counters.accuracy, suffix: '%' },
    { icon: Clock, label: 'Time Saved', value: counters.timeSaved, suffix: '%' },
    { icon: TrendingUp, label: 'ROI', value: counters.roi, suffix: '%' }
  ];

  const provenResults = {
    students: [
      { icon: Clock, text: '24/7 access to marks and predictions' },
      { icon: Briefcase, text: 'Career guidance based on YOUR subject strengths' },
      { icon: Trophy, text: 'Gamification makes learning engaging' },
      { icon: Bell, text: 'Instant alerts for low attendance or marks' }
    ],
    teachers: [
      { icon: Zap, text: '96% time savings (5 hours → 10 minutes)' },
      { icon: AlertTriangle, text: 'Instant at-risk student identification' },
      { icon: BarChart3, text: 'One-click class analytics and reports' },
      { icon: Upload, text: 'Bulk CSV import for 100+ students' }
    ],
    admins: [
      { icon: DollarSign, text: '90% cost reduction (₹3,00,000 → ₹30,000/year)' },
      { icon: TrendingUp, text: '1000% ROI in first year' },
      { icon: Shield, text: 'Complete audit trail and security' },
      { icon: Database, text: 'Centralized data management' }
    ]
  };

  const technicalHighlights = [
    { icon: Code, label: 'Tech Stack', value: 'React 18 + Flask 3.0' },
    { icon: Brain, label: 'ML Model', value: 'Random Forest (85%+ accuracy)' },
    { icon: CheckCircle, label: 'Tests', value: '93/93 passed (74.3% coverage)' },
    { icon: Users, label: 'Scalability', value: '100+ concurrent users' }
  ];

  return (
    <div className="min-h-screen bg-white dark:bg-dark-bg-primary transition-colors duration-200">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/90 dark:bg-dark-bg-secondary/90 backdrop-blur-sm shadow-sm z-50 transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Brain className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">AcademicPerformance</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link 
                to="/login" 
                className="text-gray-700 dark:text-dark-text-secondary hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors"
              >
                Login
              </Link>
              <Link 
                to="/register" 
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-blue-900/20 dark:via-indigo-900/20 dark:to-purple-900/20 transition-colors duration-200">
        <div className="max-w-7xl mx-auto text-center">
          <div className="inline-flex items-center bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 px-4 py-2 rounded-full mb-6 transition-colors duration-200">
            <Sparkles className="h-4 w-4 mr-2" />
            <span className="text-sm font-semibold">AI-Powered Student Performance Prediction System</span>
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-dark-text-primary mb-6 leading-tight transition-colors duration-200">
            Transform Academic Performance
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              with AI
            </span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-dark-text-secondary mb-4 max-w-3xl mx-auto transition-colors duration-200">
            Predict grades with 85% accuracy • Identify at-risk students early • Provide personalized career guidance
          </p>
          <p className="text-lg text-gray-500 dark:text-dark-text-secondary mb-10 max-w-2xl mx-auto transition-colors duration-200">
            150 students • 3,750 exam marks • 19,800 attendance records • 96% faster data entry
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/register" 
              className="inline-flex items-center justify-center bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition-all transform hover:scale-105 font-semibold text-lg shadow-lg"
            >
              Try Demo Dashboard
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
            <Link 
              to="/login" 
              className="inline-flex items-center justify-center bg-white dark:bg-dark-bg-secondary text-blue-600 dark:text-blue-400 px-8 py-4 rounded-lg hover:bg-gray-50 dark:hover:bg-dark-bg-primary transition-all border-2 border-blue-600 dark:border-blue-500 font-semibold text-lg"
            >
              See Live Predictions
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Bar */}
      <section className="py-12 px-4 sm:px-6 lg:px-8 bg-white dark:bg-dark-bg-secondary border-b border-gray-200 dark:border-gray-700 transition-colors duration-200">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <div key={index} className="text-center">
                  <div className="flex justify-center mb-3">
                    <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center transition-colors duration-200">
                      <Icon className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                    </div>
                  </div>
                  <div className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-dark-text-primary mb-1 transition-colors duration-200">
                    {stat.value}{stat.suffix}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-dark-text-secondary transition-colors duration-200">
                    {stat.label}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-white dark:bg-dark-bg-primary transition-colors duration-200">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-dark-text-primary mb-4 transition-colors duration-200">Powerful Features</h2>
            <p className="text-xl text-gray-600 dark:text-dark-text-secondary max-w-2xl mx-auto transition-colors duration-200">
              Real capabilities backed by actual data and proven results
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              const colorClasses = {
                blue: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600',
                red: 'bg-red-100 dark:bg-red-900/30 text-red-600',
                yellow: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600',
                green: 'bg-green-100 dark:bg-green-900/30 text-green-600',
                purple: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600',
                indigo: 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600'
              };
              
              return (
                <div 
                  key={index}
                  className="p-6 rounded-xl border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-all duration-300 hover:-translate-y-1 bg-white dark:bg-dark-bg-secondary"
                >
                  <div className={`w-14 h-14 rounded-lg ${colorClasses[feature.color]} flex items-center justify-center mb-4 transition-colors duration-200`}>
                    <Icon className="h-7 w-7" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-dark-text-primary mb-2 transition-colors duration-200">{feature.title}</h3>
                  <p className="text-gray-600 dark:text-dark-text-secondary mb-3 transition-colors duration-200">{feature.description}</p>
                  <div className="inline-flex items-center text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 px-3 py-1 rounded-full transition-colors duration-200">
                    <CheckCircle className="h-4 w-4 mr-1" />
                    {feature.stats}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Proven Results Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/10 dark:to-indigo-900/10 transition-colors duration-200">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-dark-text-primary mb-4 transition-colors duration-200">Proven Results</h2>
            <p className="text-xl text-gray-600 dark:text-dark-text-secondary max-w-2xl mx-auto transition-colors duration-200">
              Tangible benefits for students, teachers, and administrators
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* For Students */}
            <div className="bg-white dark:bg-dark-bg-secondary rounded-xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 transition-colors duration-200">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mr-4 transition-colors duration-200">
                  <Users className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">For Students</h3>
              </div>
              <ul className="space-y-4">
                {provenResults.students.map((item, index) => {
                  const Icon = item.icon;
                  return (
                    <li key={index} className="flex items-start">
                      <Icon className="h-5 w-5 text-blue-600 dark:text-blue-400 mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700 dark:text-dark-text-secondary transition-colors duration-200">{item.text}</span>
                    </li>
                  );
                })}
              </ul>
            </div>

            {/* For Teachers */}
            <div className="bg-white dark:bg-dark-bg-secondary rounded-xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 transition-colors duration-200">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mr-4 transition-colors duration-200">
                  <Award className="h-6 w-6 text-green-600 dark:text-green-400" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">For Teachers</h3>
              </div>
              <ul className="space-y-4">
                {provenResults.teachers.map((item, index) => {
                  const Icon = item.icon;
                  return (
                    <li key={index} className="flex items-start">
                      <Icon className="h-5 w-5 text-green-600 dark:text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700 dark:text-dark-text-secondary transition-colors duration-200">{item.text}</span>
                    </li>
                  );
                })}
              </ul>
            </div>

            {/* For Admins */}
            <div className="bg-white dark:bg-dark-bg-secondary rounded-xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 transition-colors duration-200">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mr-4 transition-colors duration-200">
                  <Shield className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">For Admins</h3>
              </div>
              <ul className="space-y-4">
                {provenResults.admins.map((item, index) => {
                  const Icon = item.icon;
                  return (
                    <li key={index} className="flex items-start">
                      <Icon className="h-5 w-5 text-purple-600 dark:text-purple-400 mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700 dark:text-dark-text-secondary transition-colors duration-200">{item.text}</span>
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-dark-bg-secondary transition-colors duration-200">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-dark-text-primary mb-4 transition-colors duration-200">How It Works</h2>
            <p className="text-xl text-gray-600 dark:text-dark-text-secondary max-w-2xl mx-auto transition-colors duration-200">
              Get started in four simple steps
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {steps.map((step, index) => {
              const Icon = step.icon;
              return (
                <div key={index} className="relative">
                  <div className="text-center">
                    <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg">
                      <Icon className="h-10 w-10 text-white" />
                    </div>
                    <div className="absolute top-10 left-1/2 w-full h-0.5 bg-blue-200 dark:bg-blue-800 -z-10 hidden lg:block transition-colors duration-200" 
                         style={{ display: index === steps.length - 1 ? 'none' : 'block' }} />
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-dark-text-primary mb-2 transition-colors duration-200">{step.title}</h3>
                    <p className="text-gray-600 dark:text-dark-text-secondary transition-colors duration-200">{step.description}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white dark:bg-dark-bg-primary transition-colors duration-200">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-dark-text-primary mb-4 transition-colors duration-200">What Users Say</h2>
            <p className="text-xl text-gray-600 dark:text-dark-text-secondary max-w-2xl mx-auto transition-colors duration-200">
              Real feedback from students, teachers, and parents
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div 
                key={index}
                className="bg-gray-50 dark:bg-dark-bg-secondary rounded-xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 transition-colors duration-200"
              >
                <div className="flex items-center mb-6">
                  <div className={`w-12 h-12 ${testimonial.color} rounded-full flex items-center justify-center text-white font-bold text-lg mr-4`}>
                    {testimonial.avatar}
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">{testimonial.name}</div>
                    <div className="text-sm text-gray-600 dark:text-dark-text-secondary transition-colors duration-200">{testimonial.role}</div>
                  </div>
                </div>
                <div className="flex mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-700 dark:text-dark-text-secondary italic transition-colors duration-200">"{testimonial.quote}"</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technical Highlights Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-dark-bg-secondary transition-colors duration-200">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-dark-text-primary mb-4 transition-colors duration-200">Technical Excellence</h2>
            <p className="text-xl text-gray-600 dark:text-dark-text-secondary max-w-2xl mx-auto transition-colors duration-200">
              Built with modern technologies and best practices
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {technicalHighlights.map((highlight, index) => {
              const Icon = highlight.icon;
              return (
                <div 
                  key={index}
                  className="bg-white dark:bg-dark-bg-primary rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700 text-center transition-colors duration-200"
                >
                  <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <Icon className="h-7 w-7 text-white" />
                  </div>
                  <div className="text-sm font-semibold text-gray-600 dark:text-dark-text-secondary mb-2 transition-colors duration-200">{highlight.label}</div>
                  <div className="text-lg font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">{highlight.value}</div>
                </div>
              );
            })}
          </div>
          <div className="mt-12 bg-white dark:bg-dark-bg-primary rounded-xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 transition-colors duration-200">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
              <div>
                <div className="text-3xl font-bold text-blue-600 dark:text-blue-400 mb-2 transition-colors duration-200">3,750+</div>
                <div className="text-gray-600 dark:text-dark-text-secondary transition-colors duration-200">Exam Marks Analyzed</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-green-600 dark:text-green-400 mb-2 transition-colors duration-200">19,800+</div>
                <div className="text-gray-600 dark:text-dark-text-secondary transition-colors duration-200">Attendance Records</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-purple-600 dark:text-purple-400 mb-2 transition-colors duration-200">100+</div>
                <div className="text-gray-600 dark:text-dark-text-secondary transition-colors duration-200">Concurrent Users</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Transform Academic Performance?
          </h2>
          <p className="text-xl text-blue-100 mb-10">
            Join 150+ students and teachers already using our AI-powered system
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/register" 
              className="inline-flex items-center justify-center bg-white text-blue-600 px-8 py-4 rounded-lg hover:bg-gray-100 transition-all transform hover:scale-105 font-semibold text-lg shadow-xl"
            >
              Start Free Today
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
            <Link 
              to="/login" 
              className="inline-flex items-center justify-center bg-transparent text-white px-8 py-4 rounded-lg hover:bg-white/10 transition-all border-2 border-white font-semibold text-lg"
            >
              View Demo
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 dark:bg-black text-gray-300 py-12 px-4 sm:px-6 lg:px-8 transition-colors duration-200">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Brain className="h-8 w-8 text-blue-500" />
                <span className="text-xl font-bold text-white">AcademicPerformance</span>
              </div>
              <p className="text-gray-400 dark:text-gray-500 transition-colors duration-200">
                Transforming education with AI-powered insights and predictions.
              </p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-2">
                <li>
                  <a 
                    href="#features" 
                    onClick={(e) => {
                      e.preventDefault();
                      document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' });
                    }}
                    className="cursor-pointer hover:text-blue-400 transition-colors"
                  >
                    Features
                  </a>
                </li>
                <li>
                  <Link 
                    to="/login" 
                    className="cursor-pointer hover:text-blue-400 transition-colors"
                  >
                    Demo
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Company</h4>
              <ul className="space-y-2">
                <li>
                  <a 
                    href="#about" 
                    onClick={(e) => {
                      e.preventDefault();
                      window.scrollTo({ top: 0, behavior: 'smooth' });
                    }}
                    className="cursor-pointer hover:text-blue-400 transition-colors"
                  >
                    About
                  </a>
                </li>
                <li>
                  <a 
                    href="#contact" 
                    onClick={(e) => {
                      e.preventDefault();
                      document.querySelector('footer')?.scrollIntoView({ behavior: 'smooth' });
                    }}
                    className="cursor-pointer hover:text-blue-400 transition-colors"
                  >
                    Contact
                  </a>
                </li>
                <li>
                  <Link 
                    to="/register" 
                    className="cursor-pointer hover:text-blue-400 transition-colors"
                  >
                    Careers
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Legal</h4>
              <ul className="space-y-2">
                <li>
                  <button 
                    onClick={() => openLegalModal('privacy')}
                    className="cursor-pointer hover:text-blue-400 transition-colors text-left"
                  >
                    Privacy Policy
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => openLegalModal('terms')}
                    className="cursor-pointer hover:text-blue-400 transition-colors text-left"
                  >
                    Terms of Service
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => openLegalModal('cookies')}
                    className="cursor-pointer hover:text-blue-400 transition-colors text-left"
                  >
                    Cookie Policy
                  </button>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 dark:border-gray-900 pt-8 flex flex-col md:flex-row justify-between items-center transition-colors duration-200">
            <p className="text-gray-400 dark:text-gray-500 text-sm mb-4 md:mb-0 transition-colors duration-200">
              © 2026 AcademicPerformance. All rights reserved.
            </p>
            <div className="flex space-x-6">
              <a 
                href="https://facebook.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-blue-400 transition-colors"
              >
                <Facebook className="h-6 w-6" />
              </a>
              <a 
                href="https://twitter.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-blue-400 transition-colors"
              >
                <Twitter className="h-6 w-6" />
              </a>
              <a 
                href="https://linkedin.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-blue-400 transition-colors"
              >
                <Linkedin className="h-6 w-6" />
              </a>
              <a 
                href="https://instagram.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-blue-400 transition-colors"
              >
                <Instagram className="h-6 w-6" />
              </a>
            </div>
          </div>
        </div>
      </footer>

      {/* Legal Modal */}
      {legalModal.isOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            {/* Background overlay */}
            <div 
              className="fixed inset-0 transition-opacity bg-gray-900 bg-opacity-75"
              onClick={closeLegalModal}
            ></div>

            {/* Modal panel */}
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full">
              {/* Header */}
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-2xl font-bold text-white">
                    {legalModal.title}
                  </h3>
                  <button
                    onClick={closeLegalModal}
                    className="text-white hover:text-gray-200 transition-colors"
                  >
                    <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>

              {/* Content */}
              <div className="bg-white px-6 py-6 max-h-96 overflow-y-auto">
                <div 
                  className="text-gray-700 leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: legalModal.content }}
                />
              </div>

              {/* Footer */}
              <div className="bg-gray-50 px-6 py-4 flex justify-end">
                <button
                  onClick={closeLegalModal}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Landing;
