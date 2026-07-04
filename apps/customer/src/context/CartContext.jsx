import { createContext, useContext, useEffect, useMemo, useState } from 'react'

const CartContext = createContext(null)
const STORAGE_KEY = 'kumpir_cart_v1'

function loadCart() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

let idCounter = 0
function nextLineId() {
  idCounter += 1
  return `${Date.now()}_${idCounter}`
}

export function CartProvider({ children }) {
  const [lines, setLines] = useState(loadCart)

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(lines))
  }, [lines])

  function addLine(line) {
    setLines((prev) => [...prev, { ...line, lineId: nextLineId() }])
  }

  function removeLine(lineId) {
    setLines((prev) => prev.filter((l) => l.lineId !== lineId))
  }

  function updateQuantity(lineId, quantity) {
    setLines((prev) =>
      prev
        .map((l) => (l.lineId === lineId ? { ...l, quantity, lineTotal: (l.unitPrice ?? l.lineTotal / l.quantity) * quantity } : l))
        .filter((l) => l.quantity > 0)
    )
  }

  function clearCart() {
    setLines([])
  }

  const total = useMemo(() => lines.reduce((sum, l) => sum + l.lineTotal, 0), [lines])
  const count = useMemo(() => lines.reduce((sum, l) => sum + l.quantity, 0), [lines])

  const value = { lines, addLine, removeLine, updateQuantity, clearCart, total, count }

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}

export function useCart() {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCart must be used inside CartProvider')
  return ctx
}
