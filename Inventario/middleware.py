from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from .models import Profile

class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            Profile.objects.filter(user=request.user).update(last_seen=timezone.now())
        return self.get_response(request)


class DemoModeMiddleware:
    """
    Middleware para restringir ciertas acciones en modo demo
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs que están bloqueadas para el usuario demo
        self.blocked_patterns = [
            'eliminar',
            'delete',
            'borrar',
            'admin',
        ]

    def __call__(self, request):
        # Verificar si es usuario demo
        if (hasattr(request, 'user') and 
            request.user.is_authenticated and 
            request.user.username == 'demo'):
            
            # Verificar URLs bloqueadas
            current_path = request.path.lower()
            
            if any(pattern in current_path for pattern in self.blocked_patterns):
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({
                        'status': 'error',
                        'mensaje': 'Acción no permitida en modo demo'
                    })
                else:
                    messages.warning(request, '🧪 Modo Demo: Esta acción no está permitida')
                    return redirect('Inventario:panel_control')
            
            # Verificar métodos destructivos
            if request.method in ['DELETE']:
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({
                        'status': 'error',
                        'mensaje': 'No se pueden eliminar datos en modo demo'
                    })
                else:
                    messages.warning(request, '🧪 Modo Demo: No se pueden eliminar datos')
                    return redirect('Inventario:panel_control')

        response = self.get_response(request)
        return response 