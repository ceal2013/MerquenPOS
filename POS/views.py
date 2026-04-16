from django.shortcuts import render, redirect
from django.contrib import messages
from . import services
from MerquenPOS.decorators import custom_login_required
from django.views.decorators.cache import never_cache

@custom_login_required
@never_cache
def seleccion_mesas_view(request):
    """
    Vista protegida. Solo se ejecuta si el decorador valida la sesión.
    """
    usuario = request.session['usuario_activo']
    puntos_bd = services.getPuntosVenta()
    
    if not puntos_bd:
        return render(request, 'POS/mesas.html', {'error': 'No hay puntos de venta configurados.'})

    puntos_con_mesas = []
    for punto in puntos_bd:
        mesas_del_punto = services.getEstadoMesas(punto['codigo'])
        puntos_con_mesas.append({
            'codigo': punto['codigo'],
            'nombre': punto['nombre'],
            'mesas': mesas_del_punto 
        })

    datos_turno = services.obtener_turno_activo()

    return render(request, 'POS/mesas.html', {
        'usuario': usuario,
        'puntos_con_mesas': puntos_con_mesas,
        'nombre_local': services.obtener_nombre_local(),
        'fecha_proceso': datos_turno['fecha'],
        'turno_activo': datos_turno['turno_texto']
    })