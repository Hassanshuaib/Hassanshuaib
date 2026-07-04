import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMenu } from '../context/MenuContext'
import { useCart } from '../context/CartContext'
import { AddonToggle, PrimaryButton, QuantityStepper, SectionTitle } from '../components/UI'

export default function KumpirBuilder() {
  const { menuItems, addons } = useMenu()
  const { addLine } = useCart()
  const navigate = useNavigate()

  const baseItem = menuItems.find((m) => m.id === 'kumpir')
  const freeAddons = addons.filter((a) => a.applies_to === 'kumpir' && a.kind === 'free')
  const paidAddons = addons.filter((a) => a.applies_to === 'kumpir' && a.kind === 'paid')

  const [selectedFree, setSelectedFree] = useState([])
  const [selectedPaid, setSelectedPaid] = useState([])
  const [keepSkin, setKeepSkin] = useState(false)
  const [qty, setQty] = useState(1)
  const [justAdded, setJustAdded] = useState(false)

  function toggleFree(id) {
    setSelectedFree((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]))
  }
  function togglePaid(id) {
    setSelectedPaid((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]))
  }

  const paidTotal = useMemo(
    () => selectedPaid.reduce((sum, id) => sum + Number(paidAddons.find((a) => a.id === id)?.price ?? 0), 0),
    [selectedPaid, paidAddons]
  )

  const basePrice = Number(baseItem?.price ?? 22)
  const unitPrice = basePrice + paidTotal
  const total = unitPrice * qty

  if (!baseItem) return null

  function handleAdd() {
    addLine({
      menuItemId: 'kumpir',
      name: 'الكومبير',
      quantity: qty,
      unitPrice,
      lineTotal: total,
      details: {
        free_addons: selectedFree.map((id) => freeAddons.find((a) => a.id === id)?.name),
        paid_addons: selectedPaid.map((id) => {
          const a = paidAddons.find((x) => x.id === id)
          return { name: a.name, price: Number(a.price) }
        }),
        keep_skin: keepSkin,
      },
    })
    setJustAdded(true)
    setTimeout(() => navigate('/cart'), 450)
  }

  return (
    <div className="pop-in pb-4">
      <h1 className="font-display font-extrabold text-2xl text-cream mb-1">ركّب كومبيرك 🥔</h1>
      <p className="text-cream-soft/60 text-sm mb-5">اختر إضافاتك المفضلة، والسعر يتحدث لحظياً</p>

      <div className="mb-5">
        <button
          onClick={() => setKeepSkin((v) => !v)}
          className={`w-full flex items-center justify-between rounded-xl px-4 py-3 border-2 font-semibold text-sm transition ${
            keepSkin ? 'bg-orange/15 border-orange text-orange' : 'bg-navy-800 border-navy-700 text-cream-soft/85'
          }`}
        >
          <span>أبيها بقشرتها</span>
          <span className={`w-10 h-6 rounded-full relative transition shrink-0 ${keepSkin ? 'bg-orange' : 'bg-navy-700'}`}>
            <span
              className="absolute top-0.5 w-5 h-5 rounded-full bg-navy-900 transition-all"
              style={{ right: keepSkin ? '2px' : '18px' }}
            />
          </span>
        </button>
      </div>

      <SectionTitle>إضافات مجانية</SectionTitle>
      <div className="grid grid-cols-2 gap-2 mb-5">
        {freeAddons.map((a) => (
          <AddonToggle
            key={a.id}
            label={a.name}
            price={0}
            selected={selectedFree.includes(a.id)}
            onToggle={() => toggleFree(a.id)}
          />
        ))}
      </div>

      <SectionTitle>إضافات مدفوعة</SectionTitle>
      <div className="grid grid-cols-2 gap-2 mb-6">
        {paidAddons.map((a) => (
          <AddonToggle
            key={a.id}
            label={a.name}
            price={Number(a.price)}
            selected={selectedPaid.includes(a.id)}
            onToggle={() => togglePaid(a.id)}
          />
        ))}
      </div>

      <div className="flex items-center justify-between mb-4">
        <span className="text-sm font-semibold text-cream-soft/80">الكمية</span>
        <QuantityStepper value={qty} onChange={setQty} min={1} />
      </div>

      <div className="sticky bottom-20 bg-navy-800 border border-navy-700 rounded-2xl p-4 flex items-center justify-between gap-4 shadow-xl">
        <div>
          <p className="text-xs text-cream-soft/60">الإجمالي</p>
          <p className="font-display font-extrabold text-2xl text-orange">{total} ر.س</p>
        </div>
        <PrimaryButton className="w-auto px-8" onClick={handleAdd}>
          {justAdded ? 'أُضيف ✓' : 'أضف إلى السلة'}
        </PrimaryButton>
      </div>
    </div>
  )
}
