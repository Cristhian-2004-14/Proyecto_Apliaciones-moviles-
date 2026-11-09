# Diagnóstico del entorno

Fecha: 8 de noviembre de 2026.

## Hallazgos reales

- El comando `flutter` se encuentra en `C:\flutter\bin\flutter.bat`.
- Dart SDK respondió: `3.12.2 (stable)`.
- Existe la ruta `C:\Users\Usuario\AppData\Local\Android\Sdk`, pero el sandbox negó la enumeración de su contenido.
- No se detectó Android Studio en `C:\Program Files\Android\Android Studio`.
- No había proyecto, README, evidencias ni configuración Git dentro de la carpeta de actividad antes de esta intervención.

## Incidencia resuelta y estado actual

Flutter estaba bloqueado por archivos de bloqueo obsoletos en `C:\flutter\bin\cache` y procesos Git asociados. Tras liberar esos bloqueos, se pudo ejecutar el conjunto de herramientas directamente, generar Android, resolver dependencias, analizar y probar el proyecto.

El bloqueo restante es específico de Android: Flutter detecta Android SDK 36.1.0, pero no dispone de un JDK válido y no existe un AVD configurado. El detalle y los resultados reales están en `resultado_validaciones.md`.

## Acción mínima manual

1. Instalar o reparar un JDK 17 o superior y configurarlo con `flutter config --jdk-dir="RUTA_DEL_JDK"`.
2. Crear o iniciar un AVD en Android Studio y ejecutar `flutter run`.
3. Guardar una captura real de la app en esta carpeta.
