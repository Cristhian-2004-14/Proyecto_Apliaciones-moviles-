# Guía de replicación en otra computadora

Esta guía permite preparar una computadora nueva para ejecutar **Brasas del Oriente**. La aplicación se desarrolló con Flutter para Android y utiliza Supabase como backend.

## 1. Requisitos

- Git.
- Flutter canal `stable` compatible con Dart `3.12` o superior.
- Android Studio con Android SDK, Platform Tools, emulador o teléfono físico.
- Java 17.
- Una cuenta y un proyecto en Supabase.
- Internet para descargar dependencias, conectarse a Supabase, consultar el clima y cargar mapas.

Verifica el entorno con:

```powershell
flutter doctor
```

## 2. Obtener el proyecto

```powershell
git clone URL_DEL_REPOSITORIO
cd actividad_1
flutter pub get
```

Si recibiste el proyecto como carpeta comprimida, descomprímelo y ejecuta los dos últimos comandos dentro de la carpeta raíz.

## 3. Configurar Supabase

1. Crea un proyecto en [Supabase](https://supabase.com/).
2. En **SQL Editor**, ejecuta los scripts de la carpeta `supabase/` en el orden indicado por el README principal.
3. Para el MVP, asegúrate de ejecutar los scripts de pedidos, cuentas, ubicación, Storage y fotos de productos.
4. Crea las cuentas necesarias y asigna el rol Dueño a la cuenta administradora según el script de roles.
5. Copia la URL del proyecto y la **Publishable key**. No uses `service_role` en Flutter.

## 4. Ejecutar en emulador o teléfono

Con un emulador iniciado o un teléfono conectado con depuración USB:

```powershell
flutter run --dart-define=SUPABASE_URL=https://TU_PROYECTO.supabase.co --dart-define=SUPABASE_PUBLISHABLE_KEY=TU_CLAVE_PUBLICA
```

La URL y la clave pública se entregan por comando para evitar guardarlas en el repositorio.

## 5. Comandos de calidad

```powershell
dart format lib test
flutter analyze
flutter test
```

También puedes ejecutar el script incluido:

```powershell
powershell -ExecutionPolicy Bypass -File .\herramientas\ejecutar_pruebas.ps1
```

## 6. Crear una APK para pruebas

```powershell
flutter build apk --debug --dart-define=SUPABASE_URL=https://TU_PROYECTO.supabase.co --dart-define=SUPABASE_PUBLISHABLE_KEY=TU_CLAVE_PUBLICA
```

La salida se encuentra en:

```text
build\app\outputs\flutter-apk\app-debug.apk
```

Pasa ese archivo a un teléfono Android e instala la APK autorizando instalaciones desde la fuente elegida.

## 7. Estructura relevante

```text
lib/           Código Flutter: páginas, servicios y modelos
test/          Pruebas automatizadas
supabase/      Scripts SQL, RLS, Storage y funciones RPC
herramientas/  Scripts auxiliares de diagnóstico y pruebas
documentación técnica/  Manuales del proyecto
```

## 8. Solución rápida de problemas

| Situación | Acción |
| --- | --- |
| La app indica que Supabase no está configurado | Inicia con ambos `--dart-define` y revisa URL/clave pública. |
| No se descargan paquetes | Comprueba Internet y ejecuta `flutter pub get`. |
| El teléfono no aparece | Activa Depuración USB, autoriza el equipo y ejecuta `flutter devices`. |
| Fallan fotos o Storage | Comprueba los buckets y políticas de Storage definidos en los scripts SQL. |
| No funciona voz | Acepta el permiso de micrófono y verifica que el dispositivo tenga reconocimiento de voz disponible. |

## Seguridad

No subas a GitHub secretos, contraseñas, claves `service_role`, datos bancarios ni archivos de configuración locales. La clave publishable es la única clave de Supabase que usa la aplicación cliente.
