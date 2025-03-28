from django.urls import path

from Inventario import views

app_name = 'Inventario'

urlpatterns = [
    path('', views.panel_control, name='panel_control'),
    path('panel_control/', views.panel_control, name='panel_control'),
    path('nueva_compra/', views.nueva_compra, name='nueva_compra'),
    path('historial_compras/', views.historial_compras, name='historial_compras'),
    path('productos/', views.productos, name='productos'),
    path('productos/nuevo_producto/', views.nuevo_producto, name='nuevo_producto'),
    path('editar_producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

    path('fabricantes/', views.fabricantes, name='fabricantes'),
    path('fabricantes/crear_fabricante/', views.crear_fabricante, name='crear_fabricante'),
    path('fabricantes/editar/<int:id>/', views.editar_fabricante, name='editar_fabricante'),
    path('fabricantes/borrar/<int:id>/', views.borrar_fabricante, name='borrar_fabricante'),

    path('guardar-compra/', views.guardar_compra, name='guardar_compra'),
    path('editar_compra/<int:compra_id>/', views.editar_compra, name='editar_compra'),
    path('actualizar_compra/<int:compra_id>/', views.actualizar_compra, name='actualizar_compra'),
    path('eliminar_compra/<int:compra_id>/', views.eliminar_compra, name='eliminar_compra'),

    path('clientes/', views.clientes, name='clientes'),
    path('cliente_detalles/<int:cliente_id>/', views.cliente_detalles, name='cliente_detalles'),
    #path('nuevo_cliente/', views.nuevo_cliente, name='nuevo_cliente'),
    path('editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar_cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('guardar_cliente/', views.guardar_cliente, name='guardar_cliente'),

    path('proveedores/', views.proveedores, name='proveedores'),
    path('guardar_proveedor/', views.guardar_proveedor, name='guardar_proveedor'),
    path('proveedor_detalles/<int:proveedor_id>/', views.proveedor_detalles, name='proveedor_detalles'),
    path('editar_proveedor/<int:proveedor_id>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar_proveedor/<int:proveedor_id>/', views.eliminar_proveedor, name='eliminar_proveedor'),

    path('nueva_venta/', views.nueva_venta, name='nueva_venta'),
    path('obtener_cliente/<int:cliente_id>/', views.obtener_cliente, name='obtener_cliente'),
    path('buscar_productos_venta/', views.buscar_productos_venta, name='buscar_productos_venta'),
    path('guardar_venta/', views.guardar_venta, name='guardar_venta'),
    path('lista_productos/', views.lista_productos, name='lista_productos'),

    path('admin_facturas/', views.admin_facturas, name='admin_facturas'),
    path('borrar_venta/<int:venta_id>/', views.borrar_venta, name='borrar_venta'),
    path('editar_venta/<int:venta_id>/', views.editar_venta, name='editar_venta'),
    path('admin_facturas/editar_venta/<int:venta_id>/', views.editar_venta, name='editar_venta'),
    path('actualizar_venta/', views.actualizar_venta, name='actualizar_venta'),
    path('perfil_empresa/', views.perfil_empresa, name='perfil_empresa'),
    path('ver_pdf/<int:venta_id>/', views.ver_pdf, name='ver_pdf'),
    path('reporte_inventario/', views.reporte_inventario, name='reporte_inventario'),
    path('productos-stock-bajo/', views.productos_stock_bajo, name='productos_stock_bajo'),
    path('generar-pdf-inventario/', views.generar_pdf_inventario, name='generar_pdf_inventario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

