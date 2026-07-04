import { NEXT_STATUS, NEXT_STATUS_LABEL, PICKUP_TIME_LABELS } from '../lib/constants'

function describeItem(item) {
  const parts = []
  if (item.details?.keep_skin) parts.push('بقشرتها')
  if (item.details?.free_addons?.length) parts.push(item.details.free_addons.filter(Boolean).join('، '))
  if (item.details?.paid_addons?.length) parts.push(item.details.paid_addons.map((a) => a.name).join('، '))
  if (item.details?.flavor) parts.push(`نكهة: ${item.details.flavor}`)
  if (item.details?.extra_cheetos) parts.push('زد شيتوس')
  return parts.join(' • ')
}

export default function OrderCard({ order, branchName, onAdvanceStatus, highlight }) {
  const nextStatus = NEXT_STATUS[order.status]
  const nextLabel = NEXT_STATUS_LABEL[order.status]

  return (
    <div className={`bg-navy-800 border border-navy-700 rounded-xl p-3.5 flex flex-col gap-2.5 ${highlight ? 'card-flash' : ''}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="font-bold text-cream">طلب #{order.order_number}</p>
          <p className="text-xs text-cream-soft/50 mt-0.5">
            {new Date(order.created_at).toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' })}
          </p>
        </div>
        <span className="text-xs font-bold bg-navy-700 text-cream-soft/70 px-2 py-1 rounded-full">{branchName}</span>
      </div>

      <div className="space-y-1.5 border-t border-b border-navy-700 py-2">
        {order.items.map((item, i) => (
          <div key={i} className="text-sm">
            <p className="font-semibold text-cream-soft">
              {item.quantity} × {item.name}
            </p>
            {describeItem(item) && <p className="text-xs text-cream-soft/50">{describeItem(item)}</p>}
          </div>
        ))}
      </div>

      <div className="flex items-center justify-between text-sm">
        <span className="text-cream-soft/60">{order.customer_name}</span>
        <span dir="ltr" className="text-cream-soft/60">{order.customer_phone}</span>
      </div>

      <div className="flex items-center justify-between text-sm">
        <span className="text-cream-soft/60">الاستلام: {PICKUP_TIME_LABELS[order.pickup_time] ?? order.pickup_time}</span>
        <span className="font-bold text-orange">{order.total} ر.س</span>
      </div>

      {nextStatus && (
        <button
          onClick={() => onAdvanceStatus(order, nextStatus)}
          className="mt-1 w-full rounded-lg bg-orange text-navy-900 font-bold py-2 text-sm active:scale-[0.98] transition"
        >
          {nextLabel}
        </button>
      )}
    </div>
  )
}
