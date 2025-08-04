#!/bin/bash
# Build script para Vercel - Sistema de Inventario Django

echo "🚀 Iniciando build completo para Vercel..."

# Configurar variables de entorno
export VERCEL=1
export DJANGO_SETTINGS_MODULE=SistemaInventario.settings

# Instalar dependencias
echo "📦 Instalando dependencias Python..."
pip install -r requirements.txt

echo "📁 Creando directorios necesarios..."
mkdir -p staticfiles
mkdir -p media
mkdir -p /tmp

# Ejecutar migraciones
echo "🗃️ Ejecutando migraciones de Django..."
python manage.py migrate --noinput

# Crear superusuario si no existe
echo "👤 Configurando superusuario demo..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SistemaInventario.settings')
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@demo.com', 'admin123')
    print('✅ Superusuario admin creado')
else:
    print('✅ Superusuario admin ya existe')
"

# Collectstatic para archivos estáticos
echo "🎨 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Build completado exitosamente!"
echo "🌐 Aplicación lista para deployment en Vercel"

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "¡Configuración completada!"
