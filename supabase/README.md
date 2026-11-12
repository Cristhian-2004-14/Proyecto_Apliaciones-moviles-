# Supabase de Brasas del Oriente

Ejecuta los scripts en este orden desde el SQL Editor de Supabase:

1. `01_tablas.sql`
2. `02_rls_lectura.sql`
3. `02b_datos_semilla.sql`
4. `03_escritura_publica.sql`

Este esquema fue diseñado para este proyecto; no afirma ser el esquema original del taller. Las tablas `consultas` y `reservas` aceptan inserciones públicas, pero no lecturas públicas. Nunca agregues claves secretas a este repositorio.
