from django.shortcuts import render, redirect
from POS import services # Importamos las consultas SQL desde tu app

def login_global_view(request):
    # Si el usuario hace clic en el botón "Entrar"
    if request.method == 'POST':
        usuario_digitado = request.POST.get('usuario')
        clave_digitada = request.POST.get('password')
        
        datos_usuario = services.verificar_login(usuario_digitado, clave_digitada)
        
        if datos_usuario:
            # Guardamos los datos en la sesión
            request.session['usuario_activo'] = datos_usuario
            # Lo enviamos a las mesas (crearemos esta ruta en el futuro)
            return redirect('seleccion_mesas') 
        else:
            # Falla: recargamos la página con error
            usuarios_bd = services.obtener_usuarios_activos()
            return render(request, 'login.html', {
                'usuarios': usuarios_bd, 
                'error': 'Contraseña incorrecta o usuario inválido.'
            })
            
    # Carga inicial de la página
    usuarios_bd = services.obtener_usuarios_activos()
    return render(request, 'login.html', {'usuarios': usuarios_bd})