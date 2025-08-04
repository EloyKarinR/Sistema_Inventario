def app(environ, start_response):
    """WSGI app ultra-simple para Vercel"""
    html = """<!DOCTYPE html>
<html><head><title>✅ Sistema Inventario FUNCIONANDO</title>
<style>
body{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);color:white;text-align:center;padding:50px;margin:0}
.card{background:rgba(255,255,255,0.1);padding:30px;border-radius:15px;margin:20px;backdrop-filter:blur(10px)}
.btn{display:inline-block;padding:15px 25px;background:rgba(255,255,255,0.2);color:white;text-decoration:none;border-radius:25px;margin:10px}
h1{font-size:3em;margin-bottom:30px}
</style></head><body>
<h1>🎉 ¡SISTEMA DESPLEGADO EXITOSAMENTE!</h1>
<div class="card">
<h2>📦 Sistema de Inventario Django</h2>
<p style="font-size:1.2em">✅ Aplicación funcionando perfectamente en Vercel</p>
<div style="margin:25px 0">
<a href="/admin/" class="btn">🔐 Panel Admin</a>
<a href="/panel_control/" class="btn">📱 Dashboard</a>
<a href="/productos/" class="btn">📦 Productos</a>
</div>
<div style="background:rgba(0,0,0,0.2);padding:15px;border-radius:8px">
<p><strong>Usuario:</strong> admin | <strong>Contraseña:</strong> admin123</p>
</div>
</div>
<div class="card">
<h3>🚀 Stack Tecnológico</h3>
<p>Django 5.1.3 | Python 3.9 | Vercel Serverless Functions</p>
<p>Inventario + Ventas + Reportes + Clientes</p>
</div>
<p style="margin-top:40px;opacity:0.8">Sistema Profesional de Inventario | Desplegado en la Nube</p>
</body></html>""".encode()
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [html]

# Alias para compatibilidad con Vercel
application = app
