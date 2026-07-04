import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn(
    'إعدادات Supabase ناقصة. أنشئ ملف .env من .env.example وضع فيه VITE_SUPABASE_URL و VITE_SUPABASE_ANON_KEY. سيتم استخدام بيانات تجريبية محلية للمعاينة فقط.'
  )
}

// عنوان وهمي حتى لا ينهار التطبيق بدون .env — الاستعلامات ستفشل بهدوء وتستخدم الواجهة بياناتها الاحتياطية
export const supabase = createClient(supabaseUrl || 'https://placeholder.supabase.co', supabaseAnonKey || 'placeholder-anon-key', {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
  },
})

/**
 * تسجيل دخول مجهول لهذا الجهاز إن لم توجد جلسة بعد.
 * يلزم لتفعيل RLS (auth_uid = auth.uid()) بدون ما نطلب من العميل تسجيل دخول حقيقي.
 */
export async function ensureAnonymousSession() {
  const { data } = await supabase.auth.getSession()
  if (data.session) return data.session

  const { data: signInData, error } = await supabase.auth.signInAnonymously()
  if (error) {
    console.error('تعذر بدء الجلسة:', error.message)
    return null
  }
  return signInData.session
}
