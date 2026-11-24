-- Historial del cliente y gestión de reservas por el dueño.
-- Ejecutar después de 05_cuentas_roles.sql y 08_pagos_qr.sql.
-- Las reservas antiguas sin usuario siguen siendo visibles solo para el dueño.

alter table public.reservas
add column if not exists usuario_id uuid references auth.users(id) on delete set null;

alter table public.reservas
alter column usuario_id set default auth.uid();

alter table public.reservas
add column if not exists estado text not null default 'solicitada';

alter table public.reservas
drop constraint if exists reservas_estado_check;

alter table public.reservas
add constraint reservas_estado_check
check (estado in ('solicitada', 'aceptada', 'denegada'));

create index if not exists reservas_usuario_fecha_idx
on public.reservas (usuario_id, fecha desc, hora desc);

create index if not exists reservas_estado_fecha_idx
on public.reservas (estado, fecha, hora);

alter table public.reservas enable row level security;

-- Ya no se permiten reservas anónimas: así cada cliente puede ver su historial.
drop policy if exists "crear reservas" on public.reservas;
drop policy if exists "cliente crea su reserva" on public.reservas;
create policy "cliente crea su reserva"
on public.reservas for insert
to authenticated
with check (
  usuario_id = auth.uid()
  and nombre = btrim(nombre)
  and length(nombre) between 2 and 80
  and telefono ~ '^[67][0-9]{7}$'
  and fecha >= current_date
  and personas between 1 and 50
);

drop policy if exists "cliente o dueño lee reservas" on public.reservas;
create policy "cliente o dueño lee reservas"
on public.reservas for select
to authenticated
using (usuario_id = auth.uid() or public.es_dueno());

-- Solo el dueño puede aceptar o denegar una reserva.
drop policy if exists "dueño actualiza reservas" on public.reservas;
create policy "dueño actualiza reservas"
on public.reservas for update
to authenticated
using (public.es_dueno())
with check (public.es_dueno());

-- El historial del cliente muestra únicamente sus propios pedidos.
drop policy if exists "cliente lee pedidos propios" on public.pedidos;
create policy "cliente lee pedidos propios"
on public.pedidos for select
to authenticated
using (usuario_id = auth.uid() or public.es_dueno());
