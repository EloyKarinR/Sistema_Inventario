import os
import sys
from django.core.wsgi import get_wsgi_application

# Añadir el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SistemaInventario.settings')

application = get_wsgi_application()

# Handler para Vercel
app = application
