import { useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'
import { getSavedCustomer, saveCustomer } from '../lib/customerStorage'
import { Card } from '../components/UI'
import { SteamPotato } from '../components/Logo'

const TOTAL_STAMPS = 8

export default function StampCard() {
  const saved = getSavedCustomer()
  const [phone, setPhone] = useState(saved.phone)
  const [card, setCard] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function fetchCard(p) {
    if (!/^05\d{8}$/.test(p)) {
      setError('أدخل رقم جوال صحيح (مثال: 0512345678)')
      return
    }
    setError('')
    setLoading(true)
    const { data, error: rpcError } = await supabase.rpc('get_stamp_card', { p_phone: p })
    setLoading(false)
    if (rpcError) {
      setError('تعذر جلب البيانات، حاول مرة أخرى')
      return
    }
    if (!data || data.length === 0) {
      setCard({ stamps: 0, rewards: 0, name: '' })
    } else {
      setCard(data[0])
    }
    saveCustomer({ name: saved.name, phone: p })
  }

  useEffect(() => {
    if (saved.phone) fetchCard(saved.phone)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const stamps = card?.stamps ?? 0
  const rewards = card?.rewards ?? 0

  return (
    <div className="pop-in pb-4">
      <h1 className="font-display font-extrabold text-2xl text-cream mb-1">أختامي ⭐</h1>
      <p className="text-cream-soft/60 text-sm mb-5">كل طلب مؤكد = ختم. 8 أختام = كومبير مجاني!</p>

      <div className="flex gap-2 mb-2">
        <input
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          placeholder="05xxxxxxxx"
          inputMode="numeric"
          dir="ltr"
          className="flex-1 rounded-xl bg-navy-800 border-2 border-navy-700 px-4 py-3 text-cream-soft placeholder:text-cream-soft/40 text-left focus:border-orange outline-none"
        />
        <button
          onClick={() => fetchCard(phone.trim())}
          className="rounded-xl bg-orange text-navy-900 font-bold px-5 active:scale-95 transition"
        >
          بحث
        </button>
      </div>
      {error && <p className="text-xs text-red-400 mb-4">{error}</p>}
      {loading && <p className="text-xs text-cream-soft/50 mb-4">جاري البحث...</p>}

      {card && (
        <Card className="mt-4">
          {rewards > 0 && (
            <div className="mb-4 bg-orange/15 border border-orange rounded-xl px-4 py-3 text-center">
              <p className="font-bold text-orange">🎉 لديك {rewards} كومبير مجاني بانتظارك!</p>
              <p className="text-xs text-cream-soft/60 mt-1">أخبر الموظف برقم جوالك عند الاستلام</p>
            </div>
          )}
          <div className="grid grid-cols-4 gap-3">
            {Array.from({ length: TOTAL_STAMPS }).map((_, i) => {
              const filled = i < stamps
              return (
                <div
                  key={i}
                  className={`aspect-square rounded-full border-2 border-dashed flex items-center justify-center ${
                    filled ? 'border-orange bg-orange/10 stamp-pop' : 'border-navy-700'
                  }`}
                  style={filled ? { animationDelay: `${i * 60}ms` } : undefined}
                >
                  {filled ? <SteamPotato className="w-7 h-7" /> : <span className="text-cream-soft/20 text-lg">{i + 1}</span>}
                </div>
              )
            })}
          </div>
          <p className="text-center text-xs text-cream-soft/60 mt-4">
            {stamps}/{TOTAL_STAMPS} أختام
          </p>
        </Card>
      )}
    </div>
  )
}
