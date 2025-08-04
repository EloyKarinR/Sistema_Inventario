@echo off
REM Script para instalar solo archivos necesarios para desarrollo local

echo 🧹 Instalación Limpia - Solo Desarrollo Local
echo Este script eliminará archivos específicos de Vercel deployment
echo.

set /p confirm="¿Continuar? (y/N): "
if /i not "%confirm%"=="y" (
    echo ❌ Cancelado
    pause
    exit /b 1
)

echo 🗑️ Eliminando archivos de Vercel...

REM Eliminar archivos de Vercel
if exist vercel.json del vercel.json
if exist requirements-vercel.txt del requirements-vercel.txt
if exist .vercelignore del .vercelignore
if exist Procfile del Procfile
if exist runtime.txt del runtime.txt
if exist Aptfile del Aptfile

REM Eliminar directorio api
if exist api rmdir /s /q api

REM Eliminar template específico de Vercel
if exist Inventario\templates\Inventario\bienvenida_vercel.html del Inventario\templates\Inventario\bienvenida_vercel.html

echo ✅ Archivos de Vercel eliminados
echo.
echo 📦 Archivos restantes son solo para desarrollo local:
echo    ✅ Django proyecto completo
echo    ✅ Requirements.txt para local
echo    ✅ Scripts de setup automático
echo    ✅ Documentación
echo.
echo 🚀 Ahora ejecuta: setup-local.bat
echo.
pause
