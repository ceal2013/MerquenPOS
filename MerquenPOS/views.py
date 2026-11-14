from django.shortcuts import render, redirect
from django.core.cache import cache
from POS import services # Importamos las consultas SQL desde tu app

MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_SECONDS = 60

def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')

def login_global_view(request):

    nombre_local = services.obtener_nombre_local()

    # Si el usuario hace clic en el botón "Entrar"
    if request.method == 'POST':
        usuario_digitado = (request.POST.get('usuario') or '').strip()
        clave_digitada = request.POST.get('password') or ''

        client_ip = _get_client_ip(request)
        cache_key = f"login_attempts:{client_ip}:{usuario_digitado.lower()}"
        intentos = cache.get(cache_key, 0)

        if intentos >= MAX_LOGIN_ATTEMPTS:
            usuarios_bd = services.obtener_usuarios_activos()
            return render(request, 'login.html', {
                'usuarios': usuarios_bd,
                'nombre_local': nombre_local,
                'error': 'Demasiados intentos fallidos. Espere 1 minuto antes de volver a intentar.'
            })
        
        datos_usuario = services.verificar_login(usuario_digitado, clave_digitada)
        
        if datos_usuario:
            cache.delete(cache_key)
            # Mejora de seguridad: Rotamos la clave de sesión para prevenir "session fixation".
            # Esto genera un nuevo ID de sesión, invalidando el anterior.
            request.session.cycle_key()
            
            # Guardamos el nombre del local en la sesión para no consultarlo en cada vista.
            request.session['nombre_local'] = nombre_local

            # Ahora guardamos los datos del usuario en la nueva sesión segura.
            request.session['usuario_activo'] = datos_usuario
            # Lo enviamos a las mesas (crearemos esta ruta en el futuro)
            return redirect('seleccion_mesas') 
        else:
            cache.set(cache_key, intentos + 1, LOGIN_LOCKOUT_SECONDS)
            # Falla: recargamos la página con error
            usuarios_bd = services.obtener_usuarios_activos()
            return render(request, 'login.html', {
                'usuarios': usuarios_bd,
                'nombre_local': nombre_local,
                'error': 'Contraseña incorrecta o usuario inválido.'
            })
            
    # Carga inicial de la página
    usuarios_bd = services.obtener_usuarios_activos()
    return render(request, 'login.html', {
        'usuarios': usuarios_bd,
        'nombre_local': nombre_local 
    })

def logout_global(request):
    """
    Destruye la sesión actual del usuario y lo devuelve al login.
    """
    # flush() elimina todos los datos de la sesión y la cookie del navegador
    request.session.flush() 
    
    # Redirigimos a la pantalla de inicio de sesión
    return redirect('login')