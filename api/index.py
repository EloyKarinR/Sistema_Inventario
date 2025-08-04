import os
import sys
import django
from django.core.wsgi import get_wsgi_application

# Añadir el directorio del proyecto al path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SistemaInventario.settings')

# Configurar Django
django.setup()

# Inicializar datos de demo si es la primera vez
try:
    from django.core.management import execute_from_command_line
    from django.db import connection
    
    # Ejecutar migraciones
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    
    # Crear datos de demo
    from init_demo_data import crear_datos_demo
    crear_datos_demo()
    
except Exception as e:
    print(f"Error inicializando datos: {e}")

application = get_wsgi_application()

# Handler para Vercel
app = application
