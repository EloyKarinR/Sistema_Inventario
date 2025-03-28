from django.contrib import admin

from Inventario.models import Cliente, Fabricante, HistorialCompras, NuevaCompra, NuevaVenta, PerfilEmpresa, Producto, Proveedor, Venta

# Register your models here.
admin.site.register(NuevaCompra)
admin.site.register(HistorialCompras)
admin.site.register(Producto)
admin.site.register(Fabricante)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(NuevaVenta)
admin.site.register(PerfilEmpresa)
admin.site.register(Venta)