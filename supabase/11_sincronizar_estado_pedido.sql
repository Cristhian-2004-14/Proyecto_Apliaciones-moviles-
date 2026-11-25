-- Sincroniza el estado del pedido con la revisión manual del pago.
-- Ejecutar una vez en Supabase SQL Editor después de 08_pagos_qr.sql.

-- Garantiza que cada pedido nuevo quede asociado a la cuenta que lo creó.
create or replace function public.crear_pedido(
  p_nombre text,
  p_telefono text,
  p_items jsonb
) returns bigint language plpgsql security definer set search_path = public as $$
declare
  v_pedido_id bigint;
  v_item jsonb;
  v_negocio_id bigint;
  v_cantidad integer;
  v_nombre_producto text;
  v_precio numeric(10,2);
  v_total numeric(10,2) := 0;
begin
  if auth.uid() is null then
    raise exception 'Debes iniciar sesión para crear un pedido';
  end if;
  if length(trim(coalesce(p_nombre, ''))) = 0 then
    raise exception 'El nombre es obligatorio';
  end if;
  if coalesce(p_telefono, '') !~ '^[67][0-9]{7}$' then
    raise exception 'Teléfono boliviano inválido';
  end if;
  if p_items is null or jsonb_array_length(p_items) = 0 then
    raise exception 'El pedido debe contener al menos un producto';
  end if;

  insert into public.pedidos (nombre, telefono, total, usuario_id)
  values (trim(p_nombre), trim(p_telefono), 0, auth.uid())
  returning id into v_pedido_id;

  for v_item in select value from jsonb_array_elements(p_items)
  loop
    v_negocio_id := (v_item ->> 'negocio_id')::bigint;
    v_cantidad := (v_item ->> 'cantidad')::integer;
    if v_cantidad not between 1 and 50 then
      raise exception 'Cantidad inválida';
    end if;
    select nombre, precio into v_nombre_producto, v_precio
    from public.negocios where id = v_negocio_id;
    if not found then raise exception 'Producto no encontrado'; end if;
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

grant execute on function public.crear_pedido(text, text, jsonb) to authenticated;

create or replace function public.resolver_pago_administrador(
  p_pago_id uuid, p_aprobar boolean, p_observaciones text, p_referencia_constatacion text
) returns void language plpgsql security definer set search_path = public as $$
declare
  v_pago public.pagos;
begin
  if not public.es_dueno() then
    raise exception 'Solo el dueño puede verificar pagos.';
  end if;

  select * into v_pago from public.pagos where id = p_pago_id for update;
  if not found then
    raise exception 'Pago no encontrado.';
  end if;
  if v_pago.estado = 'pagado' then
    raise exception 'Este pago ya fue aprobado.';
  end if;

  update public.pagos
  set estado = case when p_aprobar then 'pagado' else 'rechazado' end,
      updated_at = now()
  where id = p_pago_id;

  update public.pedidos
  set estado = case when p_aprobar then 'confirmado' else 'cancelado' end
  where id = v_pago.pedido_id;

  insert into public.auditoria_pagos (
    pago_id, administrador_id, accion, observaciones, referencia_constatacion
  ) values (
    p_pago_id,
    auth.uid(),
    case when p_aprobar then 'aprobado' else 'rechazado' end,
    nullif(trim(p_observaciones), ''),
    nullif(trim(p_referencia_constatacion), '')
  );
end;
$$;

-- Actualiza pedidos ya pagados o rechazados antes de esta mejora.
update public.pedidos as pedido
set estado = case
  when pago.estado = 'pagado' then 'confirmado'
  when pago.estado = 'rechazado' then 'cancelado'
  else pedido.estado
end
from public.pagos as pago
where pago.pedido_id = pedido.id;

grant execute on function public.resolver_pago_administrador(uuid, boolean, text, text)
to authenticated;
