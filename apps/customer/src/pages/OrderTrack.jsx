import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { supabase } from '../lib/supabase'
import { useMenu } from '../context/MenuContext'
import { PICKUP_TIMES } from '../lib/fallbackMenu'
import { Card, PrimaryButton } from '../components/UI'

const STEPS = [
  { key: 'new', label: 'جديد', icon: '🧾' },
  { key: 'preparing', label: 'قيد التحضير', icon: '🍳' },
  { key: 'ready', label: 'جاهز للاستلام', icon: '🥔' },
  { key: 'picked_up', label: 'تم الاستلام', icon: '✅' },
]

function describeItem(item) {
  const parts = []
  if (item.details?.keep_skin) parts.push('بقشرتها')
  if (item.details?.free_addons?.length) parts.push(item.details.free_addons.join('، '))
  if (item.details?.paid_addons?.length) parts.push(item.details.paid_addons.map((a) => a.name).join('، '))
  if (item.details?.flavor) parts.push(`نكهة: ${item.details.flavor}`)
  if (item.details?.extra_cheetos) parts.push('زد شيتوس')
  return parts.join(' • ')
}

export default function OrderTrack() {
  const { id } = useParams()
  const { branches } = useMenu()
  const [order, setOrder] = useState(null)
  const [notFound, setNotFound] = useState(false)

  useEffect(() => {
    let channel

    async function load() {
      const { data, error } = await supabase.from('orders').select('*').eq('id', id).single()
      if (error || !data) {
        setNotFound(true)
        return
      }
      setOrder(data)

      channel = supabase
        .channel(`order-${id}`)
        .on(
          'postgres_changes',
          { event: 'UPDATE', schema: 'public', table: 'orders', filter: `id=eq.${id}` },
          (payload) => setOrder(payload.new)
        )
        .subscribe()
    }

    load()
    return () => {
      if (channel) supabase.removeChannel(channel)
    }
  }, [id])

  if (notFound) {
    return (
      <div className="pop-in text-center py-16">
        <p className="text-cream-soft/70 mb-6">لم يتم العثور على الطلب</p>
        <Link to="/">
          <PrimaryButton>الرجوع للمنيو</PrimaryButton>
        </Link>
      </div>
    )
  }

  if (!order) return <p className="text-center text-cream-soft/60 py-10">جاري التحميل...</p>

  const currentStepIndex = STEPS.findIndex((s) => s.key === order.status)

  return (
    <div className="pop-in pb-4">
      <div className="text-center mb-6">
        <p className="text-cream-soft/60 text-sm">طلب رقم</p>
        <p className="font-display font-extrabold text-3xl text-orange">#{order.order_number}</p>
      </div>

      <Card className="mb-6">
        <div className="flex items-center justify-between">
          {STEPS.map((step, i) => (
            <div key={step.key} className="flex-1 flex flex-col items-center relative">
              {i > 0 && (
                <span
                  className={`absolute top-4 right-1/2 w-full h-0.5 ${
                    i <= currentStepIndex ? 'bg-orange' : 'bg-navy-700'
                  }`}
                />
              )}
              <span
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm z-10 ${
                  i <= currentStepIndex ? 'bg-orange text-navy-900' : 'bg-navy-700 text-cream-soft/50'
                }`}
              >
                {step.icon}
              </span>
              <span className={`text-[10px] mt-1.5 text-center ${i <= currentStepIndex ? 'text-orange' : 'text-cream-soft/40'}`}>
                {step.label}
              </span>
            </div>
          ))}
        </div>
      </Card>

      <Card className="mb-4 space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-cream-soft/60">الفرع</span>
          <span className="font-semibold">{branches.find((b) => b.id === order.branch)?.name ?? order.branch}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-cream-soft/60">وقت الاستلام</span>
          <span className="font-semibold">
            {PICKUP_TIMES.find((t) => t.id === order.pickup_time)?.name ?? order.pickup_time}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-cream-soft/60">الاسم</span>
          <span className="font-semibold">{order.customer_name}</span>
        </div>
      </Card>

      <Card className="space-y-3 mb-6">
        {order.items.map((item, i) => (
          <div key={i} className="flex justify-between items-start text-sm border-b border-navy-700 last:border-0 pb-3 last:pb-0">
            <div>
              <p className="font-bold text-cream">
                {item.quantity} × {item.name}
              </p>
              {describeItem(item) && <p className="text-xs text-cream-soft/60 mt-1">{describeItem(item)}</p>}
            </div>
            <span className="font-semibold text-orange">{item.lineTotal} ر.س</span>
          </div>
        ))}
        <div className="flex justify-between pt-1 font-bold">
          <span>الإجمالي</span>
          <span className="text-orange">{order.total} ر.س</span>
        </div>
      </Card>

      <Link to="/orders">
        <PrimaryButton>كل طلباتي</PrimaryButton>
      </Link>
    </div>
  )
}
