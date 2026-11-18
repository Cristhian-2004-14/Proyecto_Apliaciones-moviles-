# Traspaso: Laboratorios 12 y 13

Esta carpeta contiene la integración de servicios externos adaptada a
**Brasas del Oriente**.

## Laboratorio 12: API del clima

- `Clima.fromJson` convierte la respuesta de Open-Meteo en un modelo tipado.
- `ClimaService` usa HTTPS GET, límite de 10 segundos y manejo de errores.
- `ClimaCard` muestra carga, clima actual, error y reintento.
- No requiere clave privada.

## Laboratorio 13: contacto y mapa

- Botones Llamar, WhatsApp y Cómo llegar mediante `url_launcher`.
- Mapa integrado con OpenStreetMap y atribución visible.
- Consultas de Android para `tel`, `https` y `geo`.
- Coordenadas de Brasas del Oriente en `06_ubicacion.sql`.

## Integración recomendada

1. Copiar los archivos manteniendo sus rutas dentro del proyecto Flutter.
2. Ejecutar `flutter pub get` para instalar `http`, `flutter_map` y `latlong2`.
3. Ejecutar `supabase/06_ubicacion.sql` en Supabase SQL Editor.
4. Ejecutar la app con las variables públicas de Supabase.
5. Probar clima con y sin conexión, llamada, WhatsApp, ruta y mapa en teléfono real.

## No incluido

- Claves de Google Maps o de Supabase.
- Archivos de compilación.
- Envío de pedidos por WhatsApp: se agregará cuando el equipo decida integrarlo.
