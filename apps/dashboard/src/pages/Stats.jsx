import { useEffect, useMemo, useState } from 'react'
import { supabase } from '../lib/supabase'

function startOfToday() {
  const d = new Date()
  d.setHours(0, 0, 0, 0)
  return d.toISOString()
}

function tallyAddons(orders) {
  const counts = {}
  for (const order of orders) {
    for (const item of order.items ?? []) {
      const names = [
        ...(item.details?.free_addons ?? []).filter(Boolean),
        ...(item.details?.paid_addons ?? []).map((a) => a.name),
      ]
      for (const name of names) {
        counts[name] = (counts[name] ?? 0) + (item.quantity ?? 1)
      }
    }
  }
  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
}

export default function Stats() {
  const [orders, setOrders] = useState(null)
  const [loadError, setLoadError] = useState(false)

  useEffect(() => {
    let cancelled = false
    const timeout = setTimeout(() => {
      if (!cancelled) setLoadError(true)
    }, 10000)

    supabase
      .from('orders')
      .select('*')
      .gte('created_at', startOfToday())
      .then(({ data, error }) => {
        clearTimeout(timeout)
        if (cancelled) return
        if (error) setLoadError(true)
        else setOrders(data ?? [])
      })

    return () => {
      cancelled = true
      clearTimeout(timeout)
    }
  }, [])

  const totalSales = useMemo(() => orders?.reduce((sum, o) => sum + Number(o.total), 0) ?? 0, [orders])
  const orderCount = orders?.length ?? 0
  const topAddons = useMemo(() => (orders ? tallyAddons(orders) : []), [orders])
  const maxCount = topAddons[0]?.[1] ?? 1

  if (loadError) {
    return <p className="text-center text-cream-soft/60 py-16">تعذر جلب الإحصائيات، تحقق من الاتصال وأعد تحميل الصفحة</p>
  }

  if (orders === null) return <p className="text-center text-cream-soft/60 py-16">جاري التحميل...</p>

  return (
    <div className="pop-in space-y-6">
      <h1 className="font-display font-extrabold text-xl text-cream">إحصائيات اليوم</h1>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-navy-800 border border-navy-700 rounded-2xl p-5 text-center">
          <p className="text-cream-soft/60 text-sm mb-2">مبيعات اليوم</p>
          <p className="font-display font-extrabold text-3xl text-orange">{totalSales.toFixed(0)} ر.س</p>
        </div>
        <div className="bg-navy-800 border border-navy-700 rounded-2xl p-5 text-center">
          <p className="text-cream-soft/60 text-sm mb-2">عدد الطلبات</p>
          <p className="font-display font-extrabold text-3xl text-orange">{orderCount}</p>
        </div>
      </div>

      <div className="bg-navy-800 border border-navy-700 rounded-2xl p-5">
        <p className="font-bold text-cream mb-4">أكثر الإضافات طلباً</p>
        {topAddons.length === 0 && <p className="text-sm text-cream-soft/50">لا توجد بيانات كافية بعد</p>}
        <div className="space-y-3">
          {topAddons.map(([name, count]) => (
            <div key={name}>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-cream-soft/85">{name}</span>
                <span className="text-cream-soft/50">{count}</span>
              </div>
              <div className="h-2 bg-navy-900 rounded-full overflow-hidden">
                <div className="h-full bg-orange rounded-full" style={{ width: `${(count / maxCount) * 100}%` }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
