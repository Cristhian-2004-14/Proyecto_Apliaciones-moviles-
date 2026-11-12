# Verificación de Supabase

Fecha de verificación: 11 de noviembre de 2026.

- Se crearon las tablas `negocios`, `consultas` y `reservas`.
- RLS quedó activo en las tres tablas.
- `negocios` permite lectura pública.
- `consultas` y `reservas` permiten únicamente inserciones públicas que cumplen las validaciones.
- Se cargaron siete elementos demostrativos en `negocios`.
- La consulta real por REST con la clave pública devolvió los siete elementos.
- Se insertaron una consulta y una reserva académicas de prueba para comprobar las políticas de escritura.

No se almacenan claves de Supabase en el repositorio.
