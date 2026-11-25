$ErrorActionPreference = 'Stop'

Write-Host '1/2 Analizando código Flutter...' -ForegroundColor Cyan
flutter analyze

Write-Host '2/2 Ejecutando pruebas automáticas...' -ForegroundColor Cyan
flutter test

Write-Host 'Pruebas finalizadas sin errores.' -ForegroundColor Green
