import { useState } from 'react';
import { X } from 'lucide-react';
import api from '../api/client';
import Cookies from 'js-cookie';
import toast from 'react-hot-toast';

type AuthModalProps = {
  isOpen: boolean;
  onClose: () => void;
  mode: 'login' | 'register';
  onSuccess: () => void;
};

export default function AuthModal({ isOpen, onClose, mode, onSuccess }: AuthModalProps) {
  const [isLogin, setIsLogin] = useState(mode === 'login');
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const endpoint = isLogin 
        ? '/api/v1/auth/login/' 
        : '/api/v1/auth/register/';

      const { data } = await api.post(endpoint, { login, password });

      // Сохраняем токены (один раз!)
      Cookies.set('access_token', data.access_token, { 
        expires: 1, 
        sameSite: 'Lax', 
        path: '/' 
        });

        if (data.refresh_token) {
        Cookies.set('refresh_token', data.refresh_token, { 
            expires: 7, 
            sameSite: 'Lax', 
            path: '/' 
        });
    }

      toast.success(isLogin ? 'Успешный вход!' : 'Аккаунт успешно создан!');
      onSuccess();
      onClose();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Что-то пошло не так');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div className="bg-white rounded-3xl w-full max-w-md mx-4 overflow-hidden">
        <div className="flex justify-between items-center p-6 border-b">
          <h2 className="text-2xl font-semibold">
            {isLogin ? 'Вход' : 'Регистрация'}
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          <div>
            <label className="block text-sm font-medium mb-1">Логин</label>
            <input
              type="text"
              value={login}
              onChange={(e) => setLogin(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-emerald-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Пароль</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-emerald-500"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-2xl transition disabled:opacity-70"
          >
            {loading ? 'Подождите...' : isLogin ? 'Войти' : 'Создать аккаунт'}
          </button>
        </form>

        <div className="p-6 border-t text-center text-sm">
          {isLogin ? (
            <p>Нет аккаунта? <button onClick={() => setIsLogin(false)} className="text-emerald-600 font-medium">Зарегистрироваться</button></p>
          ) : (
            <p>Уже есть аккаунт? <button onClick={() => setIsLogin(true)} className="text-emerald-600 font-medium">Войти</button></p>
          )}
        </div>
      </div>
    </div>
  );
}