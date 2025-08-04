from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Inventario.models import Producto  # Asegúrate de importar tu modelo de Producto
from django.contrib import messages
from .forms import ProductoForm 
from decimal import Decimal
from .models import Fabricante, Venta, Cliente
from .forms import FabricanteForm
from .models import Proveedor
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import traceback
import os
from Inventario.models import HistorialCompras
from django.views.decorators.csrf import csrf_exempt  # Temporal para pruebas
from django.db.models import Max
from datetime import datetime
from .models import Cliente
from django.utils import timezone
import re
from django.db.models import Q

@login_required
@require_http_methods(["GET", "POST"])
def buscar_productos_venta(request):
    try:
        # Obtener término de búsqueda dependiendo del método
        if request.method == 'POST':
            data = json.loads(request.body)
            termino = data.get('termino', '').strip()
        else:  # GET
            termino = request.GET.get('q', '').strip()
        
        if len(termino) < 2:
            return JsonResponse({'productos': [], 'mensaje': 'Término muy corto'})
        
        print(f"Construyendo consulta de búsqueda para término: '{termino}'")
        
        # Búsqueda más flexible sin distinguir mayúsculas/minúsculas
        query = Q(nombre__icontains=termino) | Q(codigo__icontains=termino) | Q(descripcion__icontains=termino)
        
        # Buscar todos los productos que coincidan con el término
        productos = Producto.objects.filter(query)
        print(f"Productos encontrados para '{termino}': {productos.count()}")
        
        # Debug paso a paso
        print("=== DEBUG PASO A PASO ===")
        
        try:
            print("Paso 1: Intentando obtener primer producto...")
            primer_producto = productos.first()
            print(f"Primer producto obtenido: {primer_producto}")
            
            if primer_producto:
                print(f"Paso 2: Accediendo a atributos del producto...")
                print(f"ID: {primer_producto.id}")
                print(f"Nombre: {primer_producto.nombre}")
                print(f"Código: {primer_producto.codigo}")
                print(f"Precio: {primer_producto.precio}")
                print(f"Stock: {primer_producto.stock}")
                print(f"Fabricante: {primer_producto.fabricante}")
                
                # Intentar crear el diccionario del producto
                print("Paso 3: Creando diccionario del producto...")
                producto_dict = {
                    'id': primer_producto.id,
                    'nombre': primer_producto.nombre,
                    'codigo': primer_producto.codigo,
                    'precio': str(primer_producto.precio),
                    'stock': primer_producto.stock,
                    'descripcion': primer_producto.descripcion or '',
                    'imagen': primer_producto.imagen.url if primer_producto.imagen else None,
                    'fabricante': primer_producto.fabricante
                }
                print("Paso 4: Diccionario creado exitosamente!")
                print(f"Diccionario: {producto_dict}")
                
                productos_lista = [producto_dict]
            else:
                print("No se encontró ningún producto")
                productos_lista = []
                
        except Exception as e:
            print(f"ERROR en debug paso a paso: {e}")
            print(f"Traceback completo: {traceback.format_exc()}")
            productos_lista = []
        
        print(f"Total productos procesados: {len(productos_lista)}")
        
        response_data = {
            'productos': productos_lista,
            'status': 'success',
            'total_productos': len(productos_lista),
            'termino_busqueda': termino,
            'mensaje': f'Se encontraron {len(productos_lista)} productos para el término "{termino}"'
        }
        print(f"Enviando respuesta con {len(productos_lista)} productos")
        return JsonResponse(response_data)
        
    except Exception as e:
        print(f"Error en búsqueda de productos: {str(e)}")
        return JsonResponse({
            'productos': [],
            'status': 'error',
            'mensaje': str(e)
        })

# Importaciones adicionales necesarias
from .models import NuevaVenta, Venta, DetalleVenta, PerfilEmpresa, Profile
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
import pytz
import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.http import HttpResponse, FileResponse
from django.conf import settings
from reportlab.lib.units import inch
from django.db.models import Q, Sum, F, Count
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from .forms import ProfileForm


def index(request):
    """Vista de bienvenida para Vercel demo"""
    if not request.user.is_authenticated:
        # Para demo en Vercel, mostrar página de bienvenida
        if 'VERCEL' in os.environ:
            return render(request, 'Inventario/bienvenida_vercel.html')
        return redirect('Inventario:login')
    return redirect('Inventario:panel_control')

@login_required
def panel_control(request):
    # Calcular el valor total del inventario (precio * stock)
    inventario_total = Producto.objects.aggregate(
        total=Sum(F('precio') * F('stock'))
    )['total'] or 0
    
    context = {
        'inventario_total': inventario_total,
        # ... otros datos del contexto ...
    }
    return render(request, 'Inventario/panel_control.html', context)

@login_required
def nueva_compra(request):
    search_query = request.GET.get('search', '')
    proveedores = Proveedor.objects.all()
    productos = Producto.objects.all()

    if search_query:
        productos = productos.filter(producto__icontains=search_query)  # Filtra por nombre si hay búsqueda

    paginator = Paginator(productos, 5)  # 5 productos por página
    page_number = request.GET.get('page')  # Asegúrate de que tenga un valor por defecto
    page_obj = paginator.get_page(page_number)

    print(f"Página actual: {page_obj.number}, Tiene anterior: {page_obj.has_previous}, Tiene siguiente: {page_obj.has_next}")

    return render(request, 'Inventario/nueva_compra.html', {'page_obj': page_obj, 'search_query': search_query, 'proveedores': proveedores})

@login_required
def historial_compras(request):
    compras = HistorialCompras.objects.all().order_by('-fecha')
    print("Compras encontradas:", compras)
    
    context = {
        'compras': compras,
        'proveedores': Proveedor.objects.all(),  # Para el filtro de proveedores
    }
    return render(request, 'Inventario/historial_compras.html', context)

@login_required
def productos_view(request):
    # Iniciar el queryset con todos los productos
    productos_list = Producto.objects.all().order_by('codigo')
    
    # Aplicar filtros si existen
    search_query = request.GET.get('searchInput', '')
    fabricante_query = request.GET.get('fabricanteSelect', '')
    
    if search_query:
        productos_list = productos_list.filter(nombre__icontains=search_query)
    
    if fabricante_query:
        productos_list = productos_list.filter(fabricante__iexact=fabricante_query)
    
    # Configurar la paginación
    paginator = Paginator(productos_list, 5)  # Mostrar 5 productos por página
    page = request.GET.get('page', 1)
    
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    
    # Obtener fabricantes únicos para el filtro
    fabricantes_unicos = Producto.objects.values_list('fabricante', flat=True).distinct()
    
    context = {
        'productos': productos,
        'fabricantes_unicos': fabricantes_unicos,
        'search_query': search_query,
        'fabricante_query': fabricante_query,
    }
    
    return render(request, 'Inventario/productos.html', context)

def nuevo_producto(request):
    if request.method == 'POST':
        try:
            # Obtener y validar el fabricante
            fabricante_nombre = request.POST.get('fabricante')
            print(f"Fabricante recibido: '{fabricante_nombre}'")  # Debug
            
            if not fabricante_nombre:
                raise ValueError("Debe seleccionar un fabricante")

            # Convertir valores numéricos
            try:
                costo = float(request.POST['costo'])
                precio = float(request.POST['precio'])
                stock = int(request.POST['stock'])
            except ValueError as ve:
                raise ValueError("Por favor, ingrese valores numéricos válidos para costo, precio y stock")

            nuevo_producto = Producto(
                codigo=request.POST['codigo'],
                modelo=request.POST['modelo'],
                nombre=request.POST['nombre'],
                descripcion=request.POST['descripcion'],
                fabricante=fabricante_nombre,
                estado=request.POST['estado'],
                costo=costo,
                precio=precio,
                stock=stock
            )
            
            if 'imagen' in request.FILES:
                nuevo_producto.imagen = request.FILES['imagen']
            
            nuevo_producto.save()
            print(f"Producto guardado con fabricante: {nuevo_producto.fabricante}")  # Debug
            messages.success(request, 'Producto guardado exitosamente')
            return redirect('Inventario:productos')
        except Exception as e:
            print(f"Error detallado: {str(e)}")
            messages.error(request, f'Error al guardar el producto: {str(e)}')
            
            # Imprimir todos los datos del POST para debugging
            print("Datos del POST:")
            for key, value in request.POST.items():
                print(f"{key}: {value}")
            
            # Obtener fabricantes para el formulario en caso de error
            fabricantes = Fabricante.objects.all()
            return render(request, 'Inventario/nuevo_producto.html', {
                'fabricantes': fabricantes,
                'form_data': request.POST  # Devolvemos los datos del formulario para mantenerlos
            })

    # Obtener fabricantes para el formulario
    fabricantes = Fabricante.objects.all()
    return render(request, 'Inventario/nuevo_producto.html', {'fabricantes': fabricantes})

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    fabricantes = Fabricante.objects.all()
    
    print("Valores del producto:")
    print(f"Costo original: {producto.costo}")
    print(f"Precio original: {producto.precio}")
    
    # Convertir los valores a float para la presentación
    try:
        costo = float(producto.costo) if producto.costo is not None else 0.00
        precio = float(producto.precio) if producto.precio is not None else 0.00
        
        # Asegurarse de que el precio no sea menor que el costo
        if precio < costo:
            precio = costo
            # Actualizar el precio en la base de datos
            producto.precio = Decimal(str(costo))
            producto.save()
            messages.warning(request, 'El precio de venta ha sido ajustado al costo para evitar pérdidas.')
            
    except (TypeError, ValueError):
        print("Error al convertir valores decimales")
        costo = 0.00
        precio = 0.00
    
    print(f"Costo procesado: {costo}")
    print(f"Precio procesado: {precio}")
    
    # Calcular la utilidad
    utilidad = precio - costo
    print(f"Utilidad calculada: {utilidad}")
    
    if request.method == 'POST':
        try:
            # Procesar los datos del formulario
            producto.codigo = request.POST['codigo']
            producto.modelo = request.POST['modelo']
            producto.nombre = request.POST['nombre']
            producto.descripcion = request.POST['descripcion']
            producto.fabricante = request.POST['fabricante']
            producto.estado = request.POST['estado']
            
            # Convertir valores numéricos
            try:
                nuevo_costo = Decimal(request.POST['costo'])
                nuevo_precio = Decimal(request.POST['precio'])
                
                # Validar que el precio no sea menor que el costo
                if nuevo_precio < nuevo_costo:
                    nuevo_precio = nuevo_costo
                    messages.warning(request, 'El precio de venta ha sido ajustado al costo para evitar pérdidas.')
                
                producto.costo = nuevo_costo
                producto.precio = nuevo_precio
                producto.stock = int(request.POST['stock'])
            except ValueError:
                raise ValueError("Por favor, ingrese valores numéricos válidos para costo, precio y stock")
            
            if 'imagen' in request.FILES:
                producto.imagen = request.FILES['imagen']
            
            producto.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('Inventario:productos')
            
        except Exception as e:
            print(f"Error al actualizar: {str(e)}")
            messages.error(request, f'Error al actualizar el producto: {str(e)}')
    
    # Preparar el contexto para el formulario
    context = {
        'producto': producto,
        'fabricantes': fabricantes,
        'utilidad': "{:.2f}".format(utilidad),
        'costo': "{:.2f}".format(costo),
        'precio': "{:.2f}".format(precio)
    }
    print("Valores enviados al contexto:", context)
    return render(request, 'Inventario/editar_producto.html', context)

