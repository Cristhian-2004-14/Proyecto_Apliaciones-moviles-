# Brasas del Oriente — Aplicación móvil Flutter

Aplicación académica para la gestión básica de una churrasquería en Santa Cruz de la Sierra. Permite al cliente consultar el menú, crear pedidos, adjuntar comprobantes de pago, realizar reservas y revisar el estado de sus solicitudes. El dueño dispone de pantallas para verificar pagos, gestionar reservas y actualizar contenido del catálogo.

## Funcionalidades del MVP

- Catálogo con categorías, búsqueda por texto y voz, fotografías y carrito.
- Registro de pedidos y seguimiento en los estados en espera, confirmado o rechazado.
- Pago por QR configurable y envío de comprobantes JPG/PNG para revisión manual.
- Comparación de los datos disponibles del comprobante con monto, cuenta, beneficiario, fecha y operación esperados.
- Reserva de mesa y consulta del estado por parte del cliente.
- Gestión de reservas por parte del dueño: aceptar o denegar.
- Inicio de sesión, creación de cuenta y roles de cliente/dueño.
- Panel de dueño para fotos de productos, QR de pago y verificación de pagos.
- Consulta, ubicación, horarios, clima, mapa, llamada y WhatsApp.

## Requisitos funcionales implementados

- Material 3, tema centralizado y navegación entre pantallas.
- Catálogo filtrable con `ListView.builder` y tarjetas reutilizables.
- Formularios de consulta y reserva con validaciones.
- Integración con Supabase: datos remotos, RLS y scripts SQL.
- Carrito, creación de pedidos y detalle de productos mediante la función `crear_pedido`.
- Autenticación con cuentas de cliente y dueño; el dueño accede al panel de pedidos.
- Ubicación, clima de Santa Cruz con Open-Meteo, llamadas, WhatsApp, rutas y mapa OpenStreetMap.
- Pruebas de carrito, clima, navegación, validadores, estados de reserva y pagos.

- Actividad 4: fotos reales por producto en Supabase Storage, administración exclusiva del dueño y búsqueda por voz en el catálogo.
- Extra: QR bancario configurable, comprobantes privados, OCR local y constatación manual del dueño.

## Requisitos

- Flutter estable compatible con Dart 3.12 o superior.
- Android Studio con Android SDK y Java 17.
- Emulador Android o teléfono físico con depuración USB.
- Proyecto de Supabase configurado.

Compruebe el entorno con:

```powershell
flutter doctor
```

## Instalación y ejecución

```powershell
git clone https://github.com/Cristhian-2004-14/Proyecto_Apliaciones-moviles-.git
cd Proyecto_Apliaciones-moviles-
flutter pub get
```

Primero ejecuta en Supabase, desde SQL Editor, los scripts de la carpeta `supabase/` en el orden indicado en su README. Para contar con pedidos, cuentas, clima y ubicación ejecuta también `04_pedidos.sql`, `05_cuentas_roles.sql` y `06_ubicacion.sql`. Para Actividad 4 ejecuta después `07_storage_negocio.sql` y `09_fotos_productos.sql`. Para el extra de pagos QR, finalmente ejecuta `08_pagos_qr.sql` y `10_historial_cliente_y_gestion_reservas.sql`. Luego ejecuta:

```powershell
flutter pub get
dart format lib test
flutter analyze
flutter test
flutter run --dart-define=SUPABASE_URL=https://TU_PROYECTO.supabase.co --dart-define=SUPABASE_PUBLISHABLE_KEY=TU_CLAVE_PUBLICA
```

La clave pública se entrega al comando; no se guarda en el proyecto. Nunca uses una clave secreta o `service_role` en Flutter ni la subas a GitHub. Para el detalle de réplica consulte [documentación técnica/README_replicacion.md](documentaci%C3%B3n%20t%C3%A9cnica/README_replicacion.md).

## Pruebas automáticas

Antes de las pruebas manuales, ejecuta este comando desde PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\herramientas\ejecutar_pruebas.ps1
```

El script ejecuta `flutter analyze` para detectar errores estáticos y `flutter test` para validar el carrito, el clima, los validadores, los estados de reservas, pagos y QR. También comprueba que el carrito elimine correctamente su última unidad, que un estado de reserva no reconocido se trate como "En espera", que un pedido sin pago se maneje correctamente y que las validaciones rechacen formularios incompletos. No requiere Supabase ni modifica los datos reales.

## QR y comprobantes

El dueño inicia sesión y usa **Mi cuenta → Configurar QR de pagos** para cargar una imagen QR real y autorizada, además de los datos de validación del beneficiario. Esos datos se almacenan en Supabase y no están escritos en el código. El cliente debe iniciar sesión para asociar su comprobante privado con el pedido. El OCR funciona localmente en Android como apoyo documental; únicamente el dueño puede constatar un abono real y cambiar un pago a `PAGADO`.

## Diagnóstico en otra computadora

Ejecuta `herramientas\verificar_entorno_flutter.bat` con doble clic o desde CMD. No instala ni modifica nada: informa si faltan Git, Java, Flutter, Android Studio o un emulador.

## Estructura y documentos

- Código Flutter: `lib/`
- Pruebas: `test/`
- Scripts SQL: `supabase/`
- Guías técnicas y manuales: `documentación técnica/`
- Cambios y procedimiento de pruebas: `CAMBIOS_Y_PRUEBAS.md`
- Entregables finales: `entregables/Documentacion_Final_Consolidada/`
- Presentación final del video de Actividad 3: `entregables/Presentacion_video_Brasas_del_Oriente_Actividad_3_mejorada_final.pptx`

## Documentos finales incluidos

- `01_Protocolo_UAT_y_Acta_de_Conformidad.docx`: flujo completo de aceptación y firma.
- `02_Pruebas_y_Evidencias_MVP.docx`: casos de prueba y registro de evidencias.
- `03_Informe_Final_Brasas_del_Oriente_APA7.docx`: informe final en APA 7, con primera hoja en blanco, índice automático y anexos.

## Seguridad

No incluya en GitHub contraseñas, claves secretas de Supabase, `service_role`, comprobantes reales, números de cuenta ni datos personales. La configuración de Supabase se inyecta únicamente en tiempo de ejecución mediante `--dart-define`.
