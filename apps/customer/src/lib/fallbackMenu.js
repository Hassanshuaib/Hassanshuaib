// نسخة احتياطية محلية تُستخدم فقط إذا تعذر الاتصال بـ Supabase (بدون إعداد .env مثلاً)
// حتى تبقى الواجهة قابلة للمعاينة. المصدر الحقيقي للأسعار دائماً جداول menu_items/addons.

export const FALLBACK_MENU_ITEMS = [
  { id: 'kumpir', category: 'kumpir', name: 'الكومبير', description: 'بطاطس مشوية تركية تُركّب بإضافاتك المفضلة', price: 22, sort_order: 1 },
  { id: 'corn_cup', category: 'corn', name: 'كاسة ذرة', description: 'ذرة طازجة بنكهتك المفضلة', price: 9, sort_order: 2 },
  { id: 'soda', category: 'drink', name: 'مشروب غازي', description: '', price: 3, sort_order: 3 },
  { id: 'water', category: 'drink', name: 'ماء', description: '', price: 1, sort_order: 4 },
]

export const FALLBACK_ADDONS = [
  { id: 'butter', applies_to: 'kumpir', kind: 'free', name: 'زبدة', price: 0, sort_order: 1 },
  { id: 'cheddar', applies_to: 'kumpir', kind: 'free', name: 'جبنة شيدر', price: 0, sort_order: 2 },
  { id: 'mozzarella', applies_to: 'kumpir', kind: 'free', name: 'موزوريلا', price: 0, sort_order: 3 },
  { id: 'corn_topping', applies_to: 'kumpir', kind: 'free', name: 'ذرة', price: 0, sort_order: 4 },
  { id: 'pickles', applies_to: 'kumpir', kind: 'free', name: 'مخلل خيار', price: 0, sort_order: 5 },
  { id: 'jalapeno', applies_to: 'kumpir', kind: 'free', name: 'هالبينو', price: 0, sort_order: 6 },
  { id: 'red_beans', applies_to: 'kumpir', kind: 'free', name: 'فاصوليا حمراء', price: 0, sort_order: 7 },
  { id: 'black_olives', applies_to: 'kumpir', kind: 'free', name: 'زيتون أسود', price: 0, sort_order: 8 },
  { id: 'turkish_spice', applies_to: 'kumpir', kind: 'free', name: 'بهارات تركية حارة', price: 0, sort_order: 9 },
  { id: 'ranch', applies_to: 'kumpir', kind: 'free', name: 'رانش', price: 0, sort_order: 10 },
  { id: 'mayo', applies_to: 'kumpir', kind: 'free', name: 'مايونيز', price: 0, sort_order: 11 },
  { id: 'ketchup', applies_to: 'kumpir', kind: 'free', name: 'كاتشب', price: 0, sort_order: 12 },
  { id: 'chicken_strips', applies_to: 'kumpir', kind: 'paid', name: 'دجاج ستريبس', price: 4, sort_order: 13 },
  { id: 'hot_dog', applies_to: 'kumpir', kind: 'paid', name: 'هوت دوق', price: 3, sort_order: 14 },
  { id: 'oman_sticks', applies_to: 'kumpir', kind: 'paid', name: 'عيدان عمان', price: 3, sort_order: 15 },
  { id: 'crushed_cheetos', applies_to: 'kumpir', kind: 'paid', name: 'شيتوس مطحون', price: 3, sort_order: 16 },
  { id: 'extra_cheetos', applies_to: 'corn', kind: 'paid', name: 'زد شيتوس', price: 2, sort_order: 1 },
]

export const FALLBACK_CORN_FLAVORS = [
  { id: 'chef', name: 'نكهة الشيف', sort_order: 1 },
  { id: 'cheddar', name: 'جبنة شيدر', sort_order: 2 },
  { id: 'lemon_pepper', name: 'ليمون وفلفل', sort_order: 3 },
]

export const BRANCHES = [
  { id: 'almarwah', name: 'المروة' },
  { id: 'almuhammadiyah', name: 'المحمدية' },
  { id: 'annaseem', name: 'النسيم' },
]

export const PICKUP_TIMES = [
  { id: 'asap', name: 'بأسرع وقت' },
  { id: '15', name: '15 دقيقة' },
  { id: '30', name: '30 دقيقة' },
  { id: '60', name: 'ساعة' },
]

export const ORDER_STATUS_LABELS = {
  new: 'جديد',
  preparing: 'قيد التحضير',
  ready: 'جاهز للاستلام',
  picked_up: 'تم الاستلام',
}
