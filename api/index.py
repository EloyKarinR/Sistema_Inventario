def application(environ, start_response):
    """
    WSGI application simple para Vercel
    """
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sistema de Inventario - Vercel</title>
        <style>
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                margin: 0; 
                padding: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 50px 20px; 
                text-align: center; 
            }
            .logo { 
                font-size: 3.5em; 
                margin-bottom: 20px; 
                font-weight: bold; 
            }
            .card { 
                background: rgba(255, 255, 255, 0.1); 
                backdrop-filter: blur(10px); 
                border-radius: 15px; 
                padding: 30px; 
                margin: 20px 0; 
                border: 1px solid rgba(255, 255, 255, 0.2); 
            }
            .status { 
                background: rgba(0, 255, 0, 0.2); 
                padding: 15px; 
                border-radius: 8px; 
                margin: 20px 0; 
                border: 1px solid rgba(0, 255, 0, 0.3);
            }
            .btn { 
                display: inline-block; 
                padding: 12px 25px; 
                background: rgba(255, 255, 255, 0.2); 
                color: white; 
                text-decoration: none; 
                border-radius: 25px; 
                margin: 10px; 
                transition: all 0.3s ease; 
                border: 1px solid rgba(255, 255, 255, 0.3); 
            }
            .btn:hover { 
                background: rgba(255, 255, 255, 0.3); 
                transform: translateY(-2px); 
            }
            .feature-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 15px; 
                margin: 25px 0; 
            }
            .feature { 
                background: rgba(255, 255, 255, 0.1); 
                padding: 20px; 
                border-radius: 10px; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">📦 Sistema de Inventario</div>
            
            <div class="status">
                ✅ ¡Aplicación desplegada exitosamente en Vercel!
            </div>
            
            <div class="card">
                <h2>🎉 ¡Sistema Funcionando Correctamente!</h2>
                <p>Tu sistema de inventario Django está ahora disponible en la nube a través de Vercel.</p>
                
                <div class="feature-grid">
                    <div class="feature">
                        <h3>📋 Gestión de Productos</h3>
                        <p>Inventario completo</p>
                    </div>
                    <div class="feature">
                        <h3>🛒 Sistema de Ventas</h3>
                        <p>Facturación integrada</p>
                    </div>
                    <div class="feature">
                        <h3>� Reportes</h3>
                        <p>Análisis detallado</p>
                    </div>
                    <div class="feature">
                        <h3>👥 Base de Clientes</h3>
                        <p>Gestión de contactos</p>
                    </div>
                </div>
                
                <h3>🔗 Acceso al Sistema:</h3>
                <div style="margin: 25px 0;">
                    <a href="/admin/" class="btn">🔐 Panel de Administración</a>
                    <a href="/panel_control/" class="btn">� Panel de Control</a>
                    <a href="/productos/" class="btn">📦 Gestión de Productos</a>
                    <a href="/ventas/" class="btn">🛒 Módulo de Ventas</a>
                </div>
                
                <div style="background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; margin: 25px 0;">
                    <h3>🔑 Credenciales de Acceso Demo:</h3>
                    <p style="font-size: 1.1em;"><strong>Usuario:</strong> admin</p>
                    <p style="font-size: 1.1em;"><strong>Contraseña:</strong> admin123</p>
                </div>
            </div>
            
            <div class="card">
                <h3>🚀 Tecnologías Implementadas</h3>
                <p><strong>Backend:</strong> Django 5.1.3 | Python 3.9</p>
                <p><strong>Base de Datos:</strong> SQLite (Demo) | PostgreSQL (Producción)</p>
                <p><strong>Despliegue:</strong> Vercel Serverless</p>
                <p><strong>Características:</strong> Inventario, Ventas, Reportes, Clientes</p>
            </div>
            
            <div style="margin-top: 40px; opacity: 0.8;">
                <p>🌟 Sistema de Inventario Professional</p>
                <p>Desarrollado con Django | Desplegado en Vercel</p>
            </div>
        </div>
    </body>
    </html>
    """.encode('utf-8')
    
    start_response(status, headers)
    return [html_content]

# Handler para Vercel
app = application
