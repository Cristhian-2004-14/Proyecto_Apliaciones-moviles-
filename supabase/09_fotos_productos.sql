-- Actividad 4: fotos reales para cada producto del catálogo.
-- Ejecutar después de 07_storage_negocio.sql y 05_cuentas_roles.sql.

alter table public.negocios
add column if not exists imagen_path text;

-- Solo el dueño puede asociar o reemplazar la foto de un producto.
drop policy if exists "dueño actualiza fotos de productos" on public.negocios;
create policy "dueño actualiza fotos de productos"
on public.negocios for update
to authenticated
using (public.es_dueno())
with check (public.es_dueno());

-- El bucket ya fue creado en 07_storage_negocio.sql. Estas políticas
-- permiten las rutas productos/{id}/foto.ext sin abrir la escritura pública.
drop policy if exists "dueño sube foto negocio" on storage.objects;
create policy "dueño sube foto negocio"
on storage.objects for insert
to authenticated
with check (
  bucket_id = 'negocios'
  and public.es_dueno()
  and (storage.foldername(name))[1] in ('brasas-del-oriente', 'productos')
);

drop policy if exists "dueño actualiza foto negocio" on storage.objects;
create policy "dueño actualiza foto negocio"
on storage.objects for update
to authenticated
using (bucket_id = 'negocios' and public.es_dueno())
with check (
  bucket_id = 'negocios'
  and public.es_dueno()
  and (storage.foldername(name))[1] in ('brasas-del-oriente', 'productos')
);

drop policy if exists "dueño elimina foto negocio" on storage.objects;
create policy "dueño elimina foto negocio"
on storage.objects for delete
to authenticated
using (bucket_id = 'negocios' and public.es_dueno());
