export function PrimaryButton({ children, className = '', ...props }) {
  return (
    <button
      className={`w-full rounded-2xl bg-orange text-navy-900 font-bold py-3.5 text-base shadow-lg shadow-orange/20 active:scale-[0.98] transition disabled:opacity-40 disabled:active:scale-100 ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}

export function SecondaryButton({ children, className = '', ...props }) {
  return (
    <button
      className={`w-full rounded-2xl border-2 border-navy-700 text-cream-soft font-semibold py-3 text-sm active:scale-[0.98] transition ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}

export function AddonToggle({ label, price, selected, onToggle }) {
  return (
    <button
      type="button"
      onClick={onToggle}
      className={`flex items-center justify-between gap-2 rounded-xl px-3.5 py-3 border-2 text-sm font-semibold transition text-right ${
        selected
          ? 'bg-orange/15 border-orange text-orange'
          : 'bg-navy-800 border-navy-700 text-cream-soft/85'
      }`}
    >
      <span className="flex items-center gap-2">
        <span
          className={`w-4 h-4 rounded-full border-2 flex items-center justify-center shrink-0 ${
            selected ? 'border-orange bg-orange' : 'border-cream-soft/40'
          }`}
        >
          {selected && <span className="w-1.5 h-1.5 rounded-full bg-navy-900" />}
        </span>
        {label}
      </span>
      {price > 0 && <span className="text-xs opacity-80 shrink-0">+{price} ر.س</span>}
    </button>
  )
}

export function RadioOption({ label, selected, onSelect, sub }) {
  return (
    <button
      type="button"
      onClick={onSelect}
      className={`w-full flex items-center justify-between gap-2 rounded-xl px-4 py-3 border-2 text-sm font-semibold transition text-right ${
        selected
          ? 'bg-orange/15 border-orange text-orange'
          : 'bg-navy-800 border-navy-700 text-cream-soft/85'
      }`}
    >
      <span>{label}</span>
      {sub && <span className="text-xs opacity-70">{sub}</span>}
    </button>
  )
}

export function QuantityStepper({ value, onChange, min = 0 }) {
  return (
    <div className="flex items-center gap-3 bg-navy-800 border-2 border-navy-700 rounded-full px-2 py-1">
      <button
        type="button"
        onClick={() => onChange(Math.max(min, value - 1))}
        className="w-7 h-7 rounded-full bg-navy-700 text-cream-soft font-bold flex items-center justify-center active:scale-90 transition"
      >
        −
      </button>
      <span className="w-5 text-center font-bold">{value}</span>
      <button
        type="button"
        onClick={() => onChange(value + 1)}
        className="w-7 h-7 rounded-full bg-orange text-navy-900 font-bold flex items-center justify-center active:scale-90 transition"
      >
        +
      </button>
    </div>
  )
}

export function SectionTitle({ children, className = '' }) {
  return <h2 className={`font-display font-bold text-lg text-cream mb-2 ${className}`}>{children}</h2>
}

export function Card({ children, className = '' }) {
  return <div className={`bg-navy-800 border border-navy-700 rounded-2xl p-4 ${className}`}>{children}</div>
}

export function StatusBadge({ status }) {
  const map = {
    new: { label: 'جديد', className: 'bg-blue-500/20 text-blue-300' },
    preparing: { label: 'قيد التحضير', className: 'bg-orange/20 text-orange' },
    ready: { label: 'جاهز للاستلام', className: 'bg-green-500/20 text-green-300' },
    picked_up: { label: 'تم الاستلام', className: 'bg-cream-soft/10 text-cream-soft/60' },
  }
  const s = map[status] ?? map.new
  return <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${s.className}`}>{s.label}</span>
}
