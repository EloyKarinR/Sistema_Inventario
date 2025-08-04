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

def application(environ, start_response):
    """WSGI application que intenta cargar Django"""
    
    try:
        # Intentar cargar Django
        import django
        from django.conf import settings
        
        # Solo configurar Django una vez
        if not settings.configured:
            django.setup()
        
        # Importar la aplicación WSGI de Django
        from django.core.wsgi import get_wsgi_application
        django_app = get_wsgi_application()
        
        # Ejecutar la aplicación Django
        return django_app(environ, start_response)
        
    except Exception as e:
        # Si Django falla, mostrar página informativa con el error
        error_detail = str(e)
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Inventario - Configurando Django</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            background: rgba(255, 193, 7, 0.2);
            border: 1px solid rgba(255, 193, 7, 0.4);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .code {{
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            margin: 10px 0;
            overflow-x: auto;
            border: 1px solid rgba(255, 255, 255, 0.1);
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
        .btn:hover {{ 
            background: rgba(255, 255, 255, 0.3); 
            transform: translateY(-2px); 
        }}
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        .status-loading {{ background: #ffc107; }}
        .status-error {{ background: #dc3545; }}
        .progress {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">📦 Sistema de Inventario</div>
            <div style="font-size: 1.2rem; opacity: 0.9;">
                <span class="status-indicator status-loading"></span>
                Configurando Django para Vercel...
            </div>
        </div>

        <div class="progress">
            <h3>🔧 Estado de Inicialización</h3>
            <p><strong>Paso actual:</strong> Cargando aplicación Django en entorno serverless</p>
            <p><strong>Problema detectado:</strong> Configuración de Django necesita ajustes para Vercel</p>
        </div>

        <div class="card">
            <h3>🚨 Detalles del Error de Django</h3>
            <div class="error">
                <strong>Error de inicialización:</strong>
                <div class="code">{error_detail}</div>
            </div>
            
            <h4>📋 Posibles causas:</h4>
            <ul style="margin: 15px 0; padding-left: 20px;">
                <li>Dependencias de Django no instaladas en Vercel</li>
                <li>Base de datos SQLite temporal no accesible</li>
                <li>Configuración de paths o imports</li>
                <li>Variables de entorno no configuradas</li>
            </ul>
        </div>

        <div class="card">
            <h3>🛠️ Próximos pasos para activar Django</h3>
            <div style="background: rgba(0, 123, 255, 0.2); padding: 20px; border-radius: 10px; margin: 15px 0;">
                <p><strong>1.</strong> Instalar dependencias Django en requirements.txt</p>
                <p><strong>2.</strong> Configurar base de datos para Vercel serverless</p>
                <p><strong>3.</strong> Ajustar configuración de archivos estáticos</p>
                <p><strong>4.</strong> Configurar migraciones automáticas</p>
            </div>
            
            <h4>🔗 URLs que estarán disponibles:</h4>
            <div style="margin: 20px 0;">
                <a href="/admin/" class="btn">🔐 Panel Admin</a>
                <a href="/panel_control/" class="btn">📱 Dashboard</a>
                <a href="/productos/" class="btn">📦 Productos</a>
                <a href="/ventas/" class="btn">🛒 Ventas</a>
            </div>
            
            <div style="background: rgba(40, 167, 69, 0.2); padding: 15px; border-radius: 8px; margin: 20px 0;">
                <strong>🔑 Credenciales una vez configurado:</strong><br>
                Usuario: <code>admin</code> | Contraseña: <code>admin123</code>
            </div>
        </div>

        <div style="text-align: center; margin-top: 40px; opacity: 0.8;">
            <p>🌟 Sistema Django configurándose para Vercel Serverless</p>
            <p>La aplicación estará disponible una vez completada la configuración</p>
        </div>
    </div>
</body>
</html>""".encode('utf-8')
        
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Cache-Control', 'no-cache, no-store, must-revalidate')
        ])
        return [html]

# Alias para compatibilidad
app = application
