-- Extra: pagos con QR fijo y revisión documental de comprobantes.
-- Ejecutar después de 04_pedidos.sql y 05_cuentas_roles.sql.
-- No contiene cuentas, nombres, NIT ni códigos bancarios reales.

create table if not exists public.configuracion_qr_pago (
  id uuid primary key default gen_random_uuid(),
  qr_path text not null,
  beneficiario text not null,
  cuenta_destino text not null,
  activo boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create unique index if not exists configuracion_qr_pago_unico_activo
on public.configuracion_qr_pago (activo) where activo;

create table if not exists public.pagos (
  id uuid primary key default gen_random_uuid(),
  pedido_id bigint not null unique references public.pedidos(id) on delete restrict,
  usuario_id uuid not null references auth.users(id) on delete restrict,
  configuracion_qr_id uuid references public.configuracion_qr_pago(id) on delete set null,
  monto_esperado numeric(10,2) not null check (monto_esperado > 0),
  estado text not null default 'pendiente' check (estado in (
    'pendiente', 'en_validacion', 'comprobante_validado',
    'revision_manual', 'rechazado', 'pagado'
  )),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists pagos_estado_created_at_idx
on public.pagos (estado, created_at desc);

create table if not exists public.comprobantes_pago (
  id uuid primary key default gen_random_uuid(),
  pago_id uuid not null references public.pagos(id) on delete cascade,
  ruta text not null unique,
  hash_sha256 text not null check (hash_sha256 ~ '^[a-f0-9]{64}$'),
  banco_detectado text,
  exitoso_detectado boolean,
  monto_detectado numeric(10,2),
  fecha_operacion date,
  beneficiario_detectado text,
  cuenta_destino_detectada text,
  codigo_operacion text,
  texto_ocr text,
  validacion jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists comprobantes_pago_hash_idx
on public.comprobantes_pago (hash_sha256);
create index if not exists comprobantes_pago_codigo_idx
on public.comprobantes_pago (codigo_operacion)
where codigo_operacion is not null;

create table if not exists public.intentos_reutilizacion_comprobante (
  id bigint generated always as identity primary key,
  pago_id uuid not null references public.pagos(id) on delete cascade,
  hash_sha256 text,
  codigo_operacion text,
  motivo text not null,
  created_at timestamptz not null default now()
);

create table if not exists public.auditoria_pagos (
  id bigint generated always as identity primary key,
  pago_id uuid not null references public.pagos(id) on delete cascade,
  administrador_id uuid not null references auth.users(id) on delete restrict,
  accion text not null check (accion in ('aprobado', 'rechazado')),
  observaciones text,
  referencia_constatacion text,
  created_at timestamptz not null default now()
);

alter table public.configuracion_qr_pago enable row level security;
alter table public.pagos enable row level security;
alter table public.comprobantes_pago enable row level security;
alter table public.intentos_reutilizacion_comprobante enable row level security;
alter table public.auditoria_pagos enable row level security;

drop policy if exists "dueño administra QR de pago" on public.configuracion_qr_pago;
create policy "dueño administra QR de pago"
on public.configuracion_qr_pago for all to authenticated
using (public.es_dueno()) with check (public.es_dueno());

drop policy if exists "usuario o dueño lee pagos" on public.pagos;
create policy "usuario o dueño lee pagos"
on public.pagos for select to authenticated
using (usuario_id = auth.uid() or public.es_dueno());

drop policy if exists "usuario o dueño lee comprobantes" on public.comprobantes_pago;
create policy "usuario o dueño lee comprobantes"
on public.comprobantes_pago for select to authenticated
using (
  public.es_dueno() or exists (
    select 1 from public.pagos p
    where p.id = pago_id and p.usuario_id = auth.uid()
  )
);

drop policy if exists "dueño lee reutilizaciones" on public.intentos_reutilizacion_comprobante;
create policy "dueño lee reutilizaciones"
on public.intentos_reutilizacion_comprobante for select to authenticated
using (public.es_dueno());

drop policy if exists "dueño lee auditoria pagos" on public.auditoria_pagos;
create policy "dueño lee auditoria pagos"
on public.auditoria_pagos for select to authenticated
using (public.es_dueno());

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('pagos_qr', 'pagos_qr', true, 5242880, array['image/jpeg', 'image/png'])
on conflict (id) do update set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('comprobantes_pago', 'comprobantes_pago', false, 5242880, array['image/jpeg', 'image/png'])
on conflict (id) do update set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "dueño carga QR de pago" on storage.objects;
create policy "dueño carga QR de pago"
on storage.objects for insert to authenticated
with check (bucket_id = 'pagos_qr' and public.es_dueno());

drop policy if exists "dueño actualiza QR de pago" on storage.objects;
create policy "dueño actualiza QR de pago"
on storage.objects for update to authenticated
using (bucket_id = 'pagos_qr' and public.es_dueno())
with check (bucket_id = 'pagos_qr' and public.es_dueno());

drop policy if exists "cliente sube comprobante propio" on storage.objects;
create policy "cliente sube comprobante propio"
on storage.objects for insert to authenticated
with check (
  bucket_id = 'comprobantes_pago'
  and exists (
    select 1 from public.pagos p
    where p.id::text = (storage.foldername(name))[1]
      and p.usuario_id = auth.uid()
  )
);

drop policy if exists "cliente o dueño lee comprobante privado" on storage.objects;
create policy "cliente o dueño lee comprobante privado"
on storage.objects for select to authenticated
using (
  bucket_id = 'comprobantes_pago'
  and (
    public.es_dueno() or exists (
      select 1 from public.pagos p
      where p.id::text = (storage.foldername(name))[1]
        and p.usuario_id = auth.uid()
    )
  )
);

create or replace function public.obtener_qr_pago_activo()
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_qr public.configuracion_qr_pago;
begin
  select * into v_qr from public.configuracion_qr_pago
  where activo = true order by updated_at desc limit 1;
  if not found then return null; end if;
  return jsonb_build_object(
    'id', v_qr.id, 'qr_path', v_qr.qr_path, 'beneficiario', v_qr.beneficiario
  );
end;
$$;

create or replace function public.crear_pago_para_pedido(p_pedido_id bigint)
returns jsonb language plpgsql security definer set search_path = public as $$
declare
  v_pedido public.pedidos;
  v_qr public.configuracion_qr_pago;
  v_pago public.pagos;
begin
  if auth.uid() is null then raise exception 'Debes iniciar sesión para pagar.'; end if;
  select * into v_pedido from public.pedidos where id = p_pedido_id for update;
  if not found then raise exception 'Pedido no encontrado.'; end if;
  if v_pedido.usuario_id is null then
    update public.pedidos set usuario_id = auth.uid() where id = p_pedido_id;
  elsif v_pedido.usuario_id <> auth.uid() and not public.es_dueno() then
    raise exception 'No puedes pagar un pedido de otro usuario.';
  end if;
  select * into v_qr from public.configuracion_qr_pago where activo = true limit 1;
  if not found then raise exception 'El restaurante aún no configuró un QR de pago.'; end if;
  insert into public.pagos (pedido_id, usuario_id, configuracion_qr_id, monto_esperado)
  values (v_pedido.id, auth.uid(), v_qr.id, v_pedido.total)
  on conflict (pedido_id) do update set updated_at = now()
  returning * into v_pago;
  return jsonb_build_object(
    'id', v_pago.id, 'pedido_id', v_pago.pedido_id,
    'monto_esperado', v_pago.monto_esperado, 'estado', v_pago.estado,
    'created_at', v_pago.created_at, 'qr_path', v_qr.qr_path,
    'beneficiario', v_qr.beneficiario
  );
end;
$$;

create or replace function public.registrar_comprobante_pago(
  p_pago_id uuid, p_ruta text, p_hash_sha256 text, p_texto_ocr text,
  p_banco text, p_exitoso boolean, p_monto numeric, p_fecha date,
  p_beneficiario text, p_cuenta_destino text, p_codigo_operacion text
) returns jsonb language plpgsql security definer set search_path = public as $$
declare
  v_pago public.pagos; v_qr public.configuracion_qr_pago; v_pedido public.pedidos;
  v_hash_duplicado boolean; v_codigo_duplicado boolean; v_estado text; v_validacion jsonb;
begin
  select * into v_pago from public.pagos where id = p_pago_id for update;
  if not found or (v_pago.usuario_id <> auth.uid() and not public.es_dueno()) then
    raise exception 'Pago no autorizado.';
  end if;
  if p_ruta not like p_pago_id::text || '/%' then raise exception 'Ruta de comprobante inválida.'; end if;
  select * into v_qr from public.configuracion_qr_pago where id = v_pago.configuracion_qr_id;
  select * into v_pedido from public.pedidos where id = v_pago.pedido_id;
  select exists(select 1 from public.comprobantes_pago where hash_sha256 = p_hash_sha256 and pago_id <> p_pago_id) into v_hash_duplicado;
  select exists(select 1 from public.comprobantes_pago where codigo_operacion = nullif(trim(p_codigo_operacion), '') and pago_id <> p_pago_id) into v_codigo_duplicado;
  if v_hash_duplicado or v_codigo_duplicado then
    insert into public.intentos_reutilizacion_comprobante (pago_id, hash_sha256, codigo_operacion, motivo)
    values (p_pago_id, p_hash_sha256, nullif(trim(p_codigo_operacion), ''),
      case when v_hash_duplicado then 'Hash SHA-256 ya usado' else 'Código de operación ya usado' end);
  end if;
  v_validacion := jsonb_build_object(
    'banco_correcto', lower(coalesce(p_banco, '')) like '%mercantil%santa%cruz%',
    'operacion_exitosa', coalesce(p_exitoso, false),
    'monto_correcto', coalesce(p_monto = v_pago.monto_esperado, false),
    'beneficiario_correcto', lower(trim(coalesce(p_beneficiario, ''))) = lower(trim(v_qr.beneficiario)),
    'cuenta_correcta', regexp_replace(coalesce(p_cuenta_destino, ''), '\D', '', 'g') = regexp_replace(v_qr.cuenta_destino, '\D', '', 'g'),
    'fecha_compatible', coalesce(p_fecha >= (v_pedido.created_at at time zone 'America/La_Paz')::date, false),
    'codigo_duplicado', v_codigo_duplicado,
    'archivo_duplicado', v_hash_duplicado
  );
  if (v_validacion->>'banco_correcto')::boolean and (v_validacion->>'operacion_exitosa')::boolean
    and (v_validacion->>'monto_correcto')::boolean and (v_validacion->>'beneficiario_correcto')::boolean
    and (v_validacion->>'cuenta_correcta')::boolean and (v_validacion->>'fecha_compatible')::boolean
    and not v_hash_duplicado and not v_codigo_duplicado then v_estado := 'comprobante_validado';
  else v_estado := 'revision_manual'; end if;
  insert into public.comprobantes_pago (
    pago_id, ruta, hash_sha256, banco_detectado, exitoso_detectado, monto_detectado,
    fecha_operacion, beneficiario_detectado, cuenta_destino_detectada, codigo_operacion, texto_ocr, validacion
  ) values (
    p_pago_id, p_ruta, p_hash_sha256, nullif(trim(p_banco), ''), p_exitoso, p_monto,
    p_fecha, nullif(trim(p_beneficiario), ''), nullif(trim(p_cuenta_destino), ''),
    nullif(trim(p_codigo_operacion), ''), p_texto_ocr, v_validacion
  );
  update public.pagos set estado = v_estado, updated_at = now() where id = p_pago_id;
  return jsonb_build_object('id', v_pago.id, 'pedido_id', v_pago.pedido_id,
    'monto_esperado', v_pago.monto_esperado, 'estado', v_estado,
    'created_at', v_pago.created_at);
end;
$$;

create or replace function public.resolver_pago_administrador(
  p_pago_id uuid, p_aprobar boolean, p_observaciones text, p_referencia_constatacion text
) returns void language plpgsql security definer set search_path = public as $$
declare v_pago public.pagos;
begin
  if not public.es_dueno() then raise exception 'Solo el dueño puede verificar pagos.'; end if;
  select * into v_pago from public.pagos where id = p_pago_id for update;
  if not found then raise exception 'Pago no encontrado.'; end if;
  if v_pago.estado = 'pagado' then raise exception 'Este pago ya fue aprobado.'; end if;
  update public.pagos set estado = case when p_aprobar then 'pagado' else 'rechazado' end,
    updated_at = now() where id = p_pago_id;
  insert into public.auditoria_pagos (pago_id, administrador_id, accion, observaciones, referencia_constatacion)
  values (p_pago_id, auth.uid(), case when p_aprobar then 'aprobado' else 'rechazado' end,
    nullif(trim(p_observaciones), ''), nullif(trim(p_referencia_constatacion), ''));
end;
$$;

grant execute on function public.obtener_qr_pago_activo() to authenticated;
grant execute on function public.crear_pago_para_pedido(bigint) to authenticated;
grant execute on function public.registrar_comprobante_pago(uuid, text, text, text, text, boolean, numeric, date, text, text, text) to authenticated;
grant execute on function public.resolver_pago_administrador(uuid, boolean, text, text) to authenticated;
