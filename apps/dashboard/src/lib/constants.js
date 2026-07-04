export const STATUS_COLUMNS = [
  { key: 'new', label: 'جديد', color: 'bg-blue-500/15 text-blue-300 border-blue-500/30' },
  { key: 'preparing', label: 'قيد التحضير', color: 'bg-orange/15 text-orange border-orange/30' },
  { key: 'ready', label: 'جاهز للاستلام', color: 'bg-green-500/15 text-green-300 border-green-500/30' },
  { key: 'picked_up', label: 'مستلم', color: 'bg-cream-soft/10 text-cream-soft/60 border-cream-soft/20' },
]

export const NEXT_STATUS = {
  new: 'preparing',
  preparing: 'ready',
  ready: 'picked_up',
  picked_up: null,
}

export const NEXT_STATUS_LABEL = {
  new: 'ابدأ التحضير',
  preparing: 'جاهز للاستلام',
  ready: 'تم الاستلام',
  picked_up: null,
}

export const PICKUP_TIME_LABELS = {
  asap: 'بأسرع وقت',
  15: '15 دقيقة',
  30: '30 دقيقة',
  60: 'ساعة',
}
