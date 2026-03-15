import api from './api';

const adminService = {
  getDashboard: async () => {
    const response = await api.get('/admin/analytics');
    return response.data;
  },

  getUsers: async (params = {}) => {
    const response = await api.get('/admin/users', { params });
    return response.data;
  },

  createUser: async (userData) => {
    const response = await api.post('/admin/user', userData);
    return response.data;
  },

  updateUser: async (id, userData) => {
    const response = await api.put('/admin/user/' + id, userData);
    return response.data;
  },

  deleteUser: async (id) => {
    const response = await api.delete('/admin/user/' + id);
    return response.data;
  },

  getAnalytics: async () => {
    const response = await api.get('/admin/analytics');
    return response.data;
  },

  getResources: async (params = {}) => {
    const response = await api.get('/admin/resources', { params });
    return response.data;
  },

  createResource: async (resourceData) => {
    const response = await api.post('/admin/resource', resourceData);
    return response.data;
  },

  deleteResource: async (id) => {
    const response = await api.delete('/admin/resource/' + id);
    return response.data;
  },

  // CSV Import
  importCSVData: async (file, fileType, clearExisting = false) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_type', fileType);
    formData.append('clear_existing', clearExisting.toString());
    
    const response = await api.post('/admin/import-data', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  },

  downloadCSVTemplate: async (templateType) => {
    const response = await api.get(`/admin/csv-template/${templateType}`, {
      responseType: 'blob'
    });
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${templateType}_template.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    
    return { success: true };
  }
};

export default adminService;
