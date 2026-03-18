import { useState, useEffect } from 'react';
import { Users, UserCheck, AlertTriangle, TrendingUp, Upload } from 'lucide-react';
import Navbar from '../components/Navbar';
import StatCard from '../components/StatCard';
import LoadingSpinner from '../components/LoadingSpinner';
import StudentsTable from '../components/Tables/StudentsTable';
import AttendanceForm from '../components/Forms/AttendanceForm';
import MarksForm from '../components/Forms/MarksForm';
import * as teacherService from '../services/teacherService';
import toast from 'react-hot-toast';

const TeacherDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [dashboard, setDashboard] = useState(null);
  const [students, setStudents] = useState([]);
  const [atRiskStudents, setAtRiskStudents] = useState([]);
  const [activeTab, setActiveTab] = useState('attendance');

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      
      // Fetch dashboard
      try {
        const res = await teacherService.getDashboard();
        if (res.success) {
          setDashboard(res.dashboard);
        }
      } catch (err) {
        console.error('Dashboard error:', err);
      }

      // Fetch students
      try {
        const res = await teacherService.getStudents();
        if (res.success) {
          setStudents(res.students || []);
        }
      } catch (err) {
        console.error('Students error:', err);
      }

      // Fetch at-risk students
      try {
        const res = await teacherService.getAtRiskStudents();
        if (res.success) {
          setAtRiskStudents(res.at_risk_students || []);
        }
      } catch (err) {
        console.error('At-risk error:', err);
      }

    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAttendanceUpload = async (data) => {
    try {
      await teacherService.uploadAttendance(data);
      toast.success('Attendance uploaded successfully!');
      fetchAllData();
    } catch (error) {
      toast.error('Failed to upload attendance');
      throw error;
    }
  };

  const handleMarksUpload = async (data) => {
    try {
      await teacherService.uploadMarks(data);
      toast.success('Marks uploaded successfully!');
      fetchAllData();
    } catch (error) {
      toast.error('Failed to upload marks');
      throw error;
    }
  };

  const handleSendAlert = async (studentId) => {
    try {
      await teacherService.sendAlert({
        student_id: studentId,
        message: 'You are at risk. Please improve your attendance and performance.',
        severity: 'warning'
      });
      toast.success('Alert sent successfully!');
    } catch (error) {
      toast.error('Failed to send alert');
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

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-dark-bg-primary transition-colors duration-200">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">
            Welcome, {dashboard?.teacher_info?.name || 'Teacher'}!
          </h1>
          <p className="text-gray-600 dark:text-dark-text-secondary mt-1 transition-colors duration-200">
            {dashboard?.teacher_info?.subject} - {dashboard?.teacher_info?.department}
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Students"
            value={dashboard?.total_students || 0}
            icon={Users}
            color="primary"
            subtitle="In your classes"
          />
          <StatCard
            title="Present Today"
            value={dashboard?.present_today || 0}
            icon={UserCheck}
            color="success"
            subtitle="Attendance today"
          />
          <StatCard
            title="At-Risk Students"
            value={dashboard?.at_risk_students || 0}
            icon={AlertTriangle}
            color="danger"
            subtitle="Need attention"
          />
          <StatCard
            title="Class Average"
            value={`${(dashboard?.class_average || 0).toFixed(1)}%`}
            icon={TrendingUp}
            color="warning"
            subtitle="Overall performance"
          />
        </div>

        {/* Upload Section */}
        <div className="mb-8">
          <div className="bg-white dark:bg-dark-bg-secondary rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors duration-200">
            <div className="border-b border-gray-200 dark:border-gray-700">
              <div className="flex space-x-4 px-6">
                <button
                  onClick={() => setActiveTab('attendance')}
                  className={`py-4 px-4 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === 'attendance'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 dark:text-dark-text-secondary hover:text-gray-700 dark:hover:text-dark-text-primary'
                  }`}
                >
                  <Upload className="inline h-4 w-4 mr-2" />
                  Upload Attendance
                </button>
                <button
                  onClick={() => setActiveTab('marks')}
                  className={`py-4 px-4 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === 'marks'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 dark:text-dark-text-secondary hover:text-gray-700 dark:hover:text-dark-text-primary'
                  }`}
                >
                  <Upload className="inline h-4 w-4 mr-2" />
                  Upload Marks
                </button>
              </div>
            </div>
            <div className="p-6">
              {activeTab === 'attendance' ? (
                <AttendanceForm students={students} onSubmit={handleAttendanceUpload} />
              ) : (
                <MarksForm students={students} onSubmit={handleMarksUpload} />
              )}
            </div>
          </div>
        </div>

        {/* At-Risk Students */}
        {atRiskStudents.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary mb-4 flex items-center transition-colors duration-200">
              <AlertTriangle className="h-6 w-6 text-red-600 mr-2" />
              At-Risk Students
            </h2>
            <div className="bg-white dark:bg-dark-bg-secondary rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors duration-200">
              <div className="divide-y divide-gray-200 dark:divide-gray-700">
                {atRiskStudents.map((student, idx) => (
                  <div key={idx} className="p-4 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200">
                    <div>
                      <p className="font-semibold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">
                        {student.name} ({student.roll_number})
                      </p>
                      <p className="text-sm text-gray-600 dark:text-dark-text-secondary transition-colors duration-200">
                        Class {student.class_name} - Section {student.section}
                      </p>
                      <p className="text-sm text-red-600 mt-1">
                        {student.reason || 'Low attendance or poor performance'}
                      </p>
                    </div>
                    <button
                      onClick={() => handleSendAlert(student.student_id)}
                      className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium"
                    >
                      Send Alert
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Students Table */}
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary mb-4 transition-colors duration-200">All Students</h2>
          <StudentsTable students={students} />
        </div>
      </div>
    </div>
  );
};

export default TeacherDashboard;
