#!/bin/bash
# Setup script para desarrollo local

echo "🚀 Configurando Sistema de Inventario para desarrollo local..."

# Verificar si Python está instalado
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python no está instalado"
    exit 1
fi

echo "✅ Python encontrado: $(python --version)"

# Crear entorno virtual si no existe
if [ ! -d "env" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv env
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash, MSYS2, Cygwin)
    source env/Scripts/activate
else
    # Linux/Mac
    source env/bin/activate
fi

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Crear estructura de directorios
echo "📁 Creando directorios necesarios..."
mkdir -p media/productos
mkdir -p media/empresa
mkdir -p media/profile_pics

# Ejecutar migraciones
echo "🔧 Configurando base de datos..."
python manage.py makemigrations
python manage.py migrate

# Recopilar archivos estáticos
echo "🎨 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo ""
echo "✅ ¡Configuración completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Crear superusuario: python manage.py createsuperuser"
echo "2. Iniciar servidor: python manage.py runserver"
echo "3. Abrir navegador: http://localhost:8000"
echo ""
echo "🎯 Para administración: http://localhost:8000/admin/"
