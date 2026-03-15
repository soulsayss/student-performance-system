import api from './api';

export const getDashboard = async () => {
  const response = await api.get('/parent/dashboard');
  return response.data;
};

// Get children from dashboard endpoint
export const getChildren = async () => {
  const response = await api.get('/parent/dashboard');
  return response.data;
};

export const getChildPerformance = async (childId) => {
  const response = await api.get(`/parent/child/${childId}/performance`);
  return response.data;
};

export const getChildAlerts = async (childId) => {
  const response = await api.get(`/parent/child/${childId}/alerts`);
  return response.data;
};

// These are included in getChildPerformance
export const getChildAttendance = async (childId) => {
  const response = await api.get(`/parent/child/${childId}/performance`);
  return response.data;
};

export const getChildMarks = async (childId) => {
  const response = await api.get(`/parent/child/${childId}/performance`);
  return response.data;
};

export const getChildPredictions = async (childId) => {
  const response = await api.get(`/parent/child/${childId}/performance`);
  return response.data;
};

export const getChildRecommendations = async (childId) => {
  const response = await api.get(`/parent/child/${childId}/recommendations`);
  return response.data;
};
