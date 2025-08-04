@echo off
REM Setup script para desarrollo local en Windows

echo 🚀 Configurando Sistema de Inventario para desarrollo local...

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Crear entorno virtual si no existe
if not exist "env" (
    echo 📦 Creando entorno virtual...
    python -m venv env
)

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call env\Scripts\activate.bat

REM Instalar dependencias
echo 📚 Instalando dependencias...
pip install -r requirements.txt

REM Crear estructura de directorios
echo 📁 Creando directorios necesarios...
if not exist "media" mkdir media
if not exist "media\productos" mkdir media\productos
if not exist "media\empresa" mkdir media\empresa
if not exist "media\profile_pics" mkdir media\profile_pics

REM Ejecutar migraciones
echo 🔧 Configurando base de datos...
python manage.py makemigrations
python manage.py migrate

REM Recopilar archivos estáticos
echo 🎨 Recopilando archivos estáticos...
python manage.py collectstatic --noinput

echo.
echo ✅ ¡Configuración completada!
echo.
echo 📋 Próximos pasos:
echo 1. Crear superusuario: python manage.py createsuperuser
echo 2. Iniciar servidor: python manage.py runserver
echo 3. Abrir navegador: http://localhost:8000
echo.
echo 🎯 Para administración: http://localhost:8000/admin/
echo.
pause
