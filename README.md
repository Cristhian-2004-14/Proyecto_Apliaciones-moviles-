# ConectaCruz — Brasas del Oriente

Actividad de Aplicaciones Móviles I. Aplicación Flutter para el catálogo, consultas, reservas y pedidos de la churrasquería Brasas del Oriente en Santa Cruz de la Sierra.

## Requisitos funcionales implementados

- Material 3, tema centralizado y navegación entre pantallas.
- Catálogo filtrable con `ListView.builder` y tarjetas reutilizables.
- Formularios de consulta y reserva con validaciones.
- Integración con Supabase: datos remotos, RLS y scripts SQL.
- Carrito, creación de pedidos y detalle de productos mediante la función `crear_pedido`.
- Autenticación con cuentas de cliente y dueño; el dueño accede al panel de pedidos.
- Ubicación, clima de Santa Cruz con Open-Meteo, llamadas, WhatsApp, rutas y mapa OpenStreetMap.
- Pruebas de carrito, clima, navegación y validadores.

- Actividad 4: foto de portada en Supabase Storage, actualización exclusiva del dueño y búsqueda por voz en el catálogo.

## Ejecución

Primero ejecuta en Supabase, desde SQL Editor, los scripts de la carpeta `supabase/` en el orden indicado en su README. Para contar con pedidos, cuentas, clima y ubicación ejecuta también `04_pedidos.sql`, `05_cuentas_roles.sql` y `06_ubicacion.sql`. Para Actividad 4 ejecuta después `07_storage_negocio.sql`. Luego ejecuta:

```powershell
flutter pub get
dart format lib test
flutter analyze
flutter test
flutter run --dart-define=SUPABASE_URL=https://TU_PROYECTO.supabase.co --dart-define=SUPABASE_PUBLISHABLE_KEY=TU_CLAVE_PUBLICA
```

La clave pública se entrega al comando; no se guarda en el proyecto. Nunca uses una clave secreta o `service_role` en Flutter ni la subas a GitHub.

## Diagnóstico en otra computadora

Ejecuta `herramientas\verificar_entorno_flutter.bat` con doble clic o desde CMD. No instala ni modifica nada: informa si faltan Git, Java, Flutter, Android Studio o un emulador.

## Entregables

- Código Flutter: `lib/`
- Pruebas: `test/`
- Scripts SQL: `supabase/`
- Evidencias: `evidencias/`
- Presentación final del video de Actividad 3: `entregables/Presentacion_video_Brasas_del_Oriente_Actividad_3_mejorada_final.pptx`

## Estado de evidencias

La conexión real, la ejecución de scripts SQL y las capturas de Supabase deben verificarse antes de entregar.
