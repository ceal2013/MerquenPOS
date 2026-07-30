from django.shortcuts import render, redirect
from POS import services # Importamos las consultas SQL desde tu app

def login_global_view(request):

    nombre_local = services.obtener_nombre_local()

    # Si el usuario hace clic en el botón "Entrar"
    if request.method == 'POST':
        usuario_digitado = request.POST.get('usuario')
        clave_digitada = request.POST.get('password')
        
        datos_usuario = services.verificar_login(usuario_digitado, clave_digitada)
        
        if datos_usuario:
            # Mejora de seguridad: Rotamos la clave de sesión para prevenir "session fixation".
            # Esto genera un nuevo ID de sesión, invalidando el anterior.
            request.session.cycle_key()
            
            # Ahora guardamos los datos del usuario en la nueva sesión segura.
            request.session['usuario_activo'] = datos_usuario
            # Lo enviamos a las mesas (crearemos esta ruta en el futuro)
            return redirect('seleccion_mesas') 
        else:
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