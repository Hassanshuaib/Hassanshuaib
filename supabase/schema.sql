-- =========================================================
-- كومبير | Kumpir — Supabase schema
-- شغّل هذا الملف كامل من SQL Editor في مشروع Supabase
-- =========================================================

-- ---------- Extensions ----------
create extension if not exists "pgcrypto";

-- ---------- Enums ----------
do $$
begin
  if not exists (select 1 from pg_type where typname = 'order_status') then
    create type order_status as enum ('new', 'preparing', 'ready', 'picked_up');
  end if;
end$$;

-- ---------- Branches ----------
create table if not exists branches (
  id text primary key,
  name text not null,
  sort_order int not null default 0,
  active boolean not null default true
);

insert into branches (id, name, sort_order) values
  ('almarwah', 'المروة', 1),
  ('almuhammadiyah', 'المحمدية', 2),
  ('annaseem', 'النسيم', 3)
on conflict (id) do nothing;

-- ---------- Menu items ----------
-- category: 'kumpir' | 'corn' | 'drink'
create table if not exists menu_items (
  id text primary key,
  category text not null,
  name text not null,
  description text,
  price numeric(10,2) not null,
  active boolean not null default true,
  sort_order int not null default 0
);

insert into menu_items (id, category, name, description, price, sort_order) values
  ('kumpir', 'kumpir', 'الكومبير', 'بطاطس مشوية تركية تُركّب بإضافاتك المفضلة', 22, 1),
  ('corn_cup', 'corn', 'كاسة ذرة', 'ذرة طازجة بنكهتك المفضلة', 9, 2),
  ('soda', 'drink', 'مشروب غازي', '', 3, 3),
  ('water', 'drink', 'ماء', '', 1, 4)
on conflict (id) do nothing;

-- ---------- Addons ----------
-- kind: 'free' | 'paid'
-- applies_to: 'kumpir' | 'corn'
create table if not exists addons (
  id text primary key,
  applies_to text not null,
  kind text not null,
  name text not null,
  price numeric(10,2) not null default 0,
  active boolean not null default true,
  sort_order int not null default 0
);

insert into addons (id, applies_to, kind, name, price, sort_order) values
  ('butter',            'kumpir', 'free', 'زبدة',                 0, 1),
  ('cheddar',           'kumpir', 'free', 'جبنة شيدر',            0, 2),
  ('mozzarella',        'kumpir', 'free', 'موزوريلا',             0, 3),
  ('corn_topping',      'kumpir', 'free', 'ذرة',                  0, 4),
  ('pickles',           'kumpir', 'free', 'مخلل خيار',            0, 5),
  ('jalapeno',          'kumpir', 'free', 'هالبينو',              0, 6),
  ('red_beans',         'kumpir', 'free', 'فاصوليا حمراء',        0, 7),
  ('black_olives',      'kumpir', 'free', 'زيتون أسود',           0, 8),
  ('turkish_spice',     'kumpir', 'free', 'بهارات تركية حارة',    0, 9),
  ('ranch',             'kumpir', 'free', 'رانش',                 0, 10),
  ('mayo',              'kumpir', 'free', 'مايونيز',              0, 11),
  ('ketchup',           'kumpir', 'free', 'كاتشب',                0, 12),
  ('chicken_strips',    'kumpir', 'paid', 'دجاج ستريبس',          4, 13),
  ('hot_dog',           'kumpir', 'paid', 'هوت دوق',              3, 14),
  ('oman_sticks',       'kumpir', 'paid', 'عيدان عمان',           3, 15),
  ('crushed_cheetos',   'kumpir', 'paid', 'شيتوس مطحون',          3, 16)
on conflict (id) do nothing;

insert into addons (id, applies_to, kind, name, price, sort_order) values
  ('extra_cheetos', 'corn', 'paid', 'زد شيتوس', 2, 1)
on conflict (id) do nothing;

-- كاسة الذرة: نكهة واحدة (Chef / Cheddar / Lemon & Pepper) — تُحفظ كخيار داخل بند الطلب،
-- وليست إضافة منفصلة، لكن نعرضها هنا كمرجع قابل للتعديل من الداشبورد لاحقاً إن رغبت.
create table if not exists corn_flavors (
  id text primary key,
  name text not null,
  sort_order int not null default 0,
  active boolean not null default true
);

insert into corn_flavors (id, name, sort_order) values
  ('chef',   'نكهة الشيف',      1),
  ('cheddar','جبنة شيدر',       2),
  ('lemon_pepper', 'ليمون وفلفل', 3)
on conflict (id) do nothing;

