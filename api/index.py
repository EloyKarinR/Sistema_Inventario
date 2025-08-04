def application(environ, start_response):
    """WSGI simplificado para Vercel - Modo de compatibilidad"""
    
    # HTML de respuesta con información del sistema
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Inventario Django - Vercel</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; 
            color: white; 
            padding: 20px;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 40px 20px; 
        }
        .header { 
            text-align: center; 
            margin-bottom: 40px; 
        }
        .logo { 
            font-size: 3.5rem; 
            margin-bottom: 20px; 
            font-weight: bold; 
        }
        .subtitle { 
            font-size: 1.4rem; 
            opacity: 0.9; 
            margin-bottom: 10px; 
        }
        .status {
            display: inline-block;
            background: rgba(40, 167, 69, 0.2);
            border: 1px solid rgba(40, 167, 69, 0.4);
            padding: 12px 24px;
            border-radius: 25px;
            font-weight: 500;
            margin: 20px 0;
        }
        .card { 
            background: rgba(255, 255, 255, 0.1); 
            backdrop-filter: blur(10px); 
            border-radius: 16px; 
            padding: 30px; 
            margin: 20px 0; 
            border: 1px solid rgba(255, 255, 255, 0.2); 
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: transform 0.3s ease, background 0.3s ease;
        }
        .feature:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
            display: block;
        }
        .btn { 
            display: inline-block; 
            padding: 15px 30px; 
            background: rgba(255, 255, 255, 0.2); 
            color: white; 
            text-decoration: none; 
            border-radius: 25px; 
            margin: 10px; 
            transition: all 0.3s ease; 
            border: 1px solid rgba(255, 255, 255, 0.3); 
            font-weight: 500;
        }
        .btn:hover { 
            background: rgba(255, 255, 255, 0.3); 
            transform: translateY(-2px); 
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .btn-primary {
            background: rgba(0, 123, 255, 0.3);
            border-color: rgba(0, 123, 255, 0.5);
        }
        .credentials { 
            background: rgba(0, 0, 0, 0.2); 
            padding: 20px; 
            border-radius: 10px; 
            margin: 25px 0;
            text-align: center;
        }
        .tech-stack {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
            margin: 20px 0;
        }
        .tech-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            opacity: 0.8;
            font-size: 0.9rem;
        }
        .warning {
            background: rgba(255, 193, 7, 0.2);
            border: 1px solid rgba(255, 193, 7, 0.4);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        @media (max-width: 768px) {
            .logo { font-size: 2.5rem; }
            .container { padding: 20px 15px; }
            .btn { padding: 12px 20px; margin: 5px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">📦 Sistema de Inventario</div>
            <div class="subtitle">Aplicación Django Empresarial</div>
            <div class="status">✅ Desplegado en Vercel Serverless</div>
        </div>

        <div class="warning">
            <h3>🔧 Estado Actual del Sistema</h3>
            <p><strong>Modo de Compatibilidad:</strong> La aplicación está ejecutándose en modo estático mientras configuramos Django completo para Vercel serverless.</p>
            <p><strong>Funcionalidades:</strong> Base de datos, autenticación y vistas están siendo configuradas para el entorno serverless.</p>
        </div>

        <div class="card">
            <h2 style="text-align: center; margin-bottom: 30px;">🚀 Características del Sistema</h2>
            
            <div class="grid">
                <div class="feature">
                    <div class="feature-icon">📋</div>
                    <h3>Gestión de Inventario</h3>
                    <p>Control completo de productos, stock, categorías y proveedores</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🛒</div>
                    <h3>Sistema de Ventas</h3>
                    <p>Facturación, punto de venta y gestión de clientes integrada</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">📊</div>
                    <h3>Reportes Avanzados</h3>
                    <p>Análisis de ventas, inventario y reportes financieros detallados</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">👥</div>
                    <h3>Gestión de Usuarios</h3>
                    <p>Control de acceso, perfiles y seguimiento de actividad</p>
                </div>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <h3>🔗 Acceso al Sistema (Próximamente)</h3>
                <div style="margin: 25px 0;">
                    <a href="/admin/" class="btn btn-primary">🔐 Panel de Administración</a>
                    <a href="/panel_control/" class="btn">📱 Dashboard Principal</a>
                    <a href="/productos/" class="btn">📦 Gestión de Productos</a>
                    <a href="/ventas/" class="btn">🛒 Módulo de Ventas</a>
                </div>
            </div>

            <div class="credentials">
                <h3>🔑 Credenciales del Sistema</h3>
                <p style="margin: 10px 0;"><strong>Usuario:</strong> <code>admin</code></p>
                <p style="margin: 10px 0;"><strong>Contraseña:</strong> <code>admin123</code></p>
                <small style="opacity: 0.8;">Credenciales de demostración para el entorno de pruebas</small>
            </div>
        </div>

        <div class="card">
            <h3 style="text-align: center; margin-bottom: 20px;">🛠️ Stack Tecnológico</h3>
            <div class="tech-stack">
                <span class="tech-item">Django 5.1.3</span>
                <span class="tech-item">Python 3.9</span>
                <span class="tech-item">SQLite</span>
                <span class="tech-item">Vercel Serverless</span>
                <span class="tech-item">Bootstrap UI</span>
                <span class="tech-item">Chart.js</span>
            </div>
            <p style="text-align: center; margin-top: 20px; opacity: 0.9;">
                Arquitectura moderna y escalable para gestión empresarial
            </p>
        </div>

        <div class="footer">
            <p>🌟 Sistema de Inventario Profesional | Desarrollado con Django</p>
            <p>Desplegado en Vercel | Optimizado para alto rendimiento</p>
        </div>
    </div>
</body>
</html>""".encode('utf-8')
    
    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Cache-Control', 'no-cache, no-store, must-revalidate'),
        ('Pragma', 'no-cache'),
        ('Expires', '0')
    ])
    return [html]

# Alias para Vercel
app = application
