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
  getAll: (params = {}) => api.get('/tasks/', { params: { page_size: 1000, ...params } }),
  getOne: (id) => api.get(`/tasks/${id}/`),
  create: (data) => api.post('/tasks/', data),
  update: (id, data) => api.patch(`/tasks/${id}/`, data),
  delete: (id) => api.delete(`/tasks/${id}/`),
  statistics: () => api.get('/tasks/statistics/'),
  bulkUpdateStatus: (taskIds, status) => api.post('/tasks/bulk_update_status/', {
    task_ids: taskIds,
    status,
  }),
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
