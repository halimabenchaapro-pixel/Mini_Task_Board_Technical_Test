import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;
const API_KEY = localStorage.getItem('apiKey') || import.meta.env.VITE_API_KEY;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add API key to all requests
api.interceptors.request.use((config) => {
  const apiKey = localStorage.getItem('apiKey') || import.meta.env.VITE_API_KEY;
  if (apiKey) {
    config.headers['X-API-KEY'] = apiKey;
  }
  return config;
});

// Task API methods
export const taskAPI = {
  getAll: () => api.get('/tasks/'),
  getOne: (id) => api.get(`/tasks/${id}/`),
  create: (data) => api.post('/tasks/', data),
  update: (id, data) => api.patch(`/tasks/${id}/`, data),
  delete: (id) => api.delete(`/tasks/${id}/`),
};

// Auth helper
export const setApiKey = (key) => {
  localStorage.setItem('apiKey', key);
};

export const getApiKey = () => {
  return localStorage.getItem('apiKey');
};

export const clearApiKey = () => {
  localStorage.removeItem('apiKey');
};

export default api;
