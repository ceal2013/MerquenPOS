from django.shortcuts import render, redirect
from django.contrib import messages
from . import services

def seleccion_mesas_view(request):
    if 'usuario_activo' not in request.session:
        messages.error(request, "Debe iniciar sesión para ver las mesas.")
        return redirect('login')
        
    usuario = request.session['usuario_activo']
    puntos_bd = services.getPuntosVenta()
    
    if not puntos_bd:
        return render(request, 'POS/mesas.html', {'error': 'No hay puntos de venta configurados.'})

    # Empaquetamos todo junto de forma limpia
    puntos_con_mesas = []
    for punto in puntos_bd:
        mesas_del_punto = services.getEstadoMesas(punto['codigo'])
        puntos_con_mesas.append({
            'codigo': punto['codigo'],
            'nombre': punto['nombre'],
            'mesas': mesas_del_punto # Las mesas van guardadas dentro de su propio punto
        })

    return render(request, 'POS/mesas.html', {
        'usuario': usuario,
        'puntos_con_mesas': puntos_con_mesas,
        'nombre_local': services.obtener_nombre_local() 
    })