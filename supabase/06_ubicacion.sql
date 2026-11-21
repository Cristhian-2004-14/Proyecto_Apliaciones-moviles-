-- Laboratorio 13: coordenadas para la ubicación del negocio.
-- El catálogo actual usa la tabla negocios para los productos del menú.
-- Por fines del taller, cada registro toma las coordenadas de Brasas del Oriente.

alter table public.negocios
add column if not exists latitud double precision,
add column if not exists longitud double precision;

update public.negocios
set latitud = -17.7833,
    longitud = -63.1821
where latitud is null or longitud is null;
