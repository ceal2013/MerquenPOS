from django.shortcuts import render, redirect
from django.contrib import messages
from . import services

def seleccion_mesas_view(request):
    # SEGURIDAD: Verificamos si el usuario pasó por el Login
    if 'usuario_activo' not in request.session:
        messages.error(request, "Debe iniciar sesión para ver las mesas.")
        return redirect('login')
        
    usuario = request.session['usuario_activo']
    
    # 1. Traemos los puntos de venta (sectores)
    puntos_venta = services.getPuntosVenta()
    
    # 2. Si no hay puntos creados en BD, evitamos que se caiga
    if not puntos_venta:
        return render(request, 'POS/mesas.html', {'error': 'No hay puntos de venta configurados.'})

    # 3. Traemos TODAS las mesas de TODOS los puntos (lo organizaremos en el HTML)
    # Creamos un diccionario donde la 'llave' es el codigo del punto y el 'valor' es la lista de mesas
    mesas_por_punto = {}
    for punto in puntos_venta:
        codigo_punto = punto['codigo']
        mesas_del_punto = services.getEstadoMesas(codigo_punto)
        mesas_por_punto[codigo_punto] = mesas_del_punto

    return render(request, 'POS/mesas.html', {
        'usuario': usuario,
        'puntos_venta': puntos_venta,
        'mesas_por_punto': mesas_por_punto,
        # Opcional: le mandamos el nombre del local para mantener el branding
        'nombre_local': services.obtener_nombre_local() 
    })