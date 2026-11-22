-- Actividad 4: foto de portada de Brasas del Oriente.
-- Requiere haber ejecutado 05_cuentas_roles.sql.

create table if not exists public.negocio_configuracion (
  id text primary key default 'brasas-del-oriente',
  nombre text not null default 'Brasas del Oriente',
  foto_path text,
  updated_at timestamptz not null default now(),
  constraint negocio_configuracion_id_check check (id = 'brasas-del-oriente')
);

insert into public.negocio_configuracion (id, nombre)
values ('brasas-del-oriente', 'Brasas del Oriente')
on conflict (id) do nothing;

alter table public.negocio_configuracion enable row level security;

drop policy if exists "foto del negocio visible" on public.negocio_configuracion;
create policy "foto del negocio visible"
on public.negocio_configuracion for select
using (true);

drop policy if exists "dueño actualiza foto del negocio" on public.negocio_configuracion;
create policy "dueño actualiza foto del negocio"
on public.negocio_configuracion for update
to authenticated
using (public.es_dueno())
with check (public.es_dueno());

drop policy if exists "dueño inserta configuracion del negocio" on public.negocio_configuracion;
create policy "dueño inserta configuracion del negocio"
on public.negocio_configuracion for insert
to authenticated
with check (public.es_dueno());

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'negocios',
  'negocios',
  true,
  5242880,
  array['image/jpeg', 'image/png', 'image/webp']
)
on conflict (id) do update
set public = excluded.public,
    file_size_limit = excluded.file_size_limit,
    allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "foto negocio lectura publica" on storage.objects;
create policy "foto negocio lectura publica"
on storage.objects for select
using (bucket_id = 'negocios');

drop policy if exists "dueño sube foto negocio" on storage.objects;
create policy "dueño sube foto negocio"
on storage.objects for insert
to authenticated
with check (
  bucket_id = 'negocios'
  and public.es_dueno()
  and (storage.foldername(name))[1] = 'brasas-del-oriente'
);

drop policy if exists "dueño actualiza foto negocio" on storage.objects;
create policy "dueño actualiza foto negocio"
on storage.objects for update
to authenticated
using (bucket_id = 'negocios' and public.es_dueno())
with check (
  bucket_id = 'negocios'
  and public.es_dueno()
  and (storage.foldername(name))[1] = 'brasas-del-oriente'
);

drop policy if exists "dueño elimina foto negocio" on storage.objects;
create policy "dueño elimina foto negocio"
on storage.objects for delete
to authenticated
using (bucket_id = 'negocios' and public.es_dueno());
