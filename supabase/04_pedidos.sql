-- Laboratorio 10: pedidos de Brasas del Oriente.
-- Ejecute este archivo en Supabase SQL Editor antes de probar el checkout.

create table if not exists public.pedidos (
  id bigint generated always as identity primary key,
  nombre text not null check (length(trim(nombre)) > 0),
  telefono text not null check (telefono ~ '^[67][0-9]{7}$'),
  total numeric(10,2) not null check (total >= 0),
  estado text not null default 'pendiente'
    check (estado in ('pendiente', 'confirmado', 'cancelado')),
  created_at timestamptz not null default now()
);

create table if not exists public.pedido_detalles (
  id bigint generated always as identity primary key,
  pedido_id bigint not null references public.pedidos(id) on delete cascade,
  negocio_id bigint not null references public.negocios(id),
  nombre_producto text not null,
  cantidad integer not null check (cantidad between 1 and 50),
  precio_unitario numeric(10,2) not null check (precio_unitario >= 0),
  subtotal numeric(10,2) not null check (subtotal >= 0)
);

alter table public.pedidos enable row level security;
alter table public.pedido_detalles enable row level security;

create or replace function public.crear_pedido(
  p_nombre text,
  p_telefono text,
  p_items jsonb
)
returns bigint
language plpgsql
security definer
set search_path = public
as $$
declare
  v_pedido_id bigint;
  v_item jsonb;
  v_negocio_id bigint;
  v_cantidad integer;
  v_nombre_producto text;
  v_precio numeric(10,2);
  v_total numeric(10,2) := 0;
begin
  if length(trim(coalesce(p_nombre, ''))) = 0 then
    raise exception 'El nombre es obligatorio';
  end if;
  if coalesce(p_telefono, '') !~ '^[67][0-9]{7}$' then
    raise exception 'Teléfono boliviano inválido';
  end if;
  if p_items is null or jsonb_array_length(p_items) = 0 then
    raise exception 'El pedido debe contener al menos un producto';
  end if;

  insert into public.pedidos (nombre, telefono, total)
  values (trim(p_nombre), trim(p_telefono), 0)
  returning id into v_pedido_id;

  for v_item in select value from jsonb_array_elements(p_items)
  loop
    v_negocio_id := (v_item ->> 'negocio_id')::bigint;
    v_cantidad := (v_item ->> 'cantidad')::integer;
    if v_cantidad not between 1 and 50 then
      raise exception 'Cantidad inválida';
    end if;

    select nombre, precio into v_nombre_producto, v_precio
    from public.negocios
    where id = v_negocio_id;
    if not found then
      raise exception 'Producto no encontrado';
    end if;

    insert into public.pedido_detalles (
      pedido_id, negocio_id, nombre_producto, cantidad, precio_unitario, subtotal
    ) values (
      v_pedido_id, v_negocio_id, v_nombre_producto, v_cantidad, v_precio,
      v_precio * v_cantidad
    );
    v_total := v_total + (v_precio * v_cantidad);
  end loop;

  update public.pedidos set total = v_total where id = v_pedido_id;
  return v_pedido_id;
end;
$$;

grant execute on function public.crear_pedido(text, text, jsonb) to anon, authenticated;
