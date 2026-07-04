import { useEffect, useMemo, useRef, useState } from 'react'
import { supabase } from '../lib/supabase'
import { STATUS_COLUMNS } from '../lib/constants'
import { playNewOrderBeep } from '../lib/sound'
import OrderCard from '../components/OrderCard'

function startOfToday() {
  const d = new Date()
  d.setHours(0, 0, 0, 0)
  return d.toISOString()
}

export default function LiveOrders() {
  const [orders, setOrders] = useState([])
  const [branches, setBranches] = useState([])
  const [branchFilter, setBranchFilter] = useState('all')
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [flashIds, setFlashIds] = useState(new Set())
  const soundEnabled = useRef(false)

  useEffect(() => {
    let channel
    let cancelled = false

    async function load() {
      try {
        const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 10000))
        const [branchRes, orderRes] = await Promise.race([
          Promise.all([
            supabase.from('branches').select('*').order('sort_order'),
            supabase.from('orders').select('*').gte('created_at', startOfToday()).order('created_at', { ascending: true }),
          ]),
          timeout,
        ])
        if (cancelled) return
        if (branchRes.error || orderRes.error) throw branchRes.error || orderRes.error
        setBranches(branchRes.data ?? [])
        setOrders(orderRes.data ?? [])
        setLoading(false)
      } catch {
        if (!cancelled) {
          setLoadError(true)
          setLoading(false)
        }
        return
      }

      channel = supabase
        .channel('dashboard-orders')
        .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'orders' }, (payload) => {
          setOrders((prev) => [...prev, payload.new])
          if (soundEnabled.current) playNewOrderBeep()
          setFlashIds((prev) => new Set(prev).add(payload.new.id))
          setTimeout(() => {
            setFlashIds((prev) => {
              const next = new Set(prev)
              next.delete(payload.new.id)
              return next
            })
          }, 2500)
        })
        .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'orders' }, (payload) => {
          setOrders((prev) => prev.map((o) => (o.id === payload.new.id ? payload.new : o)))
        })
        .subscribe()
    }

    load()
    return () => {
      if (channel) supabase.removeChannel(channel)
    }
  }, [])

  useEffect(() => {
    function enableSound() {
      soundEnabled.current = true
      window.removeEventListener('click', enableSound)
    }
    window.addEventListener('click', enableSound)
    return () => window.removeEventListener('click', enableSound)
  }, [])

  const branchName = (id) => branches.find((b) => b.id === id)?.name ?? id

  const filteredOrders = useMemo(
    () => (branchFilter === 'all' ? orders : orders.filter((o) => o.branch === branchFilter)),
    [orders, branchFilter]
  )

  async function advanceStatus(order, nextStatus) {
    setOrders((prev) => prev.map((o) => (o.id === order.id ? { ...o, status: nextStatus } : o)))
    const { error } = await supabase.from('orders').update({ status: nextStatus }).eq('id', order.id)
    if (error) {
      setOrders((prev) => prev.map((o) => (o.id === order.id ? { ...o, status: order.status } : o)))
    }
  }

  if (loadError) {
    return <p className="text-center text-cream-soft/60 py-16">تعذر جلب الطلبات، تحقق من الاتصال وأعد تحميل الصفحة</p>
  }

  return (
    <div className="pop-in">
      <div className="flex items-center justify-between mb-5 flex-wrap gap-3">
        <h1 className="font-display font-extrabold text-xl text-cream">طلبات اليوم</h1>
        <select
          value={branchFilter}
          onChange={(e) => setBranchFilter(e.target.value)}
          className="bg-navy-800 border-2 border-navy-700 rounded-lg px-3 py-2 text-sm font-semibold text-cream-soft outline-none focus:border-orange"
        >
          <option value="all">كل الفروع</option>
          {branches.map((b) => (
            <option key={b.id} value={b.id}>
              {b.name}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <p className="text-center text-cream-soft/60 py-16">جاري تحميل الطلبات...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {STATUS_COLUMNS.map((col) => {
            const columnOrders = filteredOrders
              .filter((o) => o.status === col.key)
              .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            return (
              <div key={col.key} className="bg-navy-900 border border-navy-700 rounded-2xl p-3 min-h-[200px]">
                <div className={`flex items-center justify-between mb-3 px-2 py-1.5 rounded-lg border ${col.color}`}>
                  <span className="font-bold text-sm">{col.label}</span>
                  <span className="text-xs font-bold">{columnOrders.length}</span>
                </div>
                <div className="space-y-3 max-h-[70vh] overflow-y-auto pr-1">
                  {columnOrders.length === 0 && <p className="text-center text-xs text-cream-soft/30 py-6">لا يوجد</p>}
                  {columnOrders.map((order) => (
                    <OrderCard
                      key={order.id}
                      order={order}
                      branchName={branchName(order.branch)}
                      onAdvanceStatus={advanceStatus}
                      highlight={flashIds.has(order.id)}
                    />
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
