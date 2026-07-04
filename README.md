# كومبير | Kumpir

نظام طلبات كامل لفود ترك "كومبير" (بطاطس مشوية تركية) — جدة، السعودية.

المشروع مكوّن من تطبيقين منفصلين + قاعدة بيانات Supabase مشتركة:

| المجلد | الوصف |
|---|---|
| `apps/customer` | تطبيق العميل (PWA) — المنيو، السلة، الطلب، كرت الأختام، تتبع الطلب |
| `apps/dashboard` | لوحة تحكم المطعم — الطلبات الحية، تغيير الحالة، الإحصائيات |
| `supabase/schema.sql` | هيكل قاعدة البيانات كامل (جداول + RLS + Triggers) |

---

## 1) إعداد مشروع Supabase (خطوة يدوية)

1. أنشئ حساب/مشروع جديد من [supabase.com](https://supabase.com) (الخطة المجانية كافية).
2. بعد إنشاء المشروع، افتح **SQL Editor** والصق فيه محتوى ملف [`supabase/schema.sql`](./supabase/schema.sql) كاملاً ثم اضغط **Run**.
   - هذا ينشئ كل الجداول (`customers`, `orders`, `menu_items`, `addons`, `branches`, `corn_flavors`)
   - يفعّل **Row Level Security** بسياسات صحيحة لكل جدول
   - ينشئ الدوال والـ Triggers الخاصة ببرنامج الولاء (الأختام)
   - يضيف جدول `orders` إلى النشر الخاص بـ Realtime تلقائياً (`supabase_realtime`)
3. من تبويب **Authentication → Providers**، تأكد أن **Anonymous Sign-In** مُفعّل (مفعّل افتراضياً في المشاريع الجديدة). هذا يلزم تطبيق العميل حتى يقدر يسجّل ويتابع طلبه بدون تسجيل دخول حقيقي.
4. من تبويب **Authentication → Users**، أضف مستخدم/أكثر لموظفي الفروع (بريد إلكتروني + كلمة مرور) — هذا هو حساب الدخول للوحة التحكم (Dashboard). ليس له علاقة بالعميل نهائياً.
5. من **Project Settings → API** انسخ:
   - `Project URL`
   - `anon public` key

---

## 2) متغيرات البيئة

انسخ نفس القيم إلى ملفي `.env` في كلا التطبيقين:

```bash
cp apps/customer/.env.example apps/customer/.env
cp apps/dashboard/.env.example apps/dashboard/.env
```

ثم افتح كل ملف `.env` وضع فيه:

```
VITE_SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 3) التشغيل محلياً

يتطلب Node.js 18 أو أحدث.

### تطبيق العميل

```bash
cd apps/customer
npm install
npm run dev
```

يفتح على `http://localhost:5173`

### لوحة التحكم

```bash
cd apps/dashboard
npm install
npm run dev
```

يفتح على `http://localhost:5174` (أو أي منفذ متاح) — سجّل الدخول بالحساب اللي أنشأته في الخطوة 1.4.

> ملاحظة: لو ما ضبطت ملف `.env` بعد، تطبيق العميل يعرض بيانات منيو تجريبية محلية (fallback) عشان تقدر تعاين الواجهة، لكن الطلبات والأختام والطلبات الحية ما تشتغل فعلياً إلا بربط Supabase حقيقي.

---

## 4) تجربة الـ PWA (تثبيت التطبيق من الجوال)

1. شغّل بناء الإنتاج: `npm run build && npm run preview` داخل `apps/customer`
2. افتح الرابط من جوالك (أو انشر أولاً على Vercel — خطوات النشر بالأسفل)
3. من متصفح Chrome/Safari اضغط "إضافة إلى الشاشة الرئيسية" — يفتح كتطبيق مستقل بدون شريط المتصفح
4. يفضل ربط رابط الموقع برمز QR يوضع على طاولات/فواتير الفرع

---

## 5) هيكل قاعدة البيانات (ملخص)

- **`branches`**: الفروع (المروة، المحمدية، النسيم) — قابلة للتعديل من Table Editor مباشرة.
- **`menu_items`**: عناصر المنيو وأسعارها (الكومبير، كاسة ذرة، مشروب غازي، ماء).
- **`addons`**: الإضافات (مجانية/مدفوعة) المرتبطة بالكومبير أو كاسة الذرة.
- **`corn_flavors`**: نكهات كاسة الذرة.
- **`customers`**: كرت الولاء (`phone` مفتاح رئيسي، `stamps`, `rewards`) — تُحدَّث تلقائياً عبر Trigger عند كل طلب جديد، ولا يمكن للعميل تعديلها مباشرة.
- **`orders`**: الطلبات (`items` عمود `jsonb` يحوي تفاصيل كل بند وإضافاته، `status` من نوع enum: `new` → `preparing` → `ready` → `picked_up`).

تعديل الأسعار أو إضافة/تعطيل صنف أو إضافة يتم مباشرة من **Table Editor** في Supabase بدون أي تعديل على الكود.

### الأمان (RLS)

- العميل يستخدم جلسة **مجهولة** (Anonymous Auth) يتم إنشاؤها تلقائياً في المتصفح؛ يقدر يُنشئ طلب ويقرأ طلباته هو فقط (`auth_uid = auth.uid()`).
- كرت الأختام يُقرأ عبر دالة `get_stamp_card(phone)` فقط (RPC)، وما فيه قراءة مباشرة لجدول `customers` من العميل.
- موظفو اللوحة (تسجيل دخول حقيقي بالبريد/كلمة المرور) يقدرون يشوفون كل الطلبات ويغيّرون حالتها، بينما الجلسات المجهولة (العملاء) ما تقدر — يتم التفريق عبر `auth.jwt() ->> 'is_anonymous'`.

### الدفع

الدفع حالياً **عند الاستلام فقط**. عمود `orders.payment_method` جاهز بالفعل (القيمة الافتراضية `cash_on_pickup`) لإضافة بوابة دفع إلكتروني لاحقاً بدون تعديل بنية الجدول — فقط أضف مسار API/Edge Function للدفع وحدّث القيمة عند النجاح.

---

## 6) النشر على Vercel (مجاني) + ربط دومين

كل تطبيق (customer و dashboard) يُنشر **كمشروع Vercel منفصل** لأنهما تطبيقان مستقلان.

### أ) رفع الكود إلى GitHub

```bash
git add -A
git commit -m "المشروع الأولي"
git push
```

### ب) إنشاء مشروع Vercel لكل تطبيق

1. ادخل [vercel.com](https://vercel.com) → **Add New Project** → اختر الـ repo.
2. في خطوة الإعداد:
   - **Root Directory**: `apps/customer` (وكرر العملية مرة ثانية بمشروع منفصل بـ Root Directory = `apps/dashboard`)
   - **Framework Preset**: Vite (يكتشفه Vercel تلقائياً)
   - **Build Command**: `npm run build` (افتراضي)
   - **Output Directory**: `dist` (افتراضي)
3. في تبويب **Environment Variables** أضف نفس القيم من ملف `.env`:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
4. اضغط **Deploy**.

كرر الخطوات لإنشاء مشروع Vercel ثاني لـ `apps/dashboard` بنفس متغيرات البيئة.

### ج) ربط دومين مخصص

1. من صفحة المشروع في Vercel → **Settings → Domains**
2. أضف الدومين (مثلاً `order.kumpir.sa` لتطبيق العميل و `admin.kumpir.sa` للوحة التحكم)
3. Vercel يعطيك سجلات DNS (CNAME أو A) — أضفها عند مزوّد الدومين (كـ GoDaddy أو محلي.سا)
4. الشهادة (SSL) تتفعّل تلقائياً خلال دقائق بعد التحقق من الدومين

> نصيحة: بعد النشر، ولّد رمز QR يشير لرابط تطبيق العميل (أي مولّد QR مجاني أونلاين) واطبعه على الطاولات والفواتير.

---

## 7) ملخص أوامر سريعة

```bash
# قاعدة البيانات: نفّذ supabase/schema.sql مرة واحدة من SQL Editor في Supabase

# تطبيق العميل
cd apps/customer && npm install && cp .env.example .env   # ثم عدّل .env
npm run dev      # تطوير محلي
npm run build    # بناء إنتاج

# لوحة التحكم
cd apps/dashboard && npm install && cp .env.example .env  # ثم عدّل .env
npm run dev
npm run build
```
