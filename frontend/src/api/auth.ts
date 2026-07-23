import api from './client';
import Cookies from 'js-cookie';
import toast from 'react-hot-toast';

export const logoutUser = async () => {
  try {
    const refreshToken = Cookies.get('refresh_token');
    
    if (refreshToken) {
      await api.post('/api/v1/auth/logout/', {}, {
        headers: { Authorization: `Bearer ${refreshToken}` }
      });
    }
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    // В любом случае чистим куки
    Cookies.remove('access_token');
    Cookies.remove('refresh_token');
    toast.success('Вы успешно вышли из аккаунта');
    window.location.reload(); // или используй useNavigate
  }
};