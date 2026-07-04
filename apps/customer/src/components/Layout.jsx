import { Link } from 'react-router-dom'
import Logo from './Logo'
import BottomNav from './BottomNav'

export default function Layout({ children, showHeader = true }) {
  return (
    <div className="min-h-screen flex flex-col bg-navy-900 spice-bg">
      {showHeader && (
        <header className="safe-top sticky top-0 z-20 bg-navy-900/90 backdrop-blur border-b border-navy-700">
          <div className="max-w-md mx-auto flex items-center justify-between px-4 py-3">
            <Link to="/">
              <Logo size="sm" />
            </Link>
            <span className="text-[11px] text-cream-soft/60">جدة، السعودية</span>
          </div>
        </header>
      )}
      <main className="flex-1 max-w-md w-full mx-auto px-4 pb-24 pt-4">{children}</main>
      <BottomNav />
    </div>
  )
}
