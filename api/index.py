import os
import sys
import django
from pathlib import Path

# Agregar el directorio del proyecto al path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SistemaInventario.settings')
os.environ['VERCEL'] = '1'  # Activar configuración de Vercel

try:
    django.setup()
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
except Exception as e:
    # Si Django falla, mostrar página de error informativa
    def application(environ, start_response):
        html = f"""<!DOCTYPE html>
<html><head><title>⚠️ Error de Configuración</title>
<style>
body{{font-family:Arial;background:linear-gradient(135deg,#ff6b6b,#ee5a24);color:white;text-align:center;padding:50px;margin:0}}
.card{{background:rgba(255,255,255,0.1);padding:30px;border-radius:15px;margin:20px;backdrop-filter:blur(10px)}}
.error{{background:rgba(255,0,0,0.2);padding:15px;border-radius:8px;margin:20px;font-family:monospace;text-align:left}}
</style></head><body>
<h1>⚠️ Error en la Aplicación Django</h1>
<div class="card">
<h2>�️ Modo de Depuración</h2>
<p>La aplicación Django no pudo inicializarse correctamente.</p>
<div class="error">
Error: {str(e)}
</div>
<p><strong>Nota:</strong> Vercel necesita configuración adicional para Django completo.</p>
<p>Mostrando página estática mientras se resuelve...</p>
</div>
</body></html>""".encode('utf-8')
        
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return [html]

# Alias para compatibilidad
app = application
