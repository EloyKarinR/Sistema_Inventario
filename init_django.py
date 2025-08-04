#!/usr/bin/env python
"""
Script de inicialización para Django en Vercel
Ejecuta migraciones y crea superusuario automáticamente
"""
import os
import sys
import django
from pathlib import Path

# Configurar el entorno
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SistemaInventario.settings')
os.environ['VERCEL'] = '1'

def main():
    """Función principal de inicialización"""
    try:
        print("🚀 Iniciando configuración Django para Vercel...")
        
        # Configurar Django
        django.setup()
        
        from django.core.management import execute_from_command_line
        from django.contrib.auth.models import User
        
        print("📋 Ejecutando migraciones...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        print("👤 Creando superusuario...")
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@demo.com', 'admin123')
            print("✅ Superusuario 'admin' creado exitosamente")
        else:
            print("✅ Superusuario 'admin' ya existe")
            
        print("🎉 Inicialización completada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en inicialización: {e}")
        return False

if __name__ == '__main__':
    main()
