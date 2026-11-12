@echo off
setlocal EnableExtensions
title Instalacion rapida de Flutter

set "FLUTTER_HOME=%USERPROFILE%\development\flutter"
set "ZIP=%TEMP%\flutter_sdk.zip"

echo ================================================
echo  INSTALACION RAPIDA DE FLUTTER
echo ================================================

if exist "%FLUTTER_HOME%\bin\flutter.bat" (
  echo [OK] Flutter ya esta extraido en %FLUTTER_HOME%
  goto configurar
)

if not exist "%ZIP%" (
  echo [ERROR] No se encontro flutter_sdk.zip en %TEMP%.
  echo Ejecuta primero instalar_requisitos_flutter_intento_dos.bat
  pause
  exit /b 1
)

if not exist "%USERPROFILE%\development" mkdir "%USERPROFILE%\development"
echo [EXTRAYENDO] Flutter con la herramienta nativa de Windows...
tar -xf "%ZIP%" -C "%USERPROFILE%\development"
if errorlevel 1 (
  echo [ERROR] La extraccion fallo. No borres el archivo ZIP.
  pause
  exit /b 1
)

:configurar
set "PATH=%FLUTTER_HOME%\bin;%PATH%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p=[Environment]::GetEnvironmentVariable('Path','User'); if ($p -notlike '*development\flutter\bin*') {[Environment]::SetEnvironmentVariable('Path', $p + ';%USERPROFILE%\development\flutter\bin', 'User')}"
for /d %%J in ("%ProgramFiles%\Eclipse Adoptium\jdk-17*") do set "JDK_HOME=%%~fJ"
if defined JDK_HOME call "%FLUTTER_HOME%\bin\flutter.bat" config --jdk-dir="%JDK_HOME%"

echo.
echo [LISTO] Flutter se instalo en %FLUTTER_HOME%
echo Cierra esta ventana, abre una CMD nueva y ejecuta: flutter doctor -v
pause
