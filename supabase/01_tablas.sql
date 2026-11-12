-- Esquema propio de Brasas del Oriente. No corresponde al esquema original del taller.

create table if not exists public.negocios (
  id bigint generated always as identity primary key,
  nombre text not null,
  rubro text not null,
  descripcion text not null,
  telefono text not null check (telefono ~ '^[67][0-9]{7}$'),
  precio numeric(10,2) not null check (precio >= 0),
  created_at timestamptz not null default now()
);

create table if not exists public.consultas (
  id bigint generated always as identity primary key,
  nombre text not null check (length(trim(nombre)) > 0),
  telefono text not null check (telefono ~ '^[67][0-9]{7}$'),
  mensaje text not null check (length(trim(mensaje)) >= 10),
  created_at timestamptz not null default now()
);

create table if not exists public.reservas (
  id bigint generated always as identity primary key,
  nombre text not null check (length(trim(nombre)) > 0),
  telefono text not null check (telefono ~ '^[67][0-9]{7}$'),
  fecha date not null,
  hora time not null,
  personas integer not null check (personas between 1 and 50),
  created_at timestamptz not null default now()
);

create or replace function public.validar_reserva_futura()
returns trigger
language plpgsql
as $$
begin
  if (new.fecha + new.hora) <= (now() at time zone 'America/La_Paz') then
    raise exception 'La fecha y hora de la reserva deben ser futuras';
  end if;
  return new;
end;
$$;

drop trigger if exists validar_reserva_futura_trigger on public.reservas;
create trigger validar_reserva_futura_trigger
before insert or update on public.reservas
for each row execute function public.validar_reserva_futura();
