import { useState } from 'react';
import { Car, MapPin, Users, Award } from 'lucide-react';

function App() {
  const [isLoggedIn] = useState(false);   // или полностью удали, если не нужен

  return (
    <div className="min-h-screen bg-[#f8fafc] text-gray-900">
      {/* Навбар */}
      <nav className="fixed top-0 left-0 right-0 bg-white/90 backdrop-blur-md border-b z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-emerald-600 rounded-xl flex items-center justify-center">
              <Car className="w-5 h-5 text-white" />
            </div>
            <span className="text-2xl font-semibold tracking-tight">В путь</span>
          </div>

          <div className="flex items-center gap-8 text-sm font-medium">
            <a href="#features" className="hover:text-emerald-600 transition-colors">Возможности</a>
            <a href="#about" className="hover:text-emerald-600 transition-colors">О проекте</a>
            {isLoggedIn ? (
              <button
                onClick={() => {/* logout */}}
                className="px-5 py-2 bg-emerald-600 text-white rounded-2xl hover:bg-emerald-700 transition"
              >
                Личный кабинет
              </button>
            ) : (
              <button
                onClick={() => {/* открыть модалку логина */}}
                className="px-5 py-2 bg-emerald-600 text-white rounded-2xl hover:bg-emerald-700 transition"
              >
                Войти
              </button>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-24 pb-20 bg-gradient-to-br from-white via-emerald-50 to-white">
        <div className="max-w-5xl mx-auto px-6 text-center">
          <div className="inline-flex items-center gap-2 bg-emerald-100 text-emerald-700 px-4 py-1.5 rounded-full text-sm mb-6">
            🚗 Путешествуй умнее
          </div>
          
          <h1 className="text-6xl md:text-7xl font-bold tracking-tighter mb-6">
            Дорога ждёт.<br />
            <span className="text-emerald-600">В путь!</span>
          </h1>
          
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-10">
            Планируй поездки, находи попутчиков, делись маршрутами и открывай новые места вместе с друзьями.
          </p>

          <div className="flex gap-4 justify-center">
            <button 
              onClick={() => {/* регистрация */}}
              className="px-8 py-4 bg-emerald-600 hover:bg-emerald-700 text-white text-lg font-semibold rounded-3xl transition-all active:scale-95"
            >
              Начать путешествие
            </button>
            <button 
              onClick={() => document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })}
              className="px-8 py-4 border border-gray-300 hover:bg-gray-50 text-lg font-medium rounded-3xl transition-all"
            >
              Узнать больше
            </button>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-4xl font-bold text-center mb-16">Почему выбирают нас</h2>
          
          <div className="grid md:grid-cols-3 gap-10">
            {[
              {
                icon: <MapPin className="w-10 h-10 text-emerald-600" />,
                title: "Умные маршруты",
                desc: "Автоматический расчёт оптимального пути с учётом пробок, заправок и интересных мест."
              },
              {
                icon: <Users className="w-10 h-10 text-emerald-600" />,
                title: "Попутчики",
                desc: "Находи людей, которые едут в том же направлении. Безопасно и удобно."
              },
              {
                icon: <Award className="w-10 h-10 text-emerald-600" />,
                title: "Сообщество",
                desc: "Делись опытом, оставляй отзывы и собирай крутые коллекции маршрутов."
              }
            ].map((feature, i) => (
              <div key={i} className="bg-white border border-gray-100 p-8 rounded-3xl hover:border-emerald-200 transition-all group">
                <div className="mb-6">{feature.icon}</div>
                <h3 className="text-2xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-gray-600">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center gap-3 mb-6">
            <div className="w-8 h-8 bg-emerald-600 rounded-2xl flex items-center justify-center">
              <Car className="w-4 h-4 text-white" />
            </div>
            <span className="text-white text-xl font-semibold">В путь</span>
          </div>
          <p>© 2026 • Пет-проект для души</p>
        </div>
      </footer>
    </div>
  );
}

export default App;