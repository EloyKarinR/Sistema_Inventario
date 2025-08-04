from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.db import transaction
from django.contrib import messages
import json
import os
from .models import Producto, Venta, DetalleVenta, Cliente

def is_vercel_demo():
    """Helper function to check if running on Vercel"""
    return 'VERCEL' in os.environ

@login_required
@require_http_methods(["GET", "POST"])
def buscar_productos_venta(request):
    try:
        # Manejar tanto GET como POST
        if request.method == 'GET':
            termino = request.GET.get('q', '').strip()
        else:
            try:
                data = json.loads(request.body)
                termino = data.get('termino', '').strip()
            except json.JSONDecodeError:
                termino = ''
        
        if len(termino) < 2:
            return JsonResponse({
                'productos': [],
                'mensaje': 'El término de búsqueda debe tener al menos 2 caracteres'
            })

        # Convertir el término de búsqueda a minúsculas y eliminar espacios extras
        termino = termino.lower().strip()
        
        # Realizar la búsqueda de forma más flexible
        productos = Producto.objects.filter(
            Q(nombre__icontains=termino) |
            Q(codigo__icontains=termino)
        ).values(
            'id', 
            'nombre', 
            'codigo', 
            'precio',
            'stock',
            'fabricante',
            'imagen',
            'estado'
        )[:8]  # Limitamos a 8 resultados para una mejor presentación
        
        # Debug: imprimir información sobre la búsqueda
        print(f"Búsqueda con término: {termino}")
        print(f"SQL Query: {productos.query}")
        print(f"Número de productos encontrados: {productos.count()}")

        # Convertir a lista y formatear datos
        productos_lista = list(productos)
        for producto in productos_lista:
            producto['precio'] = str(producto.get('precio', '0'))
            producto['descripcion'] = producto.get('descripcion') or ''
            producto['fabricante'] = producto.get('fabricante', '')
            
            # Obtener la URL de la imagen
            try:
                if producto.get('imagen'):
                    # Asegurarnos de que la URL comience con /media/
                    imagen_path = producto['imagen']
                    if not imagen_path.startswith('/media/'):
                        producto['imagen'] = f'/media/{imagen_path}'
                else:
                    producto['imagen'] = '/static/img/no-image.png'
            except Exception as e:
                print(f"Error procesando imagen: {e}")
                producto['imagen'] = '/static/img/no-image.png'

        return JsonResponse({
            'productos': productos_lista,
            'status': 'success',
            'mensaje': f'Se encontraron {len(productos_lista)} productos'
        })

    except Exception as e:
        return JsonResponse({
            'productos': [],
            'status': 'error',
            'mensaje': str(e)
        })

@login_required
@require_http_methods(["POST"])
def guardar_venta(request):
    # Verificar si es demo de Vercel
    if is_vercel_demo():
        return JsonResponse({
            'status': 'error',
            'mensaje': '📋 Versión Demo: Esta es una demostración de solo lectura. No se puede registrar ventas en Vercel. Para probar todas las funcionalidades, descarga y ejecuta el proyecto localmente.'
        })
        
    try:
        print("Usuario autenticado:", request.user)
        print("Es anónimo:", request.user.is_anonymous)
        
        with transaction.atomic():
            # Validar que el cuerpo de la petición no esté vacío
            if not request.body:
                return JsonResponse({
                    'status': 'error',
                    'mensaje': 'No se recibieron datos para la venta'
                }, status=400)

            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as e:
                return JsonResponse({
                    'status': 'error',
                    'mensaje': 'Error al decodificar los datos JSON'
                }, status=400)

            # Debug: imprimir los datos recibidos
            print("Datos recibidos:", data)
            print("Tipo de datos:", type(data))
            print("Contenido del request.body:", request.body.decode('utf-8'))
            
            # Validar que todos los campos necesarios estén presentes
            detalles = data.get('detalles', [])
            if not detalles:
                return JsonResponse({
                    'status': 'error',
                    'mensaje': 'No se recibieron detalles para la venta'
                }, status=400)

            # Usar los detalles como productos
            productos = detalles
            if not productos:
                return JsonResponse({
                    'status': 'error',
                    'mensaje': 'No se recibieron productos para la venta'
                }, status=400)

            cliente_nombre = data.get('cliente')
            if not cliente_nombre:
                return JsonResponse({
                    'status': 'error',
                    'mensaje': 'No se especificó el cliente'
                }, status=400)
            
            # Si es "persona_natural", buscar o crear el cliente genérico
            if cliente_nombre == "persona_natural":
                cliente, created = Cliente.objects.get_or_create(
                    tipo="Natural",
                    nombre="Cliente General",
                    defaults={
                        'numero_impuesto': '00000000-0',
                        'nombres': 'Cliente',
                        'apellidos': 'General',
                        'telefono_empresa': '0000000000',
                        'correo_electronico': 'sin@correo.com',
                        'telefono_contacto': '0000000000',
                        'calle': 'Sin dirección',
                        'ciudad': 'Ciudad',
                        'region_provincia': 'Región',
                        'codigo_postal': '0000000',
                        'pais': 'País'
                    }
                )
                cliente_id = cliente.id
            else:
                # Aquí manejaríamos el caso de un cliente específico
                try:
                    cliente = Cliente.objects.get(id=cliente_nombre)
                    cliente_id = cliente.id
                except Cliente.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'mensaje': 'Cliente no encontrado'
                    }, status=400)

            numero_factura = data.get('numero_factura')
            if not numero_factura:
                return JsonResponse({
                    'status': 'error',
                    'mensaje': 'No se especificó el número de factura'
                }, status=400)
            
            # Crear la venta
            venta = Venta.objects.create(
                cliente_id=cliente_id,
                numero_factura=numero_factura,
                vendedor=request.user,  # Cambiado de usuario a vendedor
                neto=data.get('neto', 0),
                iva=data.get('iva', 0),
                total=data.get('total', 0)
            )
            
            # Procesar cada producto
            for producto_data in productos:
                codigo = producto_data.get('codigo')
                cantidad = int(producto_data.get('cantidad', 1))
                precio_unitario = float(producto_data.get('precio_unitario', 0))
                
                # Buscar el producto por código y asegurarse de que está activo
                try:
                    producto_id = producto_data.get('id')  # Obtener el ID del producto
                    if producto_id:
                        # Si tenemos ID, buscar por ID y validar el código
                        producto = Producto.objects.select_for_update().get(
                            id=producto_id,
                            codigo=codigo,
                            estado='Activo'
                        )
                    else:
                        # Si no tenemos ID, buscar solo por código pero mostrar advertencia
                        print(f"Advertencia: Producto sin ID especificado, código: {codigo}")
                        producto = Producto.objects.select_for_update().get(
                            codigo=codigo,
                            estado='Activo'
                        )
                    
                    if producto.stock < cantidad:
                        raise ValueError(f'Stock insuficiente para el producto {producto.nombre}')
                    
                    # Crear el detalle de venta
                    DetalleVenta.objects.create(
                        venta=venta,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                        precio_total=precio_unitario * cantidad  # Cambiado 'total' a 'precio_total'
                    )
                    
                    # Actualizar el stock
                    producto.stock -= cantidad
                    producto.save()
                    
                except Producto.MultipleObjectsReturned:
                    # Manejar el caso de productos duplicados
                    transaction.set_rollback(True)
                    return JsonResponse({
                        'status': 'error',
                        'mensaje': f'Error: Existen múltiples productos con el código {codigo}. Por favor, contacte al administrador.'
                    }, status=400)
                except Producto.DoesNotExist:
                    transaction.set_rollback(True)
                    return JsonResponse({
                        'status': 'error',
                        'mensaje': f'El producto con código {codigo} no existe o está inactivo'
                    }, status=400)
            
            return JsonResponse({
                'status': 'success',
                'mensaje': 'Venta guardada exitosamente',
                'venta_id': venta.id
            })
                
    except ValueError as e:
        return JsonResponse({
            'status': 'error',
            'mensaje': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'mensaje': f'Error al guardar la venta: {str(e)}'
        }, status=500)
