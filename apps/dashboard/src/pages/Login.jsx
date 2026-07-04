import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Logo from '../components/Logo'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    const err = await login(email.trim(), password)
    setSubmitting(false)
    if (err) {
      setError('بيانات الدخول غير صحيحة')
      return
    }
    navigate('/', { replace: true })
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-navy-900 px-4">
      <form onSubmit={handleSubmit} className="w-full max-w-sm bg-navy-800 border border-navy-700 rounded-2xl p-6 pop-in">
        <div className="flex justify-center mb-6">
          <Logo />
        </div>
        <h1 className="text-center font-bold text-lg text-cream mb-6">تسجيل دخول الموظفين</h1>

        <div className="space-y-3">
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="البريد الإلكتروني"
            dir="ltr"
            className="w-full rounded-xl bg-navy-900 border-2 border-navy-700 px-4 py-3 text-cream-soft placeholder:text-cream-soft/40 text-left focus:border-orange outline-none"
          />
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="كلمة المرور"
            dir="ltr"
            className="w-full rounded-xl bg-navy-900 border-2 border-navy-700 px-4 py-3 text-cream-soft placeholder:text-cream-soft/40 text-left focus:border-orange outline-none"
          />
        </div>

        {error && <p className="text-sm text-red-400 mt-3 text-center">{error}</p>}

        <button
          type="submit"
          disabled={submitting}
          className="w-full mt-5 rounded-xl bg-orange text-navy-900 font-bold py-3 active:scale-[0.98] transition disabled:opacity-50"
        >
          {submitting ? 'جاري الدخول...' : 'دخول'}
        </button>
      </form>
    </div>
  )
}
