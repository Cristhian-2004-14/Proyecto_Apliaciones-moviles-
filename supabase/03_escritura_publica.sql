drop policy if exists "crear consultas" on public.consultas;
create policy "crear consultas"
on public.consultas for insert
to anon, authenticated
with check (
  length(trim(nombre)) > 0
  and telefono ~ '^[67][0-9]{7}$'
  and length(trim(mensaje)) >= 10
);

drop policy if exists "crear reservas" on public.reservas;
create policy "crear reservas"
on public.reservas for insert
to anon, authenticated
with check (
  length(trim(nombre)) > 0
  and telefono ~ '^[67][0-9]{7}$'
  and personas between 1 and 50
);
