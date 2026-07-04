import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMenu } from '../context/MenuContext'
import { useCart } from '../context/CartContext'
import { AddonToggle, PrimaryButton, QuantityStepper, RadioOption, SectionTitle } from '../components/UI'

export default function CornBuilder() {
  const { menuItems, addons, cornFlavors } = useMenu()
  const { addLine } = useCart()
  const navigate = useNavigate()

  const baseItem = menuItems.find((m) => m.id === 'corn_cup')
  const extraCheetos = addons.find((a) => a.id === 'extra_cheetos')

  const [flavor, setFlavor] = useState(cornFlavors[0]?.id)

  useEffect(() => {
    if (!flavor && cornFlavors.length > 0) setFlavor(cornFlavors[0].id)
  }, [cornFlavors, flavor])
  const [addCheetos, setAddCheetos] = useState(false)
  const [qty, setQty] = useState(1)
  const [justAdded, setJustAdded] = useState(false)

  const basePrice = Number(baseItem?.price ?? 9)
  const cheetosPrice = Number(extraCheetos?.price ?? 2)
  const unitPrice = basePrice + (addCheetos ? cheetosPrice : 0)
  const total = unitPrice * qty

  if (!baseItem) return null

  function handleAdd() {
    const flavorName = cornFlavors.find((f) => f.id === flavor)?.name
    addLine({
      menuItemId: 'corn_cup',
      name: 'كاسة ذرة',
      quantity: qty,
      unitPrice,
      lineTotal: total,
      details: {
        flavor: flavorName,
        extra_cheetos: addCheetos,
      },
    })
    setJustAdded(true)
    setTimeout(() => navigate('/cart'), 450)
  }

  return (
    <div className="pop-in pb-4">
      <h1 className="font-display font-extrabold text-2xl text-cream mb-1">كاسة ذرة 🌽</h1>
      <p className="text-cream-soft/60 text-sm mb-5">اختر نكهتك المفضلة</p>

      <SectionTitle>النكهة</SectionTitle>
      <div className="space-y-2 mb-6">
        {cornFlavors.map((f) => (
          <RadioOption key={f.id} label={f.name} selected={flavor === f.id} onSelect={() => setFlavor(f.id)} />
        ))}
      </div>

      <SectionTitle>إضافات</SectionTitle>
      <div className="mb-6">
        <AddonToggle
          label={extraCheetos?.name ?? 'زد شيتوس'}
          price={cheetosPrice}
          selected={addCheetos}
          onToggle={() => setAddCheetos((v) => !v)}
        />
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
