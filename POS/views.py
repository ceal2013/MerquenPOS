from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
import json

from . import services
from MerquenPOS.decorators import custom_login_required

# =====================================================================
# 1. VISTAS PRINCIPALES (PANTALLAS)
# =====================================================================

@custom_login_required
@never_cache
def seleccion_mesas_view(request):
    """
    ========================================================
    PANTALLA: PLANO DE MESAS
    Muestra los Puntos de Venta y sus respectivas mesas.
    ========================================================
    """
    usuario = request.session['usuario_activo']
    puntos_bd = services.getPuntosVenta()
    
    if not puntos_bd:
        return render(request, 'POS/mesas.html', {'error': 'No hay puntos de venta configurados.'})

    # Lógica: Agrupamos las mesas por su punto de venta correspondiente para las pestañas
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
    """
    ========================================================
    LÓGICA: LA PUERTA DE ENTRADA A LA MESA (Doble Clic)
    Decide a dónde enviar al usuario dependiendo del Status.
    ========================================================
    """
    usuario = request.session['usuario_activo']
    
    # 1. Verificamos si la mesa YA tiene una cuenta abierta (Status = '0')
    folio_activo = services.obtener_cuenta_activa(punto, numero)
    
    if folio_activo:
        # LÓGICA DE NEGOCIO: "Mesas Fantasmas"
        # Si la mesa está abierta pero no le cargaron productos, el doble clic debe preguntar si anula.
        tiene_consumos = services.verificar_tiene_consumos(folio_activo)
        
        if not tiene_consumos:
            # Si envían el formulario de confirmación (POST)
            if request.method == 'POST':
                if request.POST.get('accion') == 'anular':
                    services.anular_cuenta(folio_activo) # sw='1', libera mesa
                    return redirect('seleccion_mesas')
                else:
                    return redirect('comanda', punto=punto, numero=numero, folio=folio_activo)
            
            # Si es GET, mostramos la alerta de Mesa Vacía
            return render(request, 'POS/confirmar_anulacion.html', {
                'punto': punto, 'numero': numero, 'folio': folio_activo,
                'nombre_local': services.obtener_nombre_local()
            })
            
        # Si la mesa está abierta Y TIENE PRODUCTOS, entra directo a la comanda
        return redirect('comanda', punto=punto, numero=numero, folio=folio_activo)

    # 2. LÓGICA DE MESA LIBRE: Si envían los cubiertos (POST), creamos la cuenta nueva
    if request.method == 'POST':
        cubiertos = request.POST.get('cubiertos', 1)
        # Enviamos el ID del usuario; el 'services.py' se encargará de buscar el Código de Garzón o usar '000'
        id_usuario = usuario['id'] 
        
        nuevo_folio = services.crear_nueva_cuenta(punto, numero, id_usuario, cubiertos)
        return redirect('comanda', punto=punto, numero=numero, folio=nuevo_folio)

    # 3. LÓGICA DE MESA LIBRE (GET): Mostramos el teclado numérico de cubiertos
    return render(request, 'POS/cubiertos.html', {
        'punto': punto,
        'numero': numero,
        'nombre_local': services.obtener_nombre_local()
    })


@never_cache
@custom_login_required
def comanda_view(request, punto, numero, folio):
    """
    ========================================================
    PANTALLA: TOMA DE PEDIDOS (COMANDA)
    Carga todos los datos necesarios para operar el lado cliente.
    ========================================================
    """
    usuario = request.session['usuario_activo']
    datos_turno = services.obtener_turno_activo()
    
    familias = services.get_familias_punto(punto)
    nombre_punto = next((p['nombre'] for p in services.getPuntosVenta() if p['codigo'] == punto), "Punto de Venta")
    
    cubiertos = services.obtener_cubiertos_cuenta(folio)
    consumos_previos = services.obtener_consumos_mesa(folio)
    nombre_garzon = services.obtener_nombre_garzon(folio)
    
    # Obtener listado de cuentas activas para este folio
    cuentas_activas = services.obtener_cuentas_folio(folio)
    if not cuentas_activas:
        cuentas_activas = ['1']
    
    return render(request, 'POS/comanda.html', {
        'punto': punto,
        'numero': numero,
        'folio': folio,
        'cubiertos': cubiertos,
        'familias': familias,
        'consumos_previos': consumos_previos,
        'cuentas_activas': cuentas_activas,
        'usuario': usuario,
        'nombre_garzon': nombre_garzon,
        'fecha_proceso': datos_turno['fecha'],
        'turno_activo': datos_turno['turno_texto'],
        'nombre_local': services.obtener_nombre_local(),
        'nombre_punto': nombre_punto
    })


# =====================================================================
# 2. ENDPOINTS AJAX - CARGA DINÁMICA DEL MENÚ (GET)
# =====================================================================

