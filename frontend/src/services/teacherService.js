import api from './api';

export const getDashboard = async () => {
  const response = await api.get('/teacher/dashboard');
  return response.data;
};

export const getStudents = async () => {
  const response = await api.get('/teacher/students');
  return response.data;
};

export const uploadAttendance = async (data) => {
  const response = await api.post('/teacher/attendance', data);
  return response.data;
};

export const uploadMarks = async (data) => {
  const response = await api.post('/teacher/marks', data);
  return response.data;
};

export const getAnalytics = async () => {
  const response = await api.get('/teacher/analytics');
  return response.data;
};

export const getAtRiskStudents = async () => {
  const response = await api.get('/teacher/at-risk-students');
  return response.data;
};

export const sendAlert = async (alertData) => {
  const response = await api.post('/teacher/send-alert', alertData);
  return response.data;
};

export const getAttendanceRecords = async () => {
  const response = await api.get('/teacher/attendance');
  return response.data;
};

export const getMarksRecords = async () => {
  const response = await api.get('/teacher/marks');
  return response.data;
};
