@echo off
setlocal EnableExtensions
title Instalador de requisitos Flutter

echo ================================================
echo  INSTALADOR DE REQUISITOS PARA FLUTTER Y ANDROID
echo ================================================
echo Este script instala Git, Java 17 y Flutter.
echo Android Studio debe instalarse por separado y completar su asistente.
echo.

where winget >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Winget no esta disponible en esta computadora.
  echo Actualiza App Installer desde Microsoft Store e intentalo de nuevo.
  pause
  exit /b 1
)

where git >nul 2>nul
if errorlevel 1 (
  echo [INSTALANDO] Git...
  winget install --id Git.Git --exact --accept-package-agreements --accept-source-agreements
) else (
  echo [OK] Git ya esta instalado.
)

where java >nul 2>nul
if errorlevel 1 (
  echo [INSTALANDO] Eclipse Temurin JDK 17...
  winget install --id EclipseAdoptium.Temurin.17.JDK --exact --accept-package-agreements --accept-source-agreements
) else (
  echo [OK] Java ya esta instalado.
)

set "FLUTTER_HOME=%USERPROFILE%\development\flutter"
if exist "%FLUTTER_HOME%\bin\flutter.bat" (
  echo [OK] Flutter ya esta instalado en %FLUTTER_HOME%
) else (
  echo [DESCARGANDO] Flutter SDK 3.44.2 estable. Esto puede tardar varios minutos...
  if not exist "%USERPROFILE%\development" mkdir "%USERPROFILE%\development"
  curl.exe -L --retry 5 --retry-delay 5 --connect-timeout 30 -o "%TEMP%\flutter_sdk.zip" "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.44.2-stable.zip"
  if errorlevel 1 (
    echo [ERROR] La descarga de Flutter fallo despues de varios intentos.
    echo Verifica tu conexion e intenta ejecutar el script nuevamente.
    pause
    exit /b 1
  )
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%TEMP%\flutter_sdk.zip' -DestinationPath '%USERPROFILE%\development' -Force"
  if not exist "%FLUTTER_HOME%\bin\flutter.bat" (
    echo [ERROR] No se pudo descargar o extraer Flutter.
    pause
    exit /b 1
  )
)

set "PATH=%FLUTTER_HOME%\bin;%PATH%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p=[Environment]::GetEnvironmentVariable('Path','User'); if ($p -notlike '*development\flutter\bin*') {[Environment]::SetEnvironmentVariable('Path', $p + ';%USERPROFILE%\development\flutter\bin', 'User')}"

for /d %%J in ("%ProgramFiles%\Eclipse Adoptium\jdk-17*") do set "JDK_HOME=%%~fJ"
if defined JDK_HOME (
  echo [CONFIGURANDO] Flutter con Java 17...
  call "%FLUTTER_HOME%\bin\flutter.bat" config --jdk-dir="%JDK_HOME%"
)

echo.
echo ================================================
echo Flutter fue instalado en: %FLUTTER_HOME%
echo Cierra esta ventana, abre una NUEVA consola CMD y ejecuta:
echo flutter doctor -v
echo.
echo Luego abre Android Studio, completa el asistente y crea un emulador.
echo ================================================
pause