def eliminar_producto(request, producto_id):
    try:
        producto = get_object_or_404(Producto, id=producto_id)
        nombre_producto = producto.nombre  # Guardamos el nombre para el mensaje
        producto.delete()
        messages.success(request, f'El producto "{nombre_producto}" fue eliminado exitosamente')
    except Exception as e:
        messages.error(request, f'Error al eliminar el producto: {str(e)}')
    
    return redirect('/productos')

@login_required
def fabricantes(request):
    queryset = Fabricante.objects.all()
    query = request.GET.get('q')
    
    if query:
        # Cambiamos nombre__icontains por fabricante__icontains
        queryset = queryset.filter(fabricante__icontains=query)

    mostrar = request.GET.get('mostrar', 5)
    paginator = Paginator(queryset, int(mostrar))

    page = request.GET.get('page')
    try:
        fabricantes = paginator.page(page)
    except PageNotAnInteger:
        fabricantes = paginator.page(1)
    except EmptyPage:
        fabricantes = paginator.page(paginator.num_pages)

    context = {
        'fabricantes': fabricantes,
        'is_paginated': fabricantes.has_other_pages(),
        'page_obj': fabricantes,
    }
    return render(request, 'Inventario/fabricantes.html', {'fabricantes': fabricantes})

def crear_fabricante(request):
    if request.method == 'POST':
        form = FabricanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Inventario:fabricantes')  # Asegúrate de que este nombre sea correcto
    else:
        form = FabricanteForm()
    return render(request, 'Inventario/fabricantes.html', {'form': form})

def lista_fabricantes(request):
    fabricantes = Fabricante.objects.all()
    return render(request, 'Inventario/fabricantes.html', {'fabricantes': fabricantes})

@require_http_methods(["POST"])
@transaction.atomic
def guardar_compra(request):
    try:
        data = json.loads(request.body)
        print("=== DEBUG: Iniciando proceso de compra ===")
        print(f"Datos recibidos: {data}")
        
        # Verificar si 'detalles' está en los datos
        if 'detalles' not in data:
            print("ERROR: No se encontró la clave 'detalles' en los datos")
            print("Datos disponibles:", data)
            raise ValueError("No hay detalles de compra. Asegúrate de agregar productos antes de guardar.")
            
        if not data['detalles']:
            raise ValueError("La lista de detalles está vacía. Agrega al menos un producto.")
        
        # Generar número de compra único
        fecha_actual = datetime.now()
        prefijo = fecha_actual.strftime('%Y%m')
        
        ultimo_numero = HistorialCompras.objects.filter(
            numero_compra__startswith=prefijo
        ).aggregate(
            max_num=Max('numero_compra')
        )['max_num']
        
        contador = int(ultimo_numero[-4:]) + 1 if ultimo_numero else 1
        nuevo_numero = f"{prefijo}{contador:04d}"
        
        # Obtener el proveedor
        proveedor = Proveedor.objects.get(id=data['proveedor'])
        
        # Crear la compra dentro de la transacción
        with transaction.atomic():
            # Crear la compra
            compra = HistorialCompras.objects.create(
                numero_compra=nuevo_numero,
                proveedor=proveedor,
                fecha=data['fecha'],
                usuario=request.user,
                neto=Decimal(str(data['neto'])),
                iva=Decimal(str(data['iva'])),
                total=Decimal(str(data['total']))
            )
            print(f"Compra creada con ID: {compra.id}")
            
            # Actualizar el stock de cada producto
            for detalle in data.get('detalles', []):
                try:
                    codigo_producto = detalle['codigo']
                    cantidad = int(detalle['cantidad'])
                    
                    print(f"Procesando producto: {codigo_producto}")
                    print(f"Cantidad a agregar: {cantidad}")
                    
                    # Modificar esta parte para usar filter en lugar de get
                    productos = Producto.objects.filter(codigo=codigo_producto)
                    if not productos.exists():
                        raise ValueError(f"Producto con código {codigo_producto} no existe")
                    if productos.count() > 1:
                        # Si hay duplicados, actualizar el primero y registrar una advertencia
                        print(f"ADVERTENCIA: Múltiples productos encontrados con código {codigo_producto}")
                    
                    producto = productos.first()
                    stock_anterior = producto.stock
                    
                    # Actualizar usando update para evitar condiciones de carrera
                    productos.update(stock=F('stock') + cantidad)
                    
                    # Verificar la actualización
                    producto_actualizado = Producto.objects.get(id=producto.id)
                    print(f"Stock verificado después de actualizar: {producto_actualizado.stock}")
                    
                except Exception as e:
                    print(f"Error al actualizar producto {codigo_producto}: {str(e)}")
                    raise
        
        print("=== Proceso de compra completado exitosamente ===")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Compra guardada exitosamente',
            'numero_compra': nuevo_numero
        })
        
    except Exception as e:
        print("Error detallado:", str(e))
        print(traceback.format_exc())
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def editar_compra(request, compra_id):
    try:
        # Obtener la compra con todos sus detalles
        compra = HistorialCompras.objects.get(id=compra_id)
        proveedores = Proveedor.objects.all()
        
        # Imprimir para debug
        print("Datos de la compra:")
        print(f"Neto: {compra.neto}")
        print(f"IVA: {compra.iva}")
        print(f"Total: {compra.total}")
        
        context = {
            'compra': compra,
            'proveedores': proveedores,
        }
        
        return render(request, 'Inventario/editar_compra.html', context)
        
    except HistorialCompras.DoesNotExist:
        messages.error(request, 'La compra no existe')
        return redirect('historial_compras')

@require_http_methods(["POST"])
def actualizar_compra(request, compra_id):
    try:
        data = json.loads(request.body)
        compra = HistorialCompras.objects.get(id=compra_id)
        
        # Verificar si el nuevo número de compra ya existe
        nuevo_numero = data['numero_compra']
        if HistorialCompras.objects.exclude(id=compra_id).filter(numero_compra=nuevo_numero).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'El número de compra ya existe'
            }, status=400)
        
        # Actualizar todos los campos incluyendo numero_compra
        compra.numero_compra = nuevo_numero
        compra.proveedor_id = data['proveedor']
        compra.fecha = data['fecha']
        compra.neto = Decimal(data['neto'])
        compra.iva = Decimal(data['iva'])
        compra.total = Decimal(data['total'])
        
        compra.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Compra actualizada exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_http_methods(["POST"])
def eliminar_compra(request, compra_id):
    try:
        compra = HistorialCompras.objects.get(id=compra_id)
        compra.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Compra eliminada exitosamente'
        })
    except HistorialCompras.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'La compra no existe'
        }, status=404)
    except Exception as e:
        print(f"Error al eliminar: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def clientes(request):
    clientes = Cliente.objects.all()
    context = {
        'clientes': clientes
    }
    return render(request, 'Inventario/clientes.html', context)

@require_http_methods(["GET"])
def cliente_detalles(request, cliente_id):
    try:
        cliente = get_object_or_404(Cliente, id=cliente_id)
        return JsonResponse({
            'status': 'success',
            'cliente': {
                'nombre': cliente.nombre,
                'numero_impuesto': cliente.numero_impuesto,
                'sitio_web': cliente.sitio_web,
                'telefono_empresa': cliente.telefono_empresa,
                'nombres': cliente.nombres,
                'apellidos': cliente.apellidos,
                'correo_electronico': cliente.correo_electronico,
                'telefono_contacto': cliente.telefono_contacto,
                'calle': cliente.calle,
                'ciudad': cliente.ciudad,
                'region_provincia': cliente.region_provincia,
                'codigo_postal': cliente.codigo_postal,
                'pais': cliente.pais
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def nuevo_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.create(**data)
            return JsonResponse({
                'status': 'success',
                'message': 'Cliente creado exitosamente'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return render(request, 'Inventario/nuevo_cliente.html')

@require_http_methods(["POST"])
def editar_cliente(request, cliente_id):
    try:
        cliente = get_object_or_404(Cliente, id=cliente_id)
        data = json.loads(request.body)
        
        # Actualizar todos los campos
        for field, value in data.items():
            setattr(cliente, field, value)
        
        cliente.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Cliente actualizado exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_http_methods(["POST"])
def eliminar_cliente(request, cliente_id):
    try:
        cliente = get_object_or_404(Cliente, id=cliente_id)
        nombre_cliente = cliente.nombre  # Guardamos el nombre para el mensaje
        cliente.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Cliente {nombre_cliente} eliminado exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_http_methods(["POST"])
def guardar_cliente(request):
    try:
        datos = json.loads(request.body)
        
        # Validar nmero de impuesto
        if not datos['numero_impuesto'].isdigit():
            return JsonResponse({
                'status': 'error',
                'message': 'El número de impuesto debe contener solo números'
            }, status=400)
        
        # Validar teléfonos
        telefono_regex = re.compile(r'^\+?[\d]{9,15}$')
        if not telefono_regex.match(datos['telefono_empresa']):
            return JsonResponse({
                'status': 'error',
                'message': 'El teléfono de empresa tiene un formato inválido'
            }, status=400)
            
        if not telefono_regex.match(datos['telefono_contacto']):
            return JsonResponse({
                'status': 'error',
                'message': 'El teléfono de contacto tiene un formato inválido'
            }, status=400)
        
        # Validar código postal
        if not datos['codigo_postal'].isdigit():
            return JsonResponse({
                'status': 'error',
                'message': 'El código postal debe contener solo números'
            }, status=400)
        
        # Si todas las validaciones pasan, guardar el cliente
        cliente = Cliente.objects.create(**datos)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Cliente guardado exitosamente',
            'id': cliente.id
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def proveedores(request):
    proveedores = Proveedor.objects.all().order_by('-fecha_registro')
    return render(request, 'Inventario/proveedores.html', {'proveedores': proveedores})

@require_http_methods(["POST"])
def guardar_proveedor(request):
    try:
        datos = json.loads(request.body)
        
        # Validar número de impuesto
        if not datos['numero_impuesto'].isdigit():
            return JsonResponse({
                'status': 'error',
                'message': 'El número de impuesto debe contener solo números'
            }, status=400)
        
        # Validar teléfonos
        telefono_regex = re.compile(r'^\+?[\d]{9,15}$')
        if not telefono_regex.match(datos['telefono_empresa']):
            return JsonResponse({
                'status': 'error',
                'message': 'El teléfono de empresa tiene un formato inválido'
            }, status=400)
            
        if not telefono_regex.match(datos['telefono_contacto']):
            return JsonResponse({
                'status': 'error',
                'message': 'El teléfono de contacto tiene un formato inválido'
            }, status=400)
        
        # Validar código postal
        if not datos['codigo_postal'].isdigit():
            return JsonResponse({
                'status': 'error',
                'message': 'El código postal debe contener solo números'
            }, status=400)
        
        # Si todas las validaciones pasan, guardar el proveedor
        proveedor = Proveedor.objects.create(**datos)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Proveedor guardado exitosamente',
            'id': proveedor.id
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_http_methods(["GET"])
def proveedor_detalles(request, proveedor_id):
    try:
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        return JsonResponse({
            'status': 'success',
            'proveedor': {
                'nombre': proveedor.nombre,
                'numero_impuesto': proveedor.numero_impuesto,
                'sitio_web': proveedor.sitio_web,
                'telefono_empresa': proveedor.telefono_empresa,
                'nombres': proveedor.nombres,
                'apellidos': proveedor.apellidos,
                'correo_electronico': proveedor.correo_electronico,
                'telefono_contacto': proveedor.telefono_contacto,
                'calle': proveedor.calle,
                'ciudad': proveedor.ciudad,
                'region_provincia': proveedor.region_provincia,
                'codigo_postal': proveedor.codigo_postal,
                'pais': proveedor.pais,
                'fecha_actualizacion': proveedor.fecha_actualizacion.isoformat() if proveedor.fecha_actualizacion else None
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_http_methods(["POST"])
def editar_proveedor(request, proveedor_id):
    try:
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        datos = json.loads(request.body)
        
        # Actualizar fecha_actualizacion
        datos['fecha_actualizacion'] = timezone.now()
        
        for campo, valor in datos.items():
            setattr(proveedor, campo, valor)
        
        proveedor.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Proveedor actualizado exitosamente'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_http_methods(["POST"])
def eliminar_proveedor(request, proveedor_id):
    try:
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        nombre_proveedor = f"{proveedor.nombre} - {proveedor.nombres} {proveedor.apellidos}"
        proveedor.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Proveedor {nombre_proveedor} eliminado exitosamente'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def nueva_venta(request):
    productos = Producto.objects.all()
    
    # Obtener término de búsqueda
    query = request.GET.get('q', '')
    
    # Consulta base excluyendo Cliente Final
    clientes_base = Cliente.objects.exclude(numero_impuesto="00000000")
    
    # Aplicar búsqueda si hay término
    if query:
        clientes_base = clientes_base.filter(
            Q(nombre__icontains=query) |
            Q(numero_impuesto__icontains=query) |
            Q(correo_electronico__icontains=query)
        )
    
    # Ordenar por frecuencia de compras y luego por nombre
    clientes = clientes_base.annotate(
        num_compras=Count('venta')
    ).order_by('-num_compras', 'nombre')
    
    # Asegurarse de que existe el Cliente Final
    cliente_final = Cliente.objects.filter(numero_impuesto="00000000").first()
    if not cliente_final:
        cliente_final = Cliente.objects.create(
            numero_impuesto="00000000",
            nombre="Cliente Final",
            telefono_empresa="000000000",
            nombres="Cliente",
            apellidos="Final",
            correo_electronico="cliente@final.com",
            telefono_contacto="000000000",
            calle="Sin dirección",
            ciudad="Sin ciudad",
            region_provincia="Sin región",
            codigo_postal="00000",
            pais="Sin país",
            tipo='persona_natural'
        )

    # Obtener el último número de factura y generar el siguiente
    ultima_venta = Venta.objects.order_by('-numero_factura').first()
    siguiente_numero = '1'
    if ultima_venta:
        try:
            ultimo_numero = int(ultima_venta.numero_factura)
            siguiente_numero = str(ultimo_numero + 1)
        except ValueError:
            # Si el último número no es numérico, empezar desde 1
            siguiente_numero = '1'

    # Obtener la fecha actual
    fecha_actual = timezone.now()

    return render(request, 'Inventario/nueva_venta.html', {
        'productos': productos,
        'clientes': clientes,
        'siguiente_numero_factura': siguiente_numero,
        'fecha_actual': fecha_actual,
        'active_page': 'nueva_venta'
    })

@login_required
@login_required
@require_POST
def crear_cliente_rapido(request):
    try:
        data = json.loads(request.body)
        
        # Validaciones básicas
        if not data.get('nombre'):
            return JsonResponse({
                'status': 'error',
                'message': 'El nombre es requerido'
            }, status=400)
            
        if not data.get('numero_impuesto'):
            return JsonResponse({
                'status': 'error',
                'message': 'El número de impuesto es requerido'
            }, status=400)
            
        # Crear el cliente con datos mínimos
        cliente = Cliente.objects.create(
            nombre=data['nombre'],
            numero_impuesto=data['numero_impuesto'],
            telefono_empresa=data.get('telefono', '000000000'),
            correo_electronico=data.get('correo_electronico', ''),
            nombres=data.get('nombres', ''),
            apellidos=data.get('apellidos', ''),
            telefono_contacto=data.get('telefono', '000000000'),
            calle=data.get('direccion', 'Sin dirección'),
            ciudad=data.get('ciudad', 'Sin ciudad'),
            region_provincia=data.get('region', 'Sin región'),
            codigo_postal='00000',
            pais=data.get('pais', 'Sin país'),
            tipo='persona_natural'  # Agregar tipo por defecto
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Cliente creado exitosamente',
            'cliente': {
                'id': cliente.id,
                'nombre': cliente.nombre,
                'numero_impuesto': cliente.numero_impuesto,
                'telefono': cliente.telefono_empresa
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_POST
@transaction.atomic
def guardar_venta(request):
    try:
        data = json.loads(request.body)
        
        # Validar que el número de factura no exista
        if Venta.objects.filter(numero_factura=data['numero_factura']).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'El número de factura ya existe'
            })
            
        # Manejar el caso de persona natural
        cliente_id = data['cliente']
        if cliente_id == 'persona_natural':
            # Buscar o crear un único Cliente Final
            cliente, created = Cliente.objects.get_or_create(
                numero_impuesto="00000000",
                defaults={
                    'nombre': "Cliente Final",
                    'telefono_empresa': "000000000",
                    'nombres': "Cliente",
                    'apellidos': "Final",
                    'correo_electronico': "cliente@final.com",
                    'telefono_contacto': "000000000",
                    'calle': "Sin dirección",
                    'ciudad': "Sin ciudad",
                    'region_provincia': "Sin región",
                    'codigo_postal': "00000",
                    'pais': "Sin país",
                    'tipo': 'persona_natural'
                }
            )
            cliente_id = cliente.id
        
        # Crear la venta
        venta = Venta.objects.create(
            numero_factura=data['numero_factura'],
            cliente_id=cliente_id,
            vendedor=request.user,
            neto=Decimal(str(data['neto'])),
            iva=Decimal(str(data['iva'])),
            total=Decimal(str(data['total']))
        )

        # Procesar los detalles
        for detalle in data['detalles']:
            producto = Producto.objects.get(codigo=detalle['codigo'])
            cantidad = int(detalle['cantidad'])

            # Validar stock
            if producto.stock < cantidad:
                # Si hay error de stock, eliminar la venta y retornar error
                venta.delete()
                return JsonResponse({
                    'status': 'error',
                    'message': f'Stock insuficiente para el producto {producto.nombre}. Stock actual: {producto.stock}'
                })

            # Crear el detalle
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=Decimal(str(detalle['precio_unitario'])),
                precio_total=Decimal(str(detalle['precio_total']))
            )

            # Actualizar el stock
            producto.stock -= cantidad
            producto.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Venta guardada exitosamente',
            'id': venta.id
        })

    except Exception as e:
        print(f"Error al guardar venta: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@require_http_methods(["GET"])
def buscar_clientes(request):
    query = request.GET.get('q', '')
    try:
        clientes = Cliente.objects.exclude(numero_impuesto="00000000")
        if query:
            clientes = clientes.filter(
                Q(nombre__icontains=query) |
                Q(numero_impuesto__icontains=query) |
                Q(correo_electronico__icontains=query)
            )
        
        # Ordenar por frecuencia de compras
        clientes = clientes.annotate(
            num_compras=Count('venta')
        ).order_by('-num_compras', 'nombre')[:10]  # Limitamos a 10 resultados
        
        data = [{
            'id': cliente.id,
            'nombre': cliente.nombre,
            'numero_impuesto': cliente.numero_impuesto,
            'correo': cliente.correo_electronico,
            'telefono': cliente.telefono_empresa,
            'num_compras': cliente.num_compras
        } for cliente in clientes]
        
        return JsonResponse({'status': 'success', 'clientes': data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def obtener_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        data = {
            'id': cliente.id,
            'nombre': cliente.nombre,
            'numero_impuesto': cliente.numero_impuesto,
            'direccion': cliente.calle,
            'ciudad': cliente.ciudad,
            'telefono': cliente.telefono_empresa,
        }
        return JsonResponse({'status': 'success', 'cliente': data})
    except Cliente.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cliente no encontrado'})

@csrf_exempt
@login_required
@require_POST
def borrar_venta(request, venta_id):
    try:
        print(f"Intentando borrar venta {venta_id}")  # Debug
        venta = Venta.objects.get(id=venta_id)
        venta.delete()
        return JsonResponse({'success': True})
    except Venta.DoesNotExist:
        error = f"Venta {venta_id} no encontrada"
        print(error)  # Debug
        return JsonResponse({'success': False, 'error': error})
    except Exception as e:
        error = f"Error al borrar venta: {str(e)}"
        print(error)  # Debug
        print(traceback.format_exc())  # Debug completo
        return JsonResponse({'success': False, 'error': error})

@login_required
def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    clientes = Cliente.objects.all()
    
    context = {
        'venta': venta,
        'detalles': detalles,
        'clientes': clientes,
    }
    return render(request, 'Inventario/editar_venta.html', context)

@login_required
@require_POST
def actualizar_venta(request):
    try:
        data = json.loads(request.body)
        venta = Venta.objects.get(id=data['id'])
        
        # Primero devolvemos el stock de los productos de la venta original
        detalles_antiguos = DetalleVenta.objects.filter(venta=venta)
        for detalle in detalles_antiguos:
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save()
        
        # Validar stock para los nuevos detalles
        for detalle in data['detalles']:
            producto = Producto.objects.get(codigo=detalle['codigo'])
            if producto.stock < int(detalle['cantidad']):
                # Revertir los cambios de stock
                for detalle_antiguo in detalles_antiguos:
                    producto = detalle_antiguo.producto
                    producto.stock -= detalle_antiguo.cantidad
                    producto.save()
                return JsonResponse({
                    'success': False,
                    'error': f'Stock insuficiente para el producto {producto.nombre}. Stock actual: {producto.stock}'
                })
        
        # Actualizar datos básicos de la venta
        venta.numero_factura = data['numero_factura']
        venta.cliente_id = data['cliente']
        
        # Calcular totales
        neto = sum(detalle['precio_total'] for detalle in data['detalles'])
        iva = neto * 0.19
        total = neto + iva
        
        venta.neto = neto
        venta.iva = iva
        venta.total = total
        venta.save()
        
        # Eliminar detalles anteriores
        DetalleVenta.objects.filter(venta=venta).delete()
        
        # Crear nuevos detalles y actualizar stock
        for detalle in data['detalles']:
            producto = Producto.objects.get(codigo=detalle['codigo'])
            cantidad = int(detalle['cantidad'])
            
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=detalle['precio_unitario'],
                precio_total=detalle['precio_total']
            )
            
            # Actualizar stock
            producto.stock -= cantidad
            producto.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Venta actualizada correctamente y stock actualizado'
        })
        
    except Venta.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Venta no encontrada'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def perfil_empresa(request):
    empresa = PerfilEmpresa.objects.first()
    
    # Obtener todas las zonas horarias y organizarlas por región
    zonas_horarias = {}
    for tz in pytz.common_timezones:
        region = tz.split('/')[0]
        if region not in zonas_horarias:
            zonas_horarias[region] = []
        zonas_horarias[region].append(tz)
    
    if request.method == 'POST':
        try:
            if not empresa:
                empresa = PerfilEmpresa()
            
            empresa.nombre = request.POST.get('nombre')
            empresa.numero_registro = request.POST.get('numero_registro')
            empresa.correo_electronico = request.POST.get('correo_electronico')
            empresa.telefono = request.POST.get('telefono')
            empresa.moneda = request.POST.get('moneda')
            empresa.zona_horaria = request.POST.get('zona_horaria')
            
            # Manejo del logo
            if request.FILES.get('logo'):
                empresa.logo = request.FILES['logo']
            
            # Datos de dirección
            empresa.calle = request.POST.get('calle')
            empresa.ciudad = request.POST.get('ciudad')
            empresa.region_provincia = request.POST.get('region_provincia')
            empresa.codigo_postal = request.POST.get('codigo_postal')
            empresa.pais = request.POST.get('pais')
            
            empresa.save()
            messages.success(request, 'Perfil de empresa actualizado correctamente')
            return redirect('perfil_empresa')
        except Exception as e:
            messages.error(request, f'Error al guardar: {str(e)}')
    
    context = {
        'empresa': empresa,
        'active_page': 'perfil_empresa'
    }
    return render(request, 'Inventario/perfil_empresa.html', context)

@login_required
def admin_facturas(request):
    # Obtener todas las ventas
    ventas = Venta.objects.all().order_by('-fecha')
    # Obtener todos los clientes para el filtro
    clientes = Cliente.objects.all()
    
    context = {
        'ventas': ventas,
        'clientes': clientes,
        'active_page': 'admin_facturas'
    }
    return render(request, 'Inventario/admin_facturas.html', context)

def ver_pdf(request, venta_id):
    # Obtener los datos
    venta = Venta.objects.get(id=venta_id)
    empresa = PerfilEmpresa.objects.first()
    detalles = DetalleVenta.objects.filter(venta=venta)  # Obtener detalles así
    
    # Crear el response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=factura_{venta.numero_factura}.pdf'
    
    # Crear el PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Dibujar el encabezado rojo
    p.setFillColor(colors.red)
    p.rect(0, height-60, width, 60, fill=1)
    
    # Logo de la empresa
    if empresa.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, str(empresa.logo))
        p.drawImage(logo_path, 50, height-50, width=100, height=40, preserveAspectRatio=True)
    
    # Información de contacto de la empresa
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 10)
    p.drawString(50, height-80, f"Tel: {empresa.telefono}")
    p.drawString(width/2-50, height-80, f"Email: {empresa.correo_electronico}")
    p.drawString(width-200, height-80, f"Dir: {empresa.calle}, {empresa.ciudad}")
    
    # Título FACTURA
    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(colors.white)
    p.drawString(width-200, height-40, "FACTURA")
    
    # Información de facturación
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height-150, "FACTURAR A")
    
    # Detalles del cliente (solo nombre)
    p.setFont("Helvetica", 10)
    p.drawString(50, height-170, f"Cliente: {venta.cliente.nombre}")
    
    # Número de factura y fecha
    p.drawString(width-200, height-150, f"Factura N°: {venta.numero_factura}")
    p.drawString(width-200, height-165, f"Fecha: {venta.fecha.strftime('%d/%m/%Y')}")
    
    # Tabla de productos
    y = height-250
    # Encabezados
    p.setFillColor(colors.red)
    p.rect(50, y, width-100, 20, fill=1)
    p.setFillColor(colors.white)
    p.drawString(60, y+5, "CANT.")
    p.drawString(120, y+5, "DESCRIPCIÓN")
    p.drawString(width-200, y+5, "PRECIO UNIT.")
    p.drawString(width-100, y+5, "PRECIO TOTAL")
    
    # Productos
    y -= 30
    p.setFillColor(colors.black)
    for detalle in detalles:  # Usar la variable detalles en lugar de venta.detalleventa_set
        p.drawString(60, y, str(detalle.cantidad))
        p.drawString(120, y, detalle.producto.nombre)
        p.drawString(width-200, y, f"${detalle.precio_unitario}")
        p.drawString(width-100, y, f"${detalle.precio_total}")
        y -= 20
    
    # Totales
    y = 150
    p.drawString(width-200, y, f"SUBTOTAL $ {venta.neto}")
    p.drawString(width-200, y-20, f"IVA $ {venta.iva}")
    p.setFont("Helvetica-Bold", 12)
    p.drawString(width-200, y-40, f"TOTAL $ {venta.total}")
    
    # Mensaje final
    p.setFont("Helvetica", 10)
    p.drawString(width/2-50, 50, "¡Gracias por su compra!")
    
    p.showPage()
    p.save()
    
    return response

def reporte_inventario(request):
    productos = Producto.objects.all()
    fabricantes = Producto.objects.values_list('fabricante', flat=True).distinct()
    
    # Obtener parámetros de búsqueda
    buscar_codigo = request.GET.get('codigo', '')
    buscar_nombre = request.GET.get('nombre', '')
    fabricante_seleccionado = request.GET.get('fabricante')

    # Aplicar filtros
    if buscar_codigo:
        productos = productos.filter(codigo__icontains=buscar_codigo)
    if buscar_nombre:
        productos = productos.filter(nombre__icontains=buscar_nombre)
    if fabricante_seleccionado:
        productos = productos.filter(fabricante=fabricante_seleccionado)
    
    # Calcular totales
    total_productos = productos.count()
    total_items = productos.aggregate(total=Sum('stock'))['total'] or 0
    total_inventario = sum(producto.stock * producto.costo for producto in productos)
    
    context = {
        'productos': productos,
        'fabricantes': fabricantes,
        'fabricante_seleccionado': fabricante_seleccionado,
        'buscar_codigo': buscar_codigo,
        'buscar_nombre': buscar_nombre,
        'total_productos': total_productos,
        'total_items': total_items,
        'total_inventario': total_inventario,
        'active_page': 'reporte_inventario'
    }
    return render(request, 'Inventario/reporte_inventario.html', context)

def productos_stock_bajo(request):
    # Obtener productos con stock <= 10, ordenados por stock ascendente
    productos_criticos = Producto.objects.filter(stock__lte=10).order_by('stock')
    
    # Categorizar productos por nivel de urgencia
    muy_criticos = productos_criticos.filter(stock__lte=3)
    criticos = productos_criticos.filter(stock__gt=3, stock__lte=7)
    precaucion = productos_criticos.filter(stock__gt=7, stock__lte=10)
    
    context = {
        'muy_criticos': muy_criticos,
        'criticos': criticos,
        'precaucion': precaucion,
        'total_criticos': productos_criticos.count(),
        'active_page': 'stock_bajo'
    }
    return render(request, 'Inventario/productos_stock_bajo.html', context)

def generar_pdf_inventario(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Logo - Actualizado con la ruta correcta
    logo_path = os.path.join(settings.MEDIA_ROOT, 'empresa', 'mitroservice.jpg')
    logo = Image(logo_path, 2*inch, 1*inch)
    elements.append(logo)
    
    # Título
    title = Paragraph("Reporte de Inventario", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    productos = Producto.objects.all().order_by('codigo')
    
    data = [['Código', 'Producto', 'Fabricante', 'Existencias', 'Costo', 'Total']]
    total_general = 0
    
    for producto in productos:
        total = producto.stock * producto.costo
        total_general += total
        data.append([
            producto.codigo,
            producto.nombre,
            producto.fabricante,
            str(producto.stock),
            f"{producto.costo:.2f}",
            f"{total:.2f}"
        ])
    
    data.append(['', '', '', '', 'Total', f"{total_general:.2f}"])
    
    table = Table(data, colWidths=[1*inch, 2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.grey),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
    ])
    table.setStyle(style)
    
    elements.append(table)
    
    doc.build(elements)
    
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'reporte_inventario_{datetime.now().strftime("%Y%m%d")}.pdf')

@csrf_exempt  # Agregamos esto temporalmente para pruebas
def editar_fabricante(request, id):
    if request.method == 'POST':
        try:
            # Debug prints
            print("="*50)
            print("Recibiendo petición POST")
            print("ID recibido:", id)
            print("POST data:", request.POST)
            
            fabricante = get_object_or_404(Fabricante, id_fabricante=id)  # Cambiado a id_fabricante
            print("Fabricante encontrado:", fabricante)
            
            # Obtener los datos
            nuevo_nombre = request.POST.get('fabricante')
            nuevo_numero = request.POST.get('numero_productos')
            nuevo_estado = request.POST.get('estado')
            
            print("Datos a actualizar:")
            print(f"Nombre: {nuevo_nombre}")
            print(f"Número productos: {nuevo_numero}")
            print(f"Estado: {nuevo_estado}")
            
            # Actualizar los datos
            fabricante.fabricante = nuevo_nombre
            fabricante.numero_productos = nuevo_numero
            fabricante.estado = nuevo_estado
            fabricante.save()
            
            print("Fabricante actualizado exitosamente")
            print("="*50)
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            import traceback
            print("ERROR:", str(e))
            print(traceback.format_exc())
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
def borrar_fabricante(request, id):
    try:
        fabricante = get_object_or_404(Fabricante, id_fabricante=id)  # Usamos id_fabricante
        fabricante.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def login_view(request):
    # Forzar el cierre de sesión de cualquier usuario anterior
    logout(request)
    
    # Si el usuario ya está autenticado (después del nuevo login), redirigir al panel de control
    if request.user.is_authenticated:
        return redirect('Inventario:panel_control')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Por favor, ingrese usuario y contraseña')
            return render(request, 'Inventario/login.html')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Limpiar completamente la sesión anterior
            request.session.flush()
            
            # Crear nueva sesión
            login(request, user)
            
            # Configurar la sesión para que expire al cerrar el navegador
            request.session.set_expiry(0)
            
            # Establecer una marca de tiempo de inicio de sesión
            request.session['login_time'] = timezone.now().timestamp()
            
            return redirect('Inventario:panel_control')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'Inventario/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        # Limpiar la sesión actual
        request.session.flush()
        # Realizar el logout
        logout(request)
    
    # Crear respuesta de redirección
    response = redirect('Inventario:login')
    
    # Eliminar todas las cookies relacionadas con la sesión
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')
    
    # Asegurar que el navegador no almacene en caché la página de login
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response
    response.delete_cookie('sessionid')
    return response

@login_required
def editar_perfil(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Perfil actualizado correctamente!')
            return redirect('Inventario:panel_control')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'Inventario/editar_perfil.html', {'form': form, 'profile': profile})

@login_required
@require_http_methods(["POST"])
def crear_cliente(request):
    try:
        data = json.loads(request.body)
        
        # Crear nuevo cliente con los datos del modal
        cliente = Cliente.objects.create(
            nombre=data.get('nombre'),
            numero_impuesto=data.get('rut_nit', ''),
            telefono_empresa=data.get('telefono', ''),
            correo_electronico=data.get('email', ''),
            tipo=data.get('tipo', 'Natural'),
            # Campos mínimos requeridos - se pueden completar después
            nombres=data.get('nombre', ''),  # Usar el nombre como nombres también
            apellidos='',  # Campo vacío por ahora
            telefono_contacto=data.get('telefono', ''),
            calle=data.get('direccion', ''),
            ciudad='',
            region_provincia='',
            codigo_postal='',
            pais='Paraguay'
        )
        
        return JsonResponse({
            'status': 'success',
            'mensaje': 'Cliente creado exitosamente',
            'cliente': {
                'id': cliente.id,
                'nombre': cliente.nombre
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'mensaje': str(e)
        }, status=400)