-- ---------- Customers (loyalty) ----------
create table if not exists customers (
  phone text primary key,
  name text,
  stamps int not null default 0,
  rewards int not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- ---------- Orders ----------
create table if not exists orders (
  id uuid primary key default gen_random_uuid(),
  order_number bigint generated always as identity,
  auth_uid uuid not null default auth.uid(),
  customer_phone text not null references customers(phone) on delete restrict,
  customer_name text not null,
  items jsonb not null,
  total numeric(10,2) not null,
  branch text not null references branches(id),
  pickup_time text not null,
  status order_status not null default 'new',
  -- الدفع حالياً "عند الاستلام" فقط. العمود جاهز لإضافة بوابة دفع لاحقاً
  -- (مثلاً 'online') بدون تعديل بنية الجدول.
  payment_method text not null default 'cash_on_pickup',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists orders_branch_idx on orders(branch);
create index if not exists orders_status_idx on orders(status);
create index if not exists orders_auth_uid_idx on orders(auth_uid);
create index if not exists orders_customer_phone_idx on orders(customer_phone);

-- ---------- updated_at triggers ----------
create or replace function set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists orders_set_updated_at on orders;
create trigger orders_set_updated_at
  before update on orders
  for each row execute function set_updated_at();

drop trigger if exists customers_set_updated_at on customers;
create trigger customers_set_updated_at
  before update on customers
  for each row execute function set_updated_at();

-- ---------- Loyalty: upsert customer + stamp on new order ----------
create or replace function handle_new_order()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  current_stamps int;
begin
  insert into customers (phone, name, stamps)
  values (new.customer_phone, new.customer_name, 1)
  on conflict (phone) do update
    set name = excluded.name,
        stamps = customers.stamps + 1
  returning stamps into current_stamps;

  if current_stamps >= 8 then
    update customers
      set stamps = 0,
          rewards = rewards + 1
      where phone = new.customer_phone;
  end if;

  return new;
end;
$$;

drop trigger if exists orders_handle_new_order on orders;
create trigger orders_handle_new_order
  after insert on orders
  for each row execute function handle_new_order();

-- ---------- RPC: قراءة كرت الأختام برقم الجوال بدون كشف الجدول كامل ----------
create or replace function get_stamp_card(p_phone text)
returns table (phone text, name text, stamps int, rewards int)
language sql
security definer
set search_path = public
as $$
  select phone, name, stamps, rewards
  from customers
  where phone = p_phone;
$$;

-- =========================================================
-- Row Level Security
-- =========================================================
alter table branches enable row level security;
alter table menu_items enable row level security;
alter table addons enable row level security;
alter table corn_flavors enable row level security;
alter table customers enable row level security;
alter table orders enable row level security;

-- القوائم والفروع والإضافات: قراءة عامة، وتعديل لموظفي الفروع فقط (مسجلين دخول فعليين لا زوّار)
create policy "public read branches" on branches for select using (true);
create policy "staff write branches" on branches for all
  using ((auth.jwt() ->> 'is_anonymous') is not true)
  with check ((auth.jwt() ->> 'is_anonymous') is not true);

create policy "public read menu_items" on menu_items for select using (true);
create policy "staff write menu_items" on menu_items for all
  using ((auth.jwt() ->> 'is_anonymous') is not true)
  with check ((auth.jwt() ->> 'is_anonymous') is not true);

create policy "public read addons" on addons for select using (true);
create policy "staff write addons" on addons for all
  using ((auth.jwt() ->> 'is_anonymous') is not true)
  with check ((auth.jwt() ->> 'is_anonymous') is not true);

create policy "public read corn_flavors" on corn_flavors for select using (true);
create policy "staff write corn_flavors" on corn_flavors for all
  using ((auth.jwt() ->> 'is_anonymous') is not true)
  with check ((auth.jwt() ->> 'is_anonymous') is not true);

-- customers: لا قراءة/كتابة مباشرة من العميل — كل شيء عبر get_stamp_card() و trigger الأختام.
-- الموظفون (تسجيل دخول حقيقي) يقدرون يشوفون العملاء عند الحاجة.
create policy "staff read customers" on customers for select
  using ((auth.jwt() ->> 'is_anonymous') is not true);

-- orders: العميل ينشئ طلب مرتبط بجلسته المجهولة، ويقرأ طلباته فقط.
-- الموظفون يقرؤون كل الطلبات ويحدّثون حالتها فقط.
create policy "customer insert own order" on orders for insert
  with check (auth_uid = auth.uid());

create policy "customer read own orders" on orders for select
  using (auth_uid = auth.uid());

create policy "staff read all orders" on orders for select
  using ((auth.jwt() ->> 'is_anonymous') is not true);

create policy "staff update orders" on orders for update
  using ((auth.jwt() ->> 'is_anonymous') is not true)
  with check ((auth.jwt() ->> 'is_anonymous') is not true);

-- ---------- Realtime ----------
alter publication supabase_realtime add table orders;