@custom_login_required
def api_get_grupos(request, punto, clase):
    """Devuelve los Grupos de una Familia en formato JSON para no recargar la página"""
    grupos = services.get_grupos_punto(punto, clase)
    return JsonResponse({'grupos': grupos})

@custom_login_required
def api_get_productos(request, punto, clase, grupo):
    """Devuelve los Platos de un Grupo consultando precios según el Punto de Venta"""
    productos = services.get_productos_grupo(punto, clase, grupo)
    return JsonResponse({'productos': productos})


# =====================================================================
# 3. ENDPOINTS AJAX - ACCIONES DEL TICKET Y LA BD (POST)
# =====================================================================

@custom_login_required
def api_agregar_ticket(request):
    """Agrega un producto, ahora lee el parámetro 'cuenta' desde el JSON."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # ... rescatas tus variables antiguas y sumas la cuenta:
            folio, punto, clase, grupo = data.get('folio'), data.get('punto'), data.get('clase'), data.get('grupo')
            producto, precio, cantidad = data.get('producto'), data.get('precio'), data.get('cantidad')
            cuenta = data.get('cuenta', '1') # Capturamos la cuenta actual
            
            usuario_id = request.session['usuario_activo']['id']
            
            services.agregar_producto_consumo(folio, punto, clase, grupo, producto, precio, cantidad, usuario_id, cuenta)
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'bad_request'}, status=400)

@custom_login_required
def api_crear_cuenta(request):
    """Llama al servicio para clonar la CtasMesas y retorna el nuevo número."""
    if request.method == 'POST':
        data = json.loads(request.body)
        folio = data.get('folio')
        nueva_cuenta = services.crear_cuenta_extra(folio)
        return JsonResponse({'status': 'ok', 'nueva_cuenta': nueva_cuenta})
    return JsonResponse({'status': 'bad_request'}, status=400)

@custom_login_required
def api_mover_producto(request):
    """Llama al servicio para actualizar el campo Cuenta en Consumos."""
    if request.method == 'POST':
        data = json.loads(request.body)
        folio = data.get('folio')
        producto = data.get('producto')
        clase = data.get('clase')
        grupo = data.get('grupo')
        origen = data.get('cuenta_origen')
        destino = data.get('cuenta_destino')
        
        services.mover_producto_cuenta(folio, producto, clase, grupo, origen, destino)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad_request'}, status=400)


@custom_login_required
def api_borrar_ticket(request):
    """
    Recibe la orden del tacho de basura y borra el producto no comandado.
    Ahora utiliza Clase y Grupo para identificar unívocamente el ítem.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        folio = data.get('folio')
        producto = data.get('producto')
        clase = data.get('clase')
        grupo = data.get('grupo')
        
        services.borrar_producto_consumo(folio, producto, clase, grupo)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad_request'}, status=400)


@custom_login_required
def api_comandar_ticket(request):
    """
    Al dar clic en "Confirmar", cambia el Flag de '0' a '1' 
    en todos los productos nuevos de esta cuenta.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        folio = data.get('folio')
        
        services.comandar_ticket(folio)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad_request'}, status=400)


@custom_login_required
def api_anular_ticket(request):
    """
    Llamado interno cuando el garzón fuerza la anulación desde adentro 
    o desde la alerta si la mesa estaba vacía.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        folio = data.get('folio')
        
        services.anular_cuenta(folio)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad_request'}, status=400)

@custom_login_required
def api_actualizar_cubiertos(request):
    """
    Recibe la orden desde el Modal de la comanda para actualizar 
    la cantidad de cubiertos en tiempo real.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        folio = data.get('folio')
        cubiertos = data.get('cubiertos')
        
        services.actualizar_cubiertos_cuenta(folio, cubiertos)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad_request'}, status=400)

@custom_login_required
def api_verificar_mesa_vacia(request, punto, numero):
    """Devuelve JSON indicando si la mesa está vacía, para decidir si mostrar Modal de Anulación."""
    estado = services.verificar_estado_ocupacion(punto, numero)
    if not estado:
        return JsonResponse({'error': 'Mesa no activa'}, status=404)
    
    # Generamos la URL de la comanda para que JS sepa a dónde redirigir
    from django.urls import reverse
    url_comanda = reverse('comanda', args=[punto, numero, estado['folio']])
    
    return JsonResponse({
        'vacia': estado['vacia'],
        'url_comanda': url_comanda,
        'folio': estado['folio']
    })

@custom_login_required
def api_anular_mesa(request):
    """Recibe la orden del Modal para anular el folio completo."""
    if request.method == 'POST':
        data = json.loads(request.body)
        services.anular_mesa_completa(data.get('folio'))
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad_request'}, status=400)