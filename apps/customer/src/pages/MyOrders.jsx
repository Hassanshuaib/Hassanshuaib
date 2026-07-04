import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { supabase, ensureAnonymousSession } from '../lib/supabase'
import { Card, PrimaryButton, StatusBadge } from '../components/UI'

export default function MyOrders() {
  const [orders, setOrders] = useState(null)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    let channel
    let cancelled = false

    async function load() {
      try {
        const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 8000))
        await Promise.race([ensureAnonymousSession(), timeout])
        const { data, error } = await supabase.from('orders').select('*').order('created_at', { ascending: false })
        if (cancelled) return
        if (error) throw error
        setOrders(data ?? [])

        channel = supabase
          .channel('my-orders')
          .on('postgres_changes', { event: '*', schema: 'public', table: 'orders' }, (payload) => {
            setOrders((prev) => {
              if (!prev) return prev
              if (payload.eventType === 'INSERT') return [payload.new, ...prev]
              if (payload.eventType === 'UPDATE') return prev.map((o) => (o.id === payload.new.id ? payload.new : o))
              return prev
            })
          })
          .subscribe()
      } catch {
        if (!cancelled) setFailed(true)
      }
    }

    load()
    return () => {
      cancelled = true
      if (channel) supabase.removeChannel(channel)
    }
  }, [])

  if (failed) {
    return (
      <div className="pop-in text-center py-16">
        <p className="text-5xl mb-4">📡</p>
        <p className="text-cream-soft/70">تعذر جلب طلباتك، تحقق من الاتصال بالإنترنت</p>
      </div>
    )
  }

  if (orders === null) return <p className="text-center text-cream-soft/60 py-10">جاري التحميل...</p>

  if (orders.length === 0) {
    return (
      <div className="pop-in text-center py-16">
        <p className="text-5xl mb-4">🧾</p>
        <p className="text-cream-soft/70 mb-6">ما عندك طلبات بعد</p>
        <Link to="/">
          <PrimaryButton>اطلب الآن</PrimaryButton>
        </Link>
      </div>
    )
  }

  return (
    <div className="pop-in pb-4">
      <h1 className="font-display font-extrabold text-2xl text-cream mb-5">طلباتي</h1>
      <div className="space-y-3">
        {orders.map((order) => (
          <Link key={order.id} to={`/orders/${order.id}`}>
            <Card className="flex items-center justify-between">
              <div>
                <p className="font-bold text-cream">طلب #{order.order_number}</p>
                <p className="text-xs text-cream-soft/60 mt-1">{order.total} ر.س</p>
              </div>
              <StatusBadge status={order.status} />
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}
