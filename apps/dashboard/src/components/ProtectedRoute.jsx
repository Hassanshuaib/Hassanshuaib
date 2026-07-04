import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function ProtectedRoute({ children }) {
  const { session, loading } = useAuth()

  if (loading) {
    return <p className="text-center text-cream-soft/60 py-20">جاري التحقق من الدخول...</p>
  }

  if (!session) {
    return <Navigate to="/login" replace />
  }

  return children
}
