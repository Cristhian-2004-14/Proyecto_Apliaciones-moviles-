# ConectaCruz

Actividad de Aplicaciones Móviles I. El proyecto implementa una primera pantalla Flutter para un catálogo de churrasquería en Santa Cruz de la Sierra.

## Requisitos funcionales implementados

- `MaterialApp` y `Scaffold`.
- Título visible **ConectaCruz**.
- Botón exacto **Ver negocios**.
- Navegación a un catálogo breve de negocios destacados.
- Prueba de widget para la navegación.

No se incluyen pedidos, reservas, autenticación ni backend.

## Ejecución

Desde esta carpeta, cuando Flutter no esté bloqueado:

```powershell
flutter create --platforms=android .
flutter pub get
dart format lib test
flutter analyze
flutter test
flutter doctor -v
flutter devices
flutter emulators
flutter run
```

## Entregables

- Código: `lib/main.dart`
- Prueba: `test/widget_test.dart`
- Informe IMRyD editable: `informe/informe_imryd.md`
- Informe IMRyD PDF: `informe/informe_imryd.pdf`
- Presentación de seis diapositivas: `presentacion/presentacion_defensa.html`
- Guion de defensa: `presentacion/guion_defensa.md`
- Diagnóstico de entorno: `evidencias/diagnostico_entorno.md`

## Estado de evidencias

La carpeta empezó vacía. El análisis y la prueba automatizada se ejecutaron correctamente. Sigue pendiente la captura real en Android porque no hay un emulador configurado y el JDK detectado por Flutter no es válido. Los resultados están en `evidencias/resultado_validaciones.md`.
