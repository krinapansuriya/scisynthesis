import axios from 'axios';

const getBaseURL = () => {
  // In production, use the environment variable for the full API URL
  // In development, use relative path (proxied by Vite)
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  return '/api/v1';
};

const api = axios.create({
  // In production: full URL from VITE_API_URL env var (e.g., https://api.scisynthesis.in/api/v1)
  // In development: relative path that Vite dev server proxies to the FastAPI backend
  // withCredentials: true for httpOnly cookies
  baseURL: getBaseURL(),
  withCredentials: true,
});

// Fallback: if a token is stored in sessionStorage (set by AuthContext on login),
// attach it as a Bearer header. This covers cases where the httpOnly cookie
// is not forwarded correctly (e.g. during first request after login).
// sessionStorage is cleared when the tab closes — safer than localStorage.
api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem('ss_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
