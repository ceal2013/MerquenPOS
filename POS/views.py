from django.shortcuts import render, redirect
from django.contrib import messages
from . import services
from MerquenPOS.decorators import custom_login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse

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

@never_cache
@custom_login_required
def abrir_mesa_view(request, punto, numero):
    usuario = request.session['usuario_activo']
    
    # 1. Verificamos si ya hay una cuenta abierta
    folio_activo = services.obtener_cuenta_activa(punto, numero)
    
    if folio_activo:
        # Si ya está abierta, redirigimos directamente a la comanda (la crearemos luego)
        return redirect('comanda', punto=punto, numero=numero, folio=folio_activo)

    # 2. Si la mesa está libre y envían el formulario con los cubiertos (POST)
    if request.method == 'POST':
        cubiertos = request.POST.get('cubiertos', 1)
        # OJO: Aquí asumimos que el id del garzón es el mismo del usuario. 
        # Si la tabla Usuarios tiene el código de Garzón en otro campo, debemos traerlo.
        id_garzon = usuario['id'] 
        
        nuevo_folio = services.crear_nueva_cuenta(punto, numero, id_garzon, cubiertos)
        return redirect('comanda', punto=punto, numero=numero, folio=nuevo_folio)

    # 3. Si la mesa está libre (GET), mostramos el teclado para preguntar cubiertos
    return render(request, 'POS/cubiertos.html', {
        'punto': punto,
        'numero': numero,
        'nombre_local': services.obtener_nombre_local()
    })

@never_cache
@custom_login_required
def comanda_view(request, punto, numero, folio):
    usuario = request.session['usuario_activo']
    
    # 1. Traer Familias disponibles para este punto
    familias = services.get_familias_punto(punto)
    
    # (Opcional) Puedes traer los productos ya consumidos de la mesa aquí
    # consumos = services.obtener_consumos_mesa(folio)
    
    return render(request, 'POS/comanda.html', {
        'punto': punto,
        'numero': numero,
        'folio': folio,
        'familias': familias,
        'nombre_local': services.obtener_nombre_local()
    })

@custom_login_required
def api_get_grupos(request, punto, clase):
    grupos = services.get_grupos_punto(punto, clase)
    return JsonResponse({'grupos': grupos})

@custom_login_required
def api_get_productos(request, punto, clase, grupo):
    productos = services.get_productos_grupo(punto, clase, grupo)
    return JsonResponse({'productos': productos})