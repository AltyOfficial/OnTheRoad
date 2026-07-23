import axios from 'axios';
import Cookies from 'js-cookie';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8001',
  withCredentials: true,           // ← Добавь это
  timeout: 15000,
});

api.interceptors.request.use((config) => {
  const token = Cookies.get('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry && 
        !originalRequest.url?.includes('/refresh/') && 
        !originalRequest.url?.includes('/logout/')) {
      
      originalRequest._retry = true;

      try {
        const refreshToken = Cookies.get('refresh_token');
        if (!refreshToken) throw error;

        const { data } = await axios.post(
          'http://127.0.0.1:8001/api/v1/auth/refresh/', 
          { refresh: refreshToken },
          { withCredentials: true }
        );

        Cookies.set('access_token', data.access_token, { expires: 1, sameSite: 'Lax', path: '/' });
        if (data.refresh) {
          Cookies.set('refresh_token', data.refresh_token, { expires: 7, sameSite: 'Lax', path: '/' });
        }

        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        return api(originalRequest);
      } catch (e) {
        Cookies.remove('access_token', { path: '/' });
        Cookies.remove('refresh_token', { path: '/' });
        window.location.reload();
      }
    }
    return Promise.reject(error);
  }
);

export default api;