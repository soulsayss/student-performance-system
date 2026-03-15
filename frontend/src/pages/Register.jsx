import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { UserPlus, Mail, Lock, User, Calendar, BookOpen, Briefcase, Users } from 'lucide-react'
import { register } from '../services/authService'

const Register = () => {
  const navigate = useNavigate()
  const [step, setStep] = useState(1)
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    role: '',
    // Student fields
    roll_number: '',
    class: '',
    section: '',
    dob: '',
    gender: '',
    // Teacher fields
    employee_id: '',
    subject: '',
    department: '',
  })

  const { register: registerField, handleSubmit, formState: { errors }, watch } = useForm()

  const selectedRole = watch('role') || formData.role

  const handleNext = (data) => {
    setFormData({ ...formData, ...data })
    setStep(step + 1)
  }

  const handleBack = () => {
    setStep(step - 1)
  }

  const onSubmit = async (data) => {
    setIsLoading(true)
    try {
      const finalData = { ...formData, ...data }
      
      // Remove empty fields
      Object.keys(finalData).forEach(key => {
        if (finalData[key] === '' || finalData[key] === undefined) {
          delete finalData[key]
        }
      })

      const response = await register(finalData)
      
      if (response.success) {
        toast.success('Registration successful! Please login.')
        navigate('/login')
      } else {
        toast.error(response.message || 'Registration failed')
      }
    } catch (error) {
      console.error('Registration error:', error)
      toast.error('Registration failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-600 via-blue-700 to-purple-700 p-12 flex-col justify-center">
        <div>
          <div className="flex items-center space-x-2 mb-12">
            <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
              <UserPlus className="w-6 h-6 text-blue-600" />
            </div>
            <span className="text-2xl font-bold text-white">Student Academic Performance</span>
          </div>
          
          <div className="text-white">
            <h1 className="text-4xl font-bold mb-6">Join Our Academic Community</h1>
            <p className="text-blue-100 text-lg mb-12">
              Create your account and start your journey towards academic excellence with AI-powered insights.
            </p>
            
            <div className="space-y-6">
              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                  <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Personalized Learning Experience</h3>
                  <p className="text-blue-100 text-sm mt-1">Get tailored recommendations based on your performance</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                  <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Real-Time Performance Tracking</h3>
                  <p className="text-blue-100 text-sm mt-1">Monitor your academic progress with detailed analytics</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                  <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                    <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Smart Recommendations</h3>
                  <p className="text-blue-100 text-sm mt-1">Receive AI-powered suggestions to improve your grades</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                  <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Gamification & Achievements</h3>
                  <p className="text-blue-100 text-sm mt-1">Earn badges and points as you progress</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Registration Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-white overflow-y-auto">
        <div className="w-full max-w-md">
          {/* Mobile Logo */}
          <div className="lg:hidden text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-full mb-4">
              <UserPlus className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900">Student Academic Performance</h1>
          </div>

          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Create Account</h2>
            <p className="text-gray-600">Join the Student Academic System</p>
          </div>

          {/* Progress Steps */}
          <div className="mb-8">
            <div className="flex items-center justify-center space-x-2">
              {[1, 2, 3].map((s) => (
                <div key={s} className="flex items-center">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                    step >= s ? 'bg-blue-600 text-white' : 'bg-gray-300 text-gray-600'
                  }`}>
                    {s}
                  </div>
                  {s < 3 && (
                    <div className={`w-12 h-1 ${step > s ? 'bg-blue-600' : 'bg-gray-300'}`} />
                  )}
                </div>
              ))}
            </div>
            <div className="flex justify-between mt-2 text-sm text-gray-600 px-2">
              <span className={step === 1 ? 'font-semibold text-blue-600' : ''}>Basic Info</span>
              <span className={step === 2 ? 'font-semibold text-blue-600' : ''}>Role</span>
              <span className={step === 3 ? 'font-semibold text-blue-600' : ''}>Details</span>
            </div>
          </div>

          {/* Form Card */}
          <div className="bg-white rounded-lg">
            <form onSubmit={handleSubmit(step === 3 ? onSubmit : handleNext)}>
              {/* Step 1: Basic Information */}
              {step === 1 && (
                <div className="space-y-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Basic Information</h2>
                  
                  {/* Name */}
                  <div>
                    <label htmlFor="name" className="label">Full Name</label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        id="name"
                        type="text"
                        autoComplete="name"
                        className={`input pl-10 ${errors.name ? 'border-danger-500' : ''}`}
                        placeholder="Enter your full name"
                        defaultValue={formData.name}
                        {...registerField('name', { required: 'Name is required' })}
                      />
                    </div>
                    {errors.name && <p className="mt-1 text-sm text-danger-600">{errors.name.message}</p>}
                  </div>

                  {/* Email */}
                  <div>
                    <label htmlFor="email" className="label">Email Address</label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        id="email"
                        type="email"
                        autoComplete="email"
                        className={`input pl-10 ${errors.email ? 'border-danger-500' : ''}`}
                        placeholder="Enter your email"
                        defaultValue={formData.email}
                        {...registerField('email', {
                          required: 'Email is required',
                          pattern: {
                            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                            message: 'Invalid email address'
                          }
                        })}
                      />
                    </div>
                    {errors.email && <p className="mt-1 text-sm text-danger-600">{errors.email.message}</p>}
                  </div>

                  {/* Password */}
                  <div>
                    <label htmlFor="password" className="label">Password</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        id="password"
                        type="password"
                        autoComplete="new-password"
                        className={`input pl-10 ${errors.password ? 'border-danger-500' : ''}`}
                        placeholder="Create a password"
                        defaultValue={formData.password}
                        {...registerField('password', {
                          required: 'Password is required',
                          minLength: {
                            value: 8,
                            message: 'Password must be at least 8 characters'
                          }
                        })}
                      />
                    </div>
                    {errors.password && <p className="mt-1 text-sm text-danger-600">{errors.password.message}</p>}
                  </div>

                  <button type="submit" className="btn btn-primary w-full">
                    Next Step
                  </button>
                </div>
              )}

              {/* Step 2: Role Selection */}
              {step === 2 && (
                <div className="space-y-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Select Your Role</h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Student */}
                    <label className={`cursor-pointer border-2 rounded-lg p-6 transition-all ${
                      selectedRole === 'student' ? 'border-blue-600 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
                    }`}>
                      <input
                        type="radio"
                        value="student"
                        className="hidden"
                        defaultChecked={formData.role === 'student'}
                        {...registerField('role', { required: 'Please select a role' })}
                      />
                      <div className="flex flex-col items-center text-center">
                        <BookOpen className="w-12 h-12 text-blue-600 mb-3" />
                        <h3 className="font-semibold text-gray-900">Student</h3>
                        <p className="text-sm text-gray-600 mt-1">Track your academic progress</p>
                      </div>
                    </label>

                    {/* Teacher */}
                    <label className={`cursor-pointer border-2 rounded-lg p-6 transition-all ${
                      selectedRole === 'teacher' ? 'border-blue-600 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
                    }`}>
                      <input
                        type="radio"
                        value="teacher"
                        className="hidden"
                        defaultChecked={formData.role === 'teacher'}
                        {...registerField('role', { required: 'Please select a role' })}
                      />
                      <div className="flex flex-col items-center text-center">
                        <Briefcase className="w-12 h-12 text-blue-600 mb-3" />
                        <h3 className="font-semibold text-gray-900">Teacher</h3>
                        <p className="text-sm text-gray-600 mt-1">Manage your classes</p>
                      </div>
                    </label>

                    {/* Parent */}
                    <label className={`cursor-pointer border-2 rounded-lg p-6 transition-all ${
                      selectedRole === 'parent' ? 'border-blue-600 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
                    }`}>
                      <input
                        type="radio"
                        value="parent"
                        className="hidden"
                        defaultChecked={formData.role === 'parent'}
                        {...registerField('role', { required: 'Please select a role' })}
                      />
                      <div className="flex flex-col items-center text-center">
                        <Users className="w-12 h-12 text-blue-600 mb-3" />
                        <h3 className="font-semibold text-gray-900">Parent</h3>
                        <p className="text-sm text-gray-600 mt-1">Monitor your child's progress</p>
                      </div>
                    </label>
                  </div>

                  {errors.role && <p className="text-sm text-danger-600">{errors.role.message}</p>}

                  <div className="flex space-x-4">
                    <button type="button" onClick={handleBack} className="btn btn-secondary flex-1">
                      Back
                    </button>
                    <button type="submit" className="btn btn-primary flex-1">
                      Next Step
                    </button>
                  </div>
                </div>
              )}

              {/* Step 3: Role-Specific Information */}
              {step === 3 && (
                <div className="space-y-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Additional Information</h2>

                  {/* Student Fields */}
                  {selectedRole === 'student' && (
                    <>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label htmlFor="roll_number" className="label">Roll Number</label>
                          <input
                            id="roll_number"
                            type="text"
                            className="input"
                            placeholder="e.g., 10A001"
                            defaultValue={formData.roll_number}
                            {...registerField('roll_number', { required: 'Roll number is required' })}
                          />
                          {errors.roll_number && <p className="mt-1 text-sm text-danger-600">{errors.roll_number.message}</p>}
                        </div>

                        <div>
                          <label htmlFor="class" className="label">Class</label>
                          <select
                            id="class"
                            className="input"
                            defaultValue={formData.class}
                            {...registerField('class', { required: 'Class is required' })}
                          >
                            <option value="">Select class</option>
                            <option value="9">Class 9</option>
                            <option value="10">Class 10</option>
                            <option value="11">Class 11</option>
                            <option value="12">Class 12</option>
                          </select>
                          {errors.class && <p className="mt-1 text-sm text-danger-600">{errors.class.message}</p>}
                        </div>

                        <div>
                          <label htmlFor="section" className="label">Section</label>
                          <select
                            id="section"
                            className="input"
                            defaultValue={formData.section}
                            {...registerField('section', { required: 'Section is required' })}
                          >
                            <option value="">Select section</option>
                            <option value="A">Section A</option>
                            <option value="B">Section B</option>
                            <option value="C">Section C</option>
                            <option value="D">Section D</option>
                          </select>
                          {errors.section && <p className="mt-1 text-sm text-danger-600">{errors.section.message}</p>}
                        </div>

                        <div>
                          <label htmlFor="gender" className="label">Gender</label>
                          <select
                            id="gender"
                            className="input"
                            defaultValue={formData.gender}
                            {...registerField('gender', { required: 'Gender is required' })}
                          >
                            <option value="">Select gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                          </select>
                          {errors.gender && <p className="mt-1 text-sm text-danger-600">{errors.gender.message}</p>}
                        </div>
                      </div>

                      <div>
                        <label htmlFor="dob" className="label">Date of Birth</label>
                        <div className="relative">
                          <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                          <input
                            id="dob"
                            type="date"
                            className="input pl-10"
                            defaultValue={formData.dob}
                            {...registerField('dob', { required: 'Date of birth is required' })}
                          />
                        </div>
                        {errors.dob && <p className="mt-1 text-sm text-danger-600">{errors.dob.message}</p>}
                      </div>
                    </>
                  )}

                  {/* Teacher Fields */}
                  {selectedRole === 'teacher' && (
                    <>
                      <div>
                        <label htmlFor="employee_id" className="label">Employee ID</label>
                        <input
                          id="employee_id"
                          type="text"
                          className="input"
                          placeholder="e.g., TCH001"
                          defaultValue={formData.employee_id}
                          {...registerField('employee_id', { required: 'Employee ID is required' })}
                        />
                        {errors.employee_id && <p className="mt-1 text-sm text-danger-600">{errors.employee_id.message}</p>}
                      </div>

                      <div>
                        <label htmlFor="subject" className="label">Subject</label>
                        <input
                          id="subject"
                          type="text"
                          className="input"
                          placeholder="e.g., Mathematics"
                          defaultValue={formData.subject}
                          {...registerField('subject', { required: 'Subject is required' })}
                        />
                        {errors.subject && <p className="mt-1 text-sm text-danger-600">{errors.subject.message}</p>}
                      </div>

                      <div>
                        <label htmlFor="department" className="label">Department</label>
                        <input
                          id="department"
                          type="text"
                          className="input"
                          placeholder="e.g., Science"
                          defaultValue={formData.department}
                          {...registerField('department', { required: 'Department is required' })}
                        />
                        {errors.department && <p className="mt-1 text-sm text-danger-600">{errors.department.message}</p>}
                      </div>
                    </>
                  )}

                  {/* Parent - No additional fields required */}
                  {selectedRole === 'parent' && (
                    <div className="text-center py-8">
                      <Users className="w-16 h-16 text-blue-600 mx-auto mb-4" />
                      <p className="text-gray-600">
                        No additional information required for parent accounts.
                        <br />
                        Click "Complete Registration" to finish.
                      </p>
                    </div>
                  )}

                  <div className="flex space-x-4">
                    <button type="button" onClick={handleBack} className="btn btn-secondary flex-1">
                      Back
                    </button>
                    <button
                      type="submit"
                      disabled={isLoading}
                      className="btn btn-primary flex-1"
                    >
                      {isLoading ? 'Registering...' : 'Complete Registration'}
                    </button>
                  </div>
                </div>
              )}
            </form>

            {/* Login Link */}
            <div className="mt-6 pt-6 border-t border-gray-200 text-center">
              <p className="text-sm text-gray-600">
                Already have an account?{' '}
                <Link to="/login" className="text-blue-600 hover:text-blue-700 font-medium">
                  Sign in here
                </Link>
              </p>
              <div className="mt-3">
                <Link 
                  to="/" 
                  className="text-sm text-gray-500 hover:text-gray-700 inline-flex items-center gap-1"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  Back to Home
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Register
