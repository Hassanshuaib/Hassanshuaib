import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCart } from '../context/CartContext'
import { useMenu } from '../context/MenuContext'
import { supabase, ensureAnonymousSession } from '../lib/supabase'
import { getSavedCustomer, saveCustomer } from '../lib/customerStorage'
import { PICKUP_TIMES } from '../lib/fallbackMenu'
import { Card, PrimaryButton, RadioOption, SectionTitle } from '../components/UI'

export default function Checkout() {
  const { lines, total, clearCart } = useCart()
  const { branches } = useMenu()
  const navigate = useNavigate()

  const saved = getSavedCustomer()
  const [name, setName] = useState(saved.name)
  const [phone, setPhone] = useState(saved.phone)
  const [branch, setBranch] = useState(branches[0]?.id)
  const [pickupTime, setPickupTime] = useState(PICKUP_TIMES[0].id)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!branch && branches.length > 0) setBranch(branches[0].id)
  }, [branches, branch])

  const phoneValid = /^05\d{8}$/.test(phone.trim())
  const canSubmit = name.trim().length >= 2 && phoneValid && branch && pickupTime && lines.length > 0 && !submitting

  async function handleConfirm() {
    if (!canSubmit) return
    setSubmitting(true)
    setError('')

    try {
      const session = await ensureAnonymousSession()
      if (!session) {
        setError('تعذر بدء الجلسة. تحقق من الاتصال بالإنترنت وحاول مرة أخرى.')
        setSubmitting(false)
        return
      }

      saveCustomer({ name: name.trim(), phone: phone.trim() })

      const items = lines.map(({ lineId: _lineId, ...rest }) => rest)

      const { data, error: insertError } = await supabase
        .from('orders')
        .insert({
          customer_phone: phone.trim(),
          customer_name: name.trim(),
          items,
          total,
          branch,
          pickup_time: pickupTime,
        })
        .select()
        .single()

      if (insertError) throw insertError

      clearCart()
      navigate(`/orders/${data.id}`, { replace: true })
    } catch (err) {
      setError(err.message ?? 'حدث خطأ أثناء إرسال الطلب. حاول مرة أخرى.')
      setSubmitting(false)
    }
  }

  return (
    <div className="pop-in pb-4">
      <h1 className="font-display font-extrabold text-2xl text-cream mb-5">تأكيد الطلب</h1>

      <SectionTitle>بياناتك</SectionTitle>
      <div className="space-y-3 mb-6">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="الاسم"
          className="w-full rounded-xl bg-navy-800 border-2 border-navy-700 px-4 py-3 text-cream-soft placeholder:text-cream-soft/40 focus:border-orange outline-none"
        />
        <input
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          placeholder="05xxxxxxxx"
          inputMode="numeric"
          dir="ltr"
          className="w-full rounded-xl bg-navy-800 border-2 border-navy-700 px-4 py-3 text-cream-soft placeholder:text-cream-soft/40 text-left focus:border-orange outline-none"
        />
        {phone && !phoneValid && <p className="text-xs text-red-400">رقم الجوال غير صحيح (مثال: 0512345678)</p>}
      </div>

      <SectionTitle>الفرع</SectionTitle>
      <div className="space-y-2 mb-6">
        {branches.map((b) => (
          <RadioOption key={b.id} label={b.name} selected={branch === b.id} onSelect={() => setBranch(b.id)} />
        ))}
      </div>

      <SectionTitle>وقت الاستلام</SectionTitle>
      <div className="space-y-2 mb-6">
        {PICKUP_TIMES.map((t) => (
          <RadioOption
            key={t.id}
            label={t.name}
            selected={pickupTime === t.id}
            onSelect={() => setPickupTime(t.id)}
          />
        ))}
      </div>

      <Card className="mb-6">
        <div className="flex items-center justify-between">
          <span className="font-semibold text-cream-soft/80">الإجمالي</span>
          <span className="font-display font-extrabold text-2xl text-orange">{total} ر.س</span>
        </div>
        <p className="text-xs text-cream-soft/50 mt-2">الدفع عند الاستلام 💵</p>
      </Card>

      {error && <p className="text-sm text-red-400 mb-3 text-center">{error}</p>}

      <PrimaryButton onClick={handleConfirm} disabled={!canSubmit}>
        {submitting ? 'جاري الإرسال...' : 'تأكيد الطلب'}
      </PrimaryButton>
    </div>
  )
}
