import { Link } from 'react-router-dom'
import { useMenu } from '../context/MenuContext'
import { useCart } from '../context/CartContext'
import { Card, QuantityStepper, SectionTitle } from '../components/UI'
import { SteamPotato } from '../components/Logo'
import { useState } from 'react'

const CATEGORY_LABELS = {
  kumpir: 'الكومبير',
  corn: 'كاسة الذرة',
  drink: 'المشروبات',
}

export default function Home() {
  const { loading, menuItems } = useMenu()

  const grouped = menuItems.reduce((acc, item) => {
    acc[item.category] = acc[item.category] || []
    acc[item.category].push(item)
    return acc
  }, {})

  return (
    <div className="pop-in">
      <section className="text-center py-6">
        <div className="flex justify-center mb-2">
          <SteamPotato className="w-16 h-16" />
        </div>
        <h1 className="brand-tilt font-display font-extrabold text-4xl text-cream">كومبير</h1>
        <p className="text-cream-soft/70 text-sm mt-3">بطاطس مشوية تركية، طازجة من فرعك في جدة</p>
      </section>

      {loading && <p className="text-center text-cream-soft/60 py-10">جاري تحميل المنيو...</p>}

      {!loading && (
        <div className="space-y-6">
          {Object.entries(grouped).map(([category, items]) => (
            <div key={category}>
              <SectionTitle>{CATEGORY_LABELS[category] ?? category}</SectionTitle>
              <div className="space-y-3">
                {items.map((item) =>
                  category === 'drink' ? (
                    <DrinkCard key={item.id} item={item} />
                  ) : (
                    <MenuLinkCard key={item.id} item={item} />
                  )
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function MenuLinkCard({ item }) {
  const to = item.category === 'kumpir' ? '/kumpir' : '/corn'
  return (
    <Link to={to}>
      <Card className="flex items-center justify-between gap-3 active:scale-[0.98] transition">
        <div>
          <h3 className="font-bold text-cream">{item.name}</h3>
          {item.description && <p className="text-xs text-cream-soft/60 mt-1">{item.description}</p>}
          <p className="text-orange font-bold mt-2">{item.price} ر.س</p>
        </div>
        <span className="text-2xl">{item.category === 'kumpir' ? '🥔' : '🌽'}</span>
      </Card>
    </Link>
  )
}

function DrinkCard({ item }) {
  const [qty, setQty] = useState(1)
  const { addLine } = useCart()

  return (
    <Card className="flex items-center justify-between gap-3">
      <div>
        <h3 className="font-bold text-cream">{item.name}</h3>
        <p className="text-orange font-bold mt-2">{item.price} ر.س</p>
      </div>
      <div className="flex flex-col items-end gap-2">
        <QuantityStepper value={qty} onChange={setQty} min={1} />
        <button
          className="text-xs font-bold text-navy-900 bg-cream px-3 py-1.5 rounded-full active:scale-95 transition"
          onClick={() =>
            addLine({
              menuItemId: item.id,
              name: item.name,
              quantity: qty,
              unitPrice: item.price,
              lineTotal: item.price * qty,
              details: {},
            })
          }
        >
          أضف
        </button>
      </div>
    </Card>
  )
}
