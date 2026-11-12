@echo off
setlocal
title Diagnostico de entorno Flutter

echo ================================================
echo   DIAGNOSTICO DE ENTORNO FLUTTER PARA ANDROID
echo ================================================
echo.

echo [1/6] Git
where git >nul 2>nul
if errorlevel 1 (
  echo [FALTA] Git no esta instalado o no esta en PATH.
) else (
  echo [OK] Git encontrado.
  git --version
)
echo.

echo [2/6] Java JDK
where java >nul 2>nul
if errorlevel 1 (
  echo [FALTA] Java JDK 17 no esta instalado o no esta en PATH.
) else (
  echo [OK] Java encontrado.
  java -version
)
echo.

echo [3/6] Flutter
where flutter >nul 2>nul
if errorlevel 1 (
  echo [FALTA] Flutter no esta instalado o no esta en PATH.
  echo Descarga: https://docs.flutter.dev/get-started/install/windows
) else (
  echo [OK] Flutter encontrado.
  flutter --version
)
echo.

echo [4/6] Android Studio
if exist "%ProgramFiles%\Android\Android Studio\bin\studio64.exe" (
  echo [OK] Android Studio encontrado.
) else (
  echo [FALTA] Android Studio no fue encontrado.
  echo Descarga: https://developer.android.com/studio
)
echo.

echo [5/6] Android SDK y ADB
if defined ANDROID_HOME (
  echo [INFO] ANDROID_HOME=%ANDROID_HOME%
)
if defined ANDROID_SDK_ROOT (
  echo [INFO] ANDROID_SDK_ROOT=%ANDROID_SDK_ROOT%
)
where adb >nul 2>nul
if errorlevel 1 (
  echo [AVISO] ADB no esta en PATH. Android Studio puede configurarlo.
) else (
  echo [OK] ADB encontrado.
  adb devices
)
echo.

echo [6/6] Diagnostico Flutter
where flutter >nul 2>nul
if errorlevel 1 (
  echo No se puede ejecutar flutter doctor porque Flutter no esta disponible.
) else (
  flutter doctor -v
)

echo.
echo ================================================
echo Copia toda esta salida y compartela si necesitas ayuda.
echo ================================================
pause
