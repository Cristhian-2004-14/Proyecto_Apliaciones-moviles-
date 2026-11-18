-- Laboratorio 11: cuentas, perfiles y roles de Brasas del Oriente.
-- Ejecute este archivo después de 04_pedidos.sql.

create table if not exists public.perfiles (
  id uuid primary key references auth.users(id) on delete cascade,
  nombre text not null,
  rol text not null default 'cliente' check (rol in ('cliente', 'dueno')),
  created_at timestamptz not null default now()
);

alter table public.pedidos
add column if not exists usuario_id uuid references auth.users(id) on delete set null;

alter table public.pedidos
alter column usuario_id set default auth.uid();

alter table public.perfiles enable row level security;

create or replace function public.crear_perfil_al_registrarse()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.perfiles (id, nombre)
  values (
    new.id,
    coalesce(nullif(trim(new.raw_user_meta_data ->> 'nombre'), ''), split_part(new.email, '@', 1))
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists crear_perfil_al_registrarse on auth.users;
create trigger crear_perfil_al_registrarse
after insert on auth.users
for each row execute function public.crear_perfil_al_registrarse();

insert into public.perfiles (id, nombre)
select
  id,
  coalesce(nullif(trim(raw_user_meta_data ->> 'nombre'), ''), split_part(email, '@', 1))
from auth.users
on conflict (id) do nothing;

create or replace function public.es_dueno()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.perfiles
    where id = auth.uid() and rol = 'dueno'
  );
$$;

grant execute on function public.es_dueno() to authenticated;

drop policy if exists "leer perfil propio o perfiles como dueño" on public.perfiles;
create policy "leer perfil propio o perfiles como dueño"
on public.perfiles for select
to authenticated
using (id = auth.uid() or public.es_dueno());

drop policy if exists "dueño lee pedidos" on public.pedidos;
create policy "dueño lee pedidos"
on public.pedidos for select
to authenticated
using (public.es_dueno());

drop policy if exists "dueño lee detalles de pedidos" on public.pedido_detalles;
create policy "dueño lee detalles de pedidos"
on public.pedido_detalles for select
to authenticated
using (public.es_dueno());

-- Después de registrar la cuenta que administrará la churrasquería,
-- ejecute esta sentencia reemplazando el UUID real del perfil:
-- update public.perfiles set rol = 'dueno' where id = 'UUID_DEL_DUENO';
