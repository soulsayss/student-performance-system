import { useState, useEffect } from 'react';
import { Users, BookOpen, TrendingUp, Activity, Plus, Edit, Trash2, Search, Upload } from 'lucide-react';
import Navbar from '../components/Navbar';
import StatCard from '../components/StatCard';
import LoadingSpinner from '../components/LoadingSpinner';
import UserModal from '../components/Modals/UserModal';
import ResourceModal from '../components/Modals/ResourceModal';
import CSVImportModal from '../components/Modals/CSVImportModal';
import adminService from '../services/adminService.new';
import toast from 'react-hot-toast';

const AdminDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [dashboard, setDashboard] = useState(null);
  const [users, setUsers] = useState([]);
  const [resources, setResources] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRole, setFilterRole] = useState('all');
  const [showUserModal, setShowUserModal] = useState(false);
  const [showResourceModal, setShowResourceModal] = useState(false);
  const [showCSVImportModal, setShowCSVImportModal] = useState(false);
  const [editingUser, setEditingUser] = useState(null);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);

      // Fetch dashboard/analytics
      try {
        const res = await adminService.getDashboard();
        if (res.success) {
          setDashboard(res.analytics);
        }
      } catch (err) {
        console.error('Dashboard error:', err);
      }

      // Fetch users
      try {
        const res = await adminService.getUsers();
        if (res.success) {
          setUsers(res.users || []);
        }
      } catch (err) {
        console.error('Users error:', err);
      }

      // Fetch resources
      try {
        const res = await adminService.getResources();
        if (res.success) {
          setResources(res.resources || []);
        }
      } catch (err) {
        console.error('Resources error:', err);
      }

    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    
    try {
      await adminService.deleteUser(userId);
      toast.success('User deleted successfully');
      fetchAllData();
    } catch (error) {
      toast.error('Failed to delete user');
    }
  };

  const handleSaveUser = async (userData) => {
    try {
      if (editingUser) {
        await adminService.updateUser(editingUser.user_id, userData);
        toast.success('User updated successfully');
      } else {
        await adminService.createUser(userData);
        toast.success('User created successfully');
      }
      setShowUserModal(false);
      setEditingUser(null);
      fetchAllData();
    } catch (error) {
      toast.error(editingUser ? 'Failed to update user' : 'Failed to create user');
      throw error;
    }
  };

  const handleDeleteResource = async (resourceId) => {
    if (!window.confirm('Are you sure you want to delete this resource?')) return;
    
    try {
      await adminService.deleteResource(resourceId);
      toast.success('Resource deleted successfully');
      fetchAllData();
    } catch (error) {
      toast.error('Failed to delete resource');
    }
  };

  const handleSaveResource = async (resourceData) => {
    try {
      await adminService.createResource(resourceData);
      toast.success('Resource created successfully');
      setShowResourceModal(false);
      fetchAllData();
    } catch (error) {
      toast.error('Failed to create resource');
      throw error;
    }
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = filterRole === 'all' || user.role === filterRole;
    return matchesSearch && matchesRole;
  });

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
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">Admin Dashboard</h1>
              <p className="text-gray-600 dark:text-dark-text-secondary mt-1 transition-colors duration-200">System Management & Analytics</p>
            </div>
            <button
              onClick={() => setShowCSVImportModal(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
            >
              <Upload className="h-4 w-4" />
              <span>Import CSV Data</span>
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Users"
            value={dashboard?.users?.total || 0}
            icon={Users}
            color="primary"
            subtitle="All system users"
          />
          <StatCard
            title="Total Students"
            value={dashboard?.users?.students || 0}
            icon={Users}
            color="success"
            subtitle="Enrolled students"
          />
          <StatCard
            title="Total Resources"
            value={dashboard?.resources?.total || 0}
            icon={BookOpen}
            color="warning"
            subtitle="Learning materials"
          />
          <StatCard
            title="Active Users"
            value={dashboard?.users?.active || 0}
            icon={Activity}
            color="danger"
            subtitle="Active users"
          />
        </div>

        {/* User Management */}
        <div className="bg-white dark:bg-dark-bg-secondary rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 mb-8 transition-colors duration-200">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">User Management</h2>
              <button
                onClick={() => {
                  setEditingUser(null);
                  setShowUserModal(true);
                }}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="h-4 w-4" />
                <span>Add User</span>
              </button>
            </div>

            {/* Filters */}
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search users..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
                />
              </div>
              <select
                value={filterRole}
                onChange={(e) => setFilterRole(e.target.value)}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-dark-bg-primary text-gray-900 dark:text-dark-text-primary transition-colors duration-200"
              >
                <option value="all">All Roles</option>
                <option value="student">Students</option>
                <option value="teacher">Teachers</option>
                <option value="parent">Parents</option>
                <option value="admin">Admins</option>
              </select>
            </div>
          </div>

          {/* Users Table */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-800 transition-colors duration-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-dark-text-secondary uppercase transition-colors duration-200">Name</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-dark-text-secondary uppercase transition-colors duration-200">Email</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-dark-text-secondary uppercase transition-colors duration-200">Role</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-dark-text-secondary uppercase transition-colors duration-200">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-dark-text-secondary uppercase transition-colors duration-200">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-dark-bg-secondary divide-y divide-gray-200 dark:divide-gray-700 transition-colors duration-200">
                {filteredUsers.map((user) => (
                  <tr key={user.user_id} className="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-dark-text-primary transition-colors duration-200">
                      {user.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-dark-text-secondary transition-colors duration-200">
                      {user.email}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        user.role === 'admin' ? 'bg-purple-100 text-purple-600' :
                        user.role === 'teacher' ? 'bg-blue-100 text-blue-600' :
                        user.role === 'student' ? 'bg-green-100 text-green-600' :
                        'bg-yellow-100 text-yellow-600'
                      }`}>
                        {user.role}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-600">
                        Active
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => {
                            setEditingUser(user);
                            setShowUserModal(true);
                          }}
                          className="p-1 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded transition-colors duration-200"
                        >
                          <Edit className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteUser(user.user_id)}
                          className="p-1 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded transition-colors duration-200"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 transition-colors duration-200">
            <p className="text-sm text-gray-700 dark:text-dark-text-secondary transition-colors duration-200">
              Showing {filteredUsers.length} of {users.length} users
            </p>
          </div>
        </div>

        {/* Resource Management */}
        <div className="bg-white dark:bg-dark-bg-secondary rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors duration-200">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900 dark:text-dark-text-primary transition-colors duration-200">Resource Management</h2>
              <button
                onClick={() => setShowResourceModal(true)}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Plus className="h-4 w-4" />
                <span>Add Resource</span>
              </button>
            </div>
          </div>

          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {resources.map((resource) => (
                <div key={resource.resource_id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-all duration-200 bg-white dark:bg-dark-bg-primary">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-gray-900 dark:text-dark-text-primary text-sm transition-colors duration-200">{resource.title}</h3>
                    <button
                      onClick={() => handleDeleteResource(resource.resource_id)}
                      className="p-1 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded transition-colors duration-200"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                  <p className="text-xs text-gray-600 dark:text-dark-text-secondary mb-2 transition-colors duration-200">{resource.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500 dark:text-dark-text-secondary transition-colors duration-200">{resource.type}</span>
                    <span className="text-xs font-medium text-blue-600">{resource.subject}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Modals */}
      <UserModal
        isOpen={showUserModal}
        onClose={() => {
          setShowUserModal(false);
          setEditingUser(null);
        }}
        onSave={handleSaveUser}
        user={editingUser}
      />

      <ResourceModal
        isOpen={showResourceModal}
        onClose={() => setShowResourceModal(false)}
        onSave={handleSaveResource}
      />

      <CSVImportModal
        isOpen={showCSVImportModal}
        onClose={() => setShowCSVImportModal(false)}
        onSuccess={fetchAllData}
      />
    </div>
  );
};

export default AdminDashboard;
