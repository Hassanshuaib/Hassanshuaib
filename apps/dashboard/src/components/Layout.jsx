import { NavLink } from 'react-router-dom'
import Logo from './Logo'
import { useAuth } from '../context/AuthContext'

export default function Layout({ children }) {
  const { logout } = useAuth()

  return (
    <div className="min-h-screen bg-navy-900">
      <header className="sticky top-0 z-20 bg-navy-800/95 backdrop-blur border-b border-navy-700">
        <div className="max-w-6xl mx-auto flex items-center justify-between px-4 py-3 gap-4">
          <Logo />
          <nav className="flex items-center gap-1 bg-navy-900 rounded-full p-1">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                `px-4 py-1.5 rounded-full text-sm font-semibold transition ${
                  isActive ? 'bg-orange text-navy-900' : 'text-cream-soft/70'
                }`
              }
            >
              الطلبات
            </NavLink>
            <NavLink
              to="/stats"
              className={({ isActive }) =>
                `px-4 py-1.5 rounded-full text-sm font-semibold transition ${
                  isActive ? 'bg-orange text-navy-900' : 'text-cream-soft/70'
                }`
              }
            >
              الإحصائيات
            </NavLink>
          </nav>
          <button onClick={logout} className="text-sm font-semibold text-cream-soft/60 hover:text-orange transition">
            تسجيل الخروج
          </button>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-4 py-6">{children}</main>
    </div>
  )
}
