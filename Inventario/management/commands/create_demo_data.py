from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Inventario.models import Producto, Cliente, Venta, DetalleVenta, Profile
from django.utils import timezone
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Crear datos de demostración para el sistema'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Creando datos de demostración...')
        
        # 1. Crear usuario demo
        self.create_demo_user()
        
        # 2. Crear productos de ejemplo
        self.create_sample_products()
        
        # 3. Crear clientes de ejemplo
        self.create_sample_clients()
        
        # 4. Crear ventas de ejemplo
        self.create_sample_sales()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Datos de demostración creados exitosamente!')
        )

    def create_demo_user(self):
        """Crear usuario demo con restricciones"""
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@sistema-inventario.com',
                'first_name': 'Usuario',
                'last_name': 'Demo',
                'is_staff': False,
                'is_superuser': False
            }
        )
        user.set_password('demo123')
        user.save()
        
        # Crear perfil si no existe
        profile, created = Profile.objects.get_or_create(
            user=user
        )
        
        if created:
            self.stdout.write('👤 Usuario demo creado')
        else:
            self.stdout.write('👤 Usuario demo ya existe')

    def create_sample_products(self):
        """Crear productos de ejemplo"""
        productos_ejemplo = [
            {
                'codigo': 'DEMO001',
                'nombre': 'Laptop Dell Inspiron 15',
                'descripcion': 'Laptop para uso profesional con 8GB RAM y 256GB SSD',
                'fabricante': 'Dell',
                'stock': 25,
                'precio': Decimal('850.00'),
                'categoria': 'Computadoras',
                'estado': 'Activo'
            },
            {
                'codigo': 'DEMO002', 
                'nombre': 'Mouse Inalámbrico Logitech',
                'descripcion': 'Mouse inalámbrico ergonómico con batería de larga duración',
                'fabricante': 'Logitech',
                'stock': 50,
                'precio': Decimal('25.99'),
                'categoria': 'Accesorios',
                'estado': 'Activo'
            },
            {
                'codigo': 'DEMO003',
                'nombre': 'Monitor Samsung 24"',
                'descripcion': 'Monitor Full HD 24 pulgadas para oficina',
                'fabricante': 'Samsung',
                'stock': 15,
                'precio': Decimal('180.00'),
                'categoria': 'Monitores',
                'estado': 'Activo'
            },
            {
                'codigo': 'DEMO004',
                'nombre': 'Teclado Mecánico RGB',
                'descripcion': 'Teclado mecánico gaming con iluminación RGB',
                'fabricante': 'Corsair',
                'stock': 30,
                'precio': Decimal('120.50'),
                'categoria': 'Accesorios',
                'estado': 'Activo'
            },
            {
                'codigo': 'DEMO005',
                'nombre': 'Impresora HP LaserJet',
                'descripcion': 'Impresora láser monocromática para oficina',
                'fabricante': 'HP',
                'stock': 8,
                'precio': Decimal('295.00'),
                'categoria': 'Impresoras',
                'estado': 'Activo'
            }
        ]
        
        for producto_data in productos_ejemplo:
            producto, created = Producto.objects.get_or_create(
                codigo=producto_data['codigo'],
                defaults=producto_data
            )
            if created:
                self.stdout.write(f'📦 Producto creado: {producto.nombre}')

    def create_sample_clients(self):
        """Crear clientes de ejemplo"""
        clientes_ejemplo = [
            {
                'nombre': 'TechCorp Solutions',
                'rut_nit': '900123456-7',
                'telefono': '+57 1 234 5678',
                'email': 'contacto@techcorp.com',
                'direccion': 'Av. Empresarial 123, Bogotá',
                'tipo': 'Juridico'
            },
            {
                'nombre': 'María González',
                'rut_nit': '12345678-9',
                'telefono': '+57 300 987 6543',
                'email': 'maria.gonzalez@email.com',
                'direccion': 'Calle 45 #12-34, Medellín',
                'tipo': 'Natural'
            },
            {
                'nombre': 'Innovate LLC',
                'rut_nit': '800987654-3',
                'telefono': '+57 2 876 5432',
                'email': 'ventas@innovate.com',
                'direccion': 'Carrera 15 #89-12, Cali',
                'tipo': 'Juridico'
            }
        ]
        
        for cliente_data in clientes_ejemplo:
            cliente, created = Cliente.objects.get_or_create(
                rut_nit=cliente_data['rut_nit'],
                defaults=cliente_data
            )
            if created:
                self.stdout.write(f'👥 Cliente creado: {cliente.nombre}')

    def create_sample_sales(self):
        """Crear ventas de ejemplo"""
        if not Producto.objects.exists() or not Cliente.objects.exists():
            self.stdout.write('⚠️ No hay productos o clientes para crear ventas')
            return
            
        productos = list(Producto.objects.all())
        clientes = list(Cliente.objects.all())
        
        # Crear 5 ventas de ejemplo
        for i in range(5):
            cliente = random.choice(clientes)
            
            venta = Venta.objects.create(
                numero_factura=f'DEMO-{1000 + i}',
                cliente=cliente,
                fecha=timezone.now().date(),
                neto=Decimal('0.00'),
                iva=Decimal('0.00'),
                total=Decimal('0.00')
            )
            
            # Agregar 1-3 productos aleatorios a la venta
            num_productos = random.randint(1, 3)
            selected_productos = random.sample(productos, min(num_productos, len(productos)))
            
            total_neto = Decimal('0.00')
            
            for producto in selected_productos:
                cantidad = random.randint(1, 3)
                precio_unitario = producto.precio
                precio_total = precio_unitario * cantidad
                
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    precio_total=precio_total
                )
                
                total_neto += precio_total
                
                # Reducir stock del producto
                producto.stock = max(0, producto.stock - cantidad)
                producto.save()
            
            # Actualizar totales de la venta
            iva = total_neto * Decimal('0.10')  # 10% IVA
            total = total_neto + iva
            
            venta.neto = total_neto
            venta.iva = iva
            venta.total = total
            venta.save()
            
            self.stdout.write(f'🛒 Venta creada: {venta.numero_factura}')
