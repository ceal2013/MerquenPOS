from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def custom_login_required(view_func):
    """
    Verifica la existencia de 'usuario_activo' en la sesión.
    Si no existe, redirige al login con un mensaje de error.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'usuario_activo' not in request.session:
            messages.error(request, "Debe iniciar sesión para acceder a esta sección.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view