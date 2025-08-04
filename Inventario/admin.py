from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html

from Inventario.models import Cliente, Fabricante, HistorialCompras, NuevaCompra, NuevaVenta, PerfilEmpresa, Producto, Proveedor, Venta

# Personalizar el admin site
admin.site.site_header = "🏢 Sistema de Inventario - Administración"
admin.site.site_title = "Sistema de Inventario"
admin.site.index_title = "Panel de Administración"

# CSS personalizado para el admin
class CustomAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = format_html("""
        <style>
            #header { 
                background: linear-gradient(135deg, #2c5f2d 0%, #0c4b33 100%) !important; 
                border-bottom: 3px solid #97bc62 !important; 
            }
            #branding h1, #branding h1 a:link, #branding h1 a:visited { 
                color: #fff !important; 
                font-weight: bold !important; 
            }
            .breadcrumbs { 
                background: #97bc62 !important; 
                color: #2c5f2d !important; 
                font-weight: 600 !important; 
            }
            .breadcrumbs a { color: #2c5f2d !important; }
            .module h2, .module caption { 
                background: linear-gradient(135deg, #2c5f2d, #0c4b33) !important; 
                color: white !important; 
            }
            .button, input[type=submit], input[type=button], .submit-row input, a.button { 
                background: linear-gradient(135deg, #2c5f2d, #0c4b33) !important; 
                border: none !important; 
                color: white !important; 
                border-radius: 6px !important; 
            }
            .button:hover, input[type=submit]:hover { 
                background: linear-gradient(135deg, #0c4b33, #2c5f2d) !important; 
            }
            .results th { 
                background: linear-gradient(135deg, #2c5f2d, #0c4b33) !important; 
                color: white !important; 
            }
            .results tr:nth-child(even) { background: #f8f9fa !important; }
            .results tr:hover { background: #e8f5e8 !important; }
            #content { background: #f8f9fa !important; }
        </style>
        """)
        return context

# Aplicar la personalización
# admin_site = CustomAdminSite(name='custom_admin')

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