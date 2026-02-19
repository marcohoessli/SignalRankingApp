import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth
export const signup = (data) => api.post('/api/auth/signup', data);
export const login = (data) => api.post('/api/auth/login', data);
export const getMe = () => api.get('/api/auth/me');
export const verifyEmail = (token) => api.get(`/api/auth/verify-email?token=${token}`);
export const requestPasswordReset = (email) => api.post('/api/auth/request-password-reset', { email });
export const resetPassword = (data) => api.post('/api/auth/reset-password', data);

// Questions
export const getQuestions = (params) => api.get('/api/questions', { params });
export const getQuestion = (id) => api.get(`/api/questions/${id}`);
export const createQuestion = (data) => api.post('/api/questions', data);
export const updateQuestion = (id, data) => api.put(`/api/questions/${id}`, data);
export const closeQuestion = (id) => api.post(`/api/questions/${id}/close`);
export const resolveQuestion = (id, outcome) => api.post(`/api/questions/${id}/resolve`, { outcome });
export const deleteQuestion = (id) => api.delete(`/api/questions/${id}`);

// Predictions
export const getMyPredictions = () => api.get('/api/predictions');
export const createPrediction = (data) => api.post('/api/predictions', data);
export const updatePrediction = (id, data) => api.put(`/api/predictions/${id}`, data);
export const getPredictionForQuestion = (questionId) => api.get(`/api/predictions/question/${questionId}`);

// Leaderboard
export const getLeaderboard = (params) => api.get('/api/leaderboard', { params });

export default api;
