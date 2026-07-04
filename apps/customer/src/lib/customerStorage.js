const KEY = 'kumpir_customer_v1'

export function getSavedCustomer() {
  try {
    const raw = localStorage.getItem(KEY)
    return raw ? JSON.parse(raw) : { name: '', phone: '' }
  } catch {
    return { name: '', phone: '' }
  }
}

export function saveCustomer({ name, phone }) {
  localStorage.setItem(KEY, JSON.stringify({ name, phone }))
}
