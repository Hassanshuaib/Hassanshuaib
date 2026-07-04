import { Link, useNavigate } from 'react-router-dom'
import { useCart } from '../context/CartContext'
import { Card, PrimaryButton, QuantityStepper, SecondaryButton } from '../components/UI'

function describeLine(line) {
  const parts = []
  if (line.details?.keep_skin) parts.push('بقشرتها')
  if (line.details?.free_addons?.length) parts.push(line.details.free_addons.join('، '))
  if (line.details?.paid_addons?.length) parts.push(line.details.paid_addons.map((a) => a.name).join('، '))
  if (line.details?.flavor) parts.push(`نكهة: ${line.details.flavor}`)
  if (line.details?.extra_cheetos) parts.push('زد شيتوس')
  return parts.join(' • ')
}

export default function Cart() {
  const { lines, removeLine, updateQuantity, total } = useCart()
  const navigate = useNavigate()

  if (lines.length === 0) {
    return (
      <div className="pop-in text-center py-16">
        <p className="text-5xl mb-4">🛒</p>
        <p className="text-cream-soft/70 mb-6">سلتك فاضية للحين</p>
        <Link to="/">
          <PrimaryButton>تصفح المنيو</PrimaryButton>
        </Link>
      </div>
    )
  }

  return (
    <div className="pop-in pb-4">
      <h1 className="font-display font-extrabold text-2xl text-cream mb-4">سلتك</h1>

      <div className="space-y-3 mb-6">
        {lines.map((line) => (
          <Card key={line.lineId} className="flex flex-col gap-2">
            <div className="flex items-start justify-between gap-2">
              <div>
                <h3 className="font-bold text-cream">{line.name}</h3>
                {describeLine(line) && <p className="text-xs text-cream-soft/60 mt-1">{describeLine(line)}</p>}
              </div>
              <button onClick={() => removeLine(line.lineId)} className="text-cream-soft/40 text-lg leading-none">
                ✕
              </button>
            </div>
            <div className="flex items-center justify-between mt-1">
              <QuantityStepper value={line.quantity} onChange={(q) => updateQuantity(line.lineId, q)} min={1} />
              <span className="font-bold text-orange">{line.lineTotal} ر.س</span>
            </div>
          </Card>
        ))}
      </div>

      <Card className="flex items-center justify-between mb-4">
        <span className="font-semibold text-cream-soft/80">الإجمالي</span>
        <span className="font-display font-extrabold text-2xl text-orange">{total} ر.س</span>
      </Card>

      <PrimaryButton onClick={() => navigate('/checkout')}>متابعة الطلب</PrimaryButton>
      <div className="mt-3">
        <Link to="/">
          <SecondaryButton>إضافة المزيد</SecondaryButton>
        </Link>
      </div>
    </div>
  )
}
