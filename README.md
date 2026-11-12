# ConectaCruz

Actividad de Aplicaciones Móviles I. Aplicación Flutter para el catálogo, consultas y reservas de la churrasquería Brasas del Oriente en Santa Cruz de la Sierra.

## Requisitos funcionales implementados

- Material 3, tema centralizado y navegación entre pantallas.
- Catálogo filtrable con `ListView.builder` y tarjetas reutilizables.
- Formularios de consulta y reserva con validaciones.
- Integración preparada para Supabase: datos remotos, RLS y scripts SQL.
- Pruebas de navegación y validadores.

No se incluyen pagos, autenticación ni pedidos.

## Ejecución

Primero ejecuta en Supabase, desde SQL Editor, los scripts de la carpeta `supabase/` en el orden indicado en su README. Luego ejecuta:

```powershell
flutter pub get
dart format lib test
flutter analyze
flutter test
flutter run --dart-define=SUPABASE_URL=https://xsvuuxvwwfyhazofuull.supabase.co --dart-define=SUPABASE_PUBLISHABLE_KEY=TU_CLAVE_PUBLICA
```

La clave pública se entrega al comando; no se guarda en el proyecto. Nunca uses una clave secreta o `service_role` en Flutter ni la subas a GitHub.

## Diagnóstico en otra computadora

Ejecuta `herramientas\verificar_entorno_flutter.bat` con doble clic o desde CMD. No instala ni modifica nada: informa si faltan Git, Java, Flutter, Android Studio o un emulador.

## Entregables

- Código Flutter: `lib/`
- Pruebas: `test/`
- Scripts SQL: `supabase/`
- Evidencias: `evidencias/`

## Estado de evidencias

La conexión real, la ejecución de scripts SQL y las capturas de Supabase deben verificarse antes de entregar.
