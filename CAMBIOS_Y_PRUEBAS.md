# Cambios y pruebas realizadas

## Versión final del MVP

Esta versión consolida el MVP de **Brasas del Oriente**, una aplicación Flutter para pedidos, reservas y gestión básica de una churrasquería.

### Cambios funcionales principales

- Catálogo con categorías, búsqueda escrita y búsqueda por voz.
- Carrito, confirmación y registro de pedidos.
- Historial del cliente con los estados **en espera**, **confirmado** y **rechazado**.
- Reserva de mesa, consulta posterior de su estado y panel del dueño para aceptarla o denegarla.
- Registro de comprobantes de pago mediante imagen JPG o PNG.
- Revisión manual de pagos para el dueño con comparación entre importe, cuenta destino, beneficiario, fecha y operación detectada.
- Administración de fotos del catálogo y QR de pago desde la cuenta del dueño.
- Formularios de consultas, ubicación, horarios, mapa, llamadas y acceso a WhatsApp.

### Cambios técnicos principales

- Integración con Supabase Auth, PostgreSQL, Storage y políticas RLS.
- Scripts SQL para pedidos, roles, Storage, fotos, pagos, historial y sincronización de estados.
- Corrección del historial para consultar los estados de pedido y pago sin depender de un campo inexistente.
- Corrección de actualización asíncrona de estado en la pantalla de pedidos y reservas.
- Pruebas unitarias para validación, flujo de carrito y estados de historial.

## Ejecutar las pruebas

Desde la raíz del proyecto:

```powershell
flutter pub get
dart format lib test
flutter analyze
flutter test
```

O utiliza el script de apoyo:

```powershell
powershell -ExecutionPolicy Bypass -File .\herramientas\ejecutar_pruebas.ps1
```

Las pruebas automáticas no requieren credenciales y no modifican la base de datos. Para la validación integral con Supabase, siga el protocolo UAT disponible en `entregables/Documentacion_Final_Consolidada/`.

## Prueba manual mínima

1. Inicie la aplicación con la URL y la publishable key de Supabase.
2. Cree o inicie sesión con una cuenta cliente.
3. Agregue productos, confirme un pedido y adjunte un comprobante de prueba.
4. Revise en **Mis pedidos y reservas** el estado del pedido.
5. Cree una reserva y compruebe que aparece inicialmente en espera.
6. Inicie sesión como dueño, gestione la reserva y revise el pago.
7. Vuelva a ingresar como cliente y confirme que los cambios de estado se reflejan.

## Documentación disponible

- `documentación técnica/README_replicacion.md`: instalación y réplica en otra computadora.
- `documentación técnica/Manual_de_uso_MVP.docx`: recorrido para cliente y dueño.
- `documentación técnica/Guia_de_desarrollo_y_despliegue.docx`: requisitos técnicos y despliegue.
- `documentación técnica/Historias_de_usuario_MVP.md`: alcance mínimo del producto.
- `entregables/Documentacion_Final_Consolidada/`: protocolo UAT, pruebas y evidencia, e informe final en APA 7.
