import axios from 'axios';

import { clearAuth, getAccessToken, getRefreshToken, storeAccessToken } from './storage';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

let refreshPromise = null;

client.interceptors.request.use((config) => {
  const accessToken = getAccessToken();
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const isAuthRequest = originalRequest?.url?.includes('auth/login/') || originalRequest?.url?.includes('auth/refresh/');

    if (error.response?.status !== 401 || originalRequest?._retry || isAuthRequest) {
      return Promise.reject(error);
    }

    const refreshToken = getRefreshToken();
    if (!refreshToken) {
      clearAuth();
      window.location.assign('/login');
      return Promise.reject(error);
    }

    originalRequest._retry = true;
    try {
      refreshPromise ||= axios
        .post(`${client.defaults.baseURL}auth/refresh/`, { refresh: refreshToken })
        .finally(() => {
          refreshPromise = null;
        });
      const refreshResponse = await refreshPromise;
      storeAccessToken(refreshResponse.data.access);
      originalRequest.headers = originalRequest.headers || {};
      originalRequest.headers.Authorization = `Bearer ${refreshResponse.data.access}`;
      return client(originalRequest);
    } catch (refreshError) {
      clearAuth();
      window.location.assign('/login');
      return Promise.reject(refreshError);
    }
  },
);

export default client;