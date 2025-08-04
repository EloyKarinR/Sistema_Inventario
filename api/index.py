import os
import sys
from pathlib import Path

# Configurar el path del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Configurar variables de entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SistemaInventario.settings')
os.environ['VERCEL'] = '1'

# Variable global para Django app
_django_app = None

def initialize_django():
    """Inicializar Django una sola vez"""
    global _django_app
    
    if _django_app is not None:
        return _django_app
    
    try:
        import django
        from django.conf import settings
        
        # Configurar Django
        if not settings.configured:
            django.setup()
        
        # Ejecutar migraciones automáticamente
        from django.core.management import execute_from_command_line
        try:
            print("🗃️ Ejecutando migraciones...")
            execute_from_command_line(['manage.py', 'migrate', '--noinput'])
            
            # Crear superusuario si no existe
            from django.contrib.auth.models import User
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@demo.com', 'admin123')
                print("👤 Superusuario creado: admin/admin123")
                
        except Exception as migrate_error:
            print(f"⚠️ Error en migraciones: {migrate_error}")
        
        # Importar la aplicación WSGI de Django
        from django.core.wsgi import get_wsgi_application
        _django_app = get_wsgi_application()
        print("✅ Django inicializado correctamente")
        return _django_app
        
    except Exception as e:
        print(f"❌ Error inicializando Django: {e}")
        raise e

def application(environ, start_response):
    """WSGI application que carga Django"""
    
    try:
        # Intentar inicializar Django
        django_app = initialize_django()
        
        # Ejecutar la aplicación Django
        return django_app(environ, start_response)
        
    except Exception as e:
        # Si Django falla, mostrar página informativa con el error
        error_detail = str(e)
        import traceback
        error_traceback = traceback.format_exc()
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Inventario - Error de Django</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            min-height: 100vh; 
            color: white; 
            padding: 20px;
        }}
        .container {{ 
            max-width: 1000px; 
            margin: 0 auto; 
            padding: 40px 20px; 
        }}
        .header {{ 
            text-align: center; 
            margin-bottom: 40px; 
        }}
        .logo {{ 
            font-size: 3rem; 
            margin-bottom: 20px; 
            font-weight: bold; 
        }}
        .card {{ 
            background: rgba(255, 255, 255, 0.1); 
            backdrop-filter: blur(10px); 
            border-radius: 16px; 
            padding: 30px; 
            margin: 20px 0; 
            border: 1px solid rgba(255, 255, 255, 0.2); 
        }}
        .error {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .code {{
            background: rgba(0, 0, 0, 0.4);
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            margin: 10px 0;
            overflow-x: auto;
            border: 1px solid rgba(255, 255, 255, 0.1);
            white-space: pre-wrap;
        }}
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            background: #dc3545;
        }}
        .btn {{ 
            display: inline-block; 
            padding: 12px 24px; 
            background: rgba(255, 255, 255, 0.2); 
            color: white; 
            text-decoration: none; 
            border-radius: 25px; 
            margin: 8px; 
            transition: all 0.3s ease; 
            border: 1px solid rgba(255, 255, 255, 0.3); 
        }}
        .solution {{
            background: rgba(40, 167, 69, 0.2);
            border: 1px solid rgba(40, 167, 69, 0.4);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">📦 Sistema de Inventario</div>
            <div style="font-size: 1.2rem; opacity: 0.9;">
                <span class="status-indicator"></span>
                Error de Configuración Django
            </div>
        </div>

        <div class="card">
            <h3>🚨 Error Detallado de Django</h3>
            <div class="error">
                <strong>Error principal:</strong>
                <div class="code">{error_detail}</div>
            </div>
            
            <h4>📋 Stack Trace Completo:</h4>
            <div class="code">{error_traceback}</div>
        </div>

        <div class="solution">
            <h3>🛠️ Posibles Soluciones</h3>
            <p><strong>1. Base de datos:</strong> Verificar acceso a /tmp/ en Vercel</p>
            <p><strong>2. Dependencias:</strong> Asegurar que todas las librerías están instaladas</p>
            <p><strong>3. Configuración:</strong> Revisar settings.py para Vercel</p>
            <p><strong>4. Permisos:</strong> Verificar permisos de escritura en filesystem</p>
        </div>

        <div class="card">
            <h4>� Próximos pasos:</h4>
            <ol style="margin: 15px 0; padding-left: 20px;">
                <li>Revisar logs de Vercel para más detalles</li>
                <li>Verificar configuración de variables de entorno</li>
                <li>Considerar usar base de datos externa (PostgreSQL)</li>
                <li>Simplificar configuración inicial</li>
            </ol>
            
            <div style="margin: 20px 0;">
                <a href="/" class="btn">� Recargar página</a>
                <a href="javascript:location.reload()" class="btn">🔁 Refrescar</a>
            </div>
        </div>

        <div style="text-align: center; margin-top: 40px; opacity: 0.8;">
            <p>🌟 Sistema Django en proceso de configuración</p>
            <p>Los errores nos ayudan a identificar y solucionar problemas específicos</p>
        </div>
    </div>
</body>
</html>""".encode('utf-8')
        
        start_response('500 Internal Server Error', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Cache-Control', 'no-cache, no-store, must-revalidate')
        ])
        return [html]

# Alias para compatibilidad
app = application
