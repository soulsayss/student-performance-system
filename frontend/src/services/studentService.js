import api from './api';

export const getDashboard = async () => {
  const response = await api.get('/student/dashboard');
  return response.data;
};

export const getAttendance = async () => {
  const response = await api.get('/student/attendance');
  return response.data;
};

export const getMarks = async () => {
  const response = await api.get('/student/marks');
  return response.data;
};

export const getPredictions = async () => {
  const response = await api.get('/student/predictions');
  return response.data;
};

export const getRecommendations = async () => {
  const response = await api.get('/student/recommendations');
  return response.data;
};

export const getAchievements = async () => {
  const response = await api.get('/student/achievements');
  return response.data;
};

export const getAlerts = async () => {
  const response = await api.get('/student/alerts');
  return response.data;
};

export const getCareerSuggestions = async () => {
  const response = await api.get('/student/career-suggestions');
  return response.data;
};
