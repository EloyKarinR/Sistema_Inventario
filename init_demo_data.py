#!/usr/bin/env python
"""
Script de inicialización para crear datos de prueba en Vercel
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SistemaInventario.settings')
django.setup()

from django.contrib.auth.models import User
from Inventario.models import Fabricante, Producto, Cliente, Proveedor

def crear_datos_demo():
    """Crear datos de demostración para la aplicación"""
    
    # Crear superusuario si no existe
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@demo.com', 'admin123')
        print("✅ Superusuario 'admin' creado")
    
    # Crear fabricante de ejemplo
    if not Fabricante.objects.exists():
        fabricante = Fabricante.objects.create(
            nombre="Demo Tech",
            descripcion="Fabricante de demostración"
        )
        print("✅ Fabricante demo creado")
    else:
        fabricante = Fabricante.objects.first()
    
    # Crear producto de ejemplo
    if not Producto.objects.exists():
        Producto.objects.create(
            codigo="DEMO001",
            nombre="Producto Demo",
            descripcion="Producto de demostración para Vercel",
            precio_compra=100.00,
            precio_venta=150.00,
            stock=10,
            fabricante=fabricante
        )
        print("✅ Producto demo creado")
    
    # Crear cliente de ejemplo
    if not Cliente.objects.exists():
        Cliente.objects.create(
            nombre="Cliente Demo",
            email="cliente@demo.com",
            telefono="123456789",
            direccion="Dirección de demostración"
        )
        print("✅ Cliente demo creado")
    
    # Crear proveedor de ejemplo
    if not Proveedor.objects.exists():
        Proveedor.objects.create(
            nombre="Proveedor Demo",
            email="proveedor@demo.com",
            telefono="987654321",
            direccion="Dirección del proveedor demo"
        )
        print("✅ Proveedor demo creado")
    
    print("🎉 ¡Datos de demostración creados exitosamente!")

if __name__ == '__main__':
    crear_datos_demo()
