import { NavLink } from 'react-router-dom'
import { useCart } from '../context/CartContext'

const items = [
  { to: '/', label: 'المنيو', icon: '🍽️' },
  { to: '/offers', label: 'العروض', icon: '🎁' },
  { to: '/cart', label: 'السلة', icon: '🛒' },
  { to: '/orders', label: 'طلباتي', icon: '🧾' },
  { to: '/stamps', label: 'أختامي', icon: '⭐' },
]

export default function BottomNav() {
  const { count } = useCart()
  return (
    <nav className="fixed bottom-0 inset-x-0 z-30 bg-navy-800/95 backdrop-blur border-t border-navy-700 safe-bottom">
      <ul className="max-w-md mx-auto flex items-stretch justify-between px-1">
        {items.map((item) => (
          <li key={item.to} className="flex-1">
            <NavLink
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                `relative flex flex-col items-center gap-0.5 py-2.5 text-xs transition-colors ${
                  isActive ? 'text-orange' : 'text-cream-soft/70'
                }`
              }
            >
              <span className="text-lg leading-none">{item.icon}</span>
              <span className="font-semibold">{item.label}</span>
              {item.to === '/cart' && count > 0 && (
                <span className="absolute top-1 left-1/2 translate-x-3 min-w-4 h-4 px-1 rounded-full bg-orange text-navy-900 text-[10px] font-bold flex items-center justify-center">
                  {count}
                </span>
              )}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}
