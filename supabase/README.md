# Supabase de Brasas del Oriente

Ejecuta los scripts en este orden desde el SQL Editor de Supabase:

1. `01_tablas.sql`
2. `02_rls_lectura.sql`
3. `02b_datos_semilla.sql`
4. `03_escritura_publica.sql`
5. `04_pedidos.sql`
6. `05_cuentas_roles.sql`
7. `06_ubicacion.sql`
8. `07_storage_negocio.sql`
9. `09_fotos_productos.sql`
10. `08_pagos_qr.sql` (extra opcional)

Este esquema fue diseñado para este proyecto; no afirma ser el esquema original del taller. Las tablas `consultas` y `reservas` aceptan inserciones públicas, pero no lecturas públicas. Nunca agregues claves secretas a este repositorio.
