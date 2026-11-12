alter table public.negocios enable row level security;
alter table public.consultas enable row level security;
alter table public.reservas enable row level security;

drop policy if exists "lectura publica negocios" on public.negocios;
create policy "lectura publica negocios"
on public.negocios for select
to anon, authenticated
using (true);
