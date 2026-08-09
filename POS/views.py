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

    # Mejora de rendimiento: Cargamos inicialmente solo las mesas del primer punto de venta.
    # Las mesas de los otros puntos se cargarán dinámicamente con AJAX al hacer clic en su pestaña.
    puntos_con_mesas = []
    if puntos_bd:
        # Cargamos el primero
        primer_punto = puntos_bd[0]
        mesas_primer_punto = services.getEstadoMesas(primer_punto['codigo'])
        puntos_con_mesas.append({
            'codigo': primer_punto['codigo'],
            'nombre': primer_punto['nombre'],
            'mesas': mesas_primer_punto
        })
        # Los demás se agregan vacíos, para ser llenados por JS
        for punto in puntos_bd[1:]:
            puntos_con_mesas.append({
                'codigo': punto['codigo'],
                'nombre': punto['nombre'],
                'mesas': [] # Se cargará con AJAX
        })

    datos_turno = services.obtener_turno_activo()

    return render(request, 'POS/mesas.html', {
        'usuario': usuario,
        'puntos_con_mesas': puntos_con_mesas,
        'nombre_local': request.session.get('nombre_local', 'Restaurante'),
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
                'nombre_local': request.session.get('nombre_local', 'Restaurante')
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
        'nombre_local': request.session.get('nombre_local', 'Restaurante')
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

    # Mejora de rendimiento y simplificación:
    # 1. Se obtiene el nombre del punto con una consulta específica en lugar de traerlos todos.
    # 2. Se agrupan 3 consultas (cubiertos, garzón, cuentas) en una sola llamada.
    nombre_punto = services.get_punto_nombre(punto)
    detalles_cuenta = services.obtener_detalles_cuenta(folio)
    consumos_previos = services.obtener_consumos_mesa(folio)

    return render(request, 'POS/comanda.html', {
        'punto': punto,
        'numero': numero,
        'folio': folio,
        'cubiertos': detalles_cuenta['cubiertos'],
        'familias': familias,
        'consumos_previos': consumos_previos,
        'cuentas_activas': detalles_cuenta['cuentas_activas'],
        'usuario': usuario,
        'nombre_garzon': detalles_cuenta['nombre_garzon'],
        'fecha_proceso': datos_turno['fecha'],
        'turno_activo': datos_turno['turno_texto'],
        'nombre_local': request.session.get('nombre_local', 'Restaurante'),
        'nombre_punto': nombre_punto
    })


# =====================================================================
# 2. ENDPOINTS AJAX - CARGA DINÁMICA DEL MENÚ (GET)
# =====================================================================

@custom_login_required
def api_get_mesas_punto(request, punto):
    """Devuelve el estado de las mesas para un punto de venta específico en formato JSON."""
    mesas = services.getEstadoMesas(punto)
    return JsonResponse({'mesas': mesas})


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

@custom_login_required
def api_opciones_menu(request, clase, grupo, producto):
    """Devuelve las opciones configuradas para un producto de tipo Menú."""
    opciones = services.obtener_opciones_menu(clase, grupo, producto)
    
    if not opciones:
        # Si no hay opciones, se devuelve un indicador para que el frontend lo sepa.
        return JsonResponse({'sin_opciones': True, 'opciones': {}})
        
    return JsonResponse({'sin_opciones': False, 'opciones': opciones})

@custom_login_required
def api_buscar_productos(request):
    """
    Busca productos por nombre y devuelve una lista en formato JSON.
    Recibe los parámetros 'q' (término de búsqueda) y 'punto' (punto de venta).
    """
    termino = request.GET.get('q', '')
    punto = request.GET.get('punto', '')

    if not termino or not punto:
        return JsonResponse({'productos': []})

    productos = services.buscar_productos_por_nombre(punto, termino)
    return JsonResponse({'productos': productos})

# =====================================================================
# 3. ENDPOINTS AJAX - ACCIONES DEL TICKET Y LA BD (POST)
# =====================================================================

@custom_login_required
def api_agregar_ticket(request):
    """Agrega un producto o un paquete de menú a la comanda."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            folio = data.get('folio')
            punto = data.get('punto')
            cuenta = data.get('cuenta', '1')
            usuario_id = request.session['usuario_activo']['id']

            producto_padre = data.get('producto_padre')
            opciones = data.get('opciones', [])

            # CORRECCIÓN: Se añade compatibilidad para el formato de producto individual.
            # Si no se recibe la estructura de 'producto_padre', se asume el formato antiguo
            # y se construye el diccionario esperado por el servicio.
            if not producto_padre:
                if 'producto' in data and 'clase' in data and 'grupo' in data:
                    producto_padre = {
                        'producto': data.get('producto'),
                        'clase': data.get('clase'),
                        'grupo': data.get('grupo'),
                        'precio': data.get('precio'),
                        'cantidad': data.get('cantidad'),
                        'nota': data.get('nota', '')
                    }
                else:
                    return JsonResponse({'status': 'error', 'message': 'El formato de datos del producto es incorrecto.'}, status=400)

            services.agregar_producto_consumo(
                folio=folio, punto=punto, cuenta=cuenta, usuario_id=usuario_id,
                producto_padre=producto_padre, opciones=opciones
            )
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
    """Llama al servicio para actualizar el campo Cuenta en Consumos usando el Indice."""
    if request.method == 'POST':
        data = json.loads(request.body)
        folio = data.get('folio')
        indice = data.get('indice')
        destino = data.get('cuenta_destino')
        
        services.mover_producto_cuenta(folio, indice, destino)
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
        cuenta = data.get('cuenta', '1')
        nota = data.get('nota', '')
        
        services.borrar_producto_consumo(folio, producto, clase, grupo, cuenta, nota)
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
        # MEJORA: Se cambia la función que se llama.
        # En lugar de usar la compleja 'anular_mesa_completa', que puede causar bloqueos
        # en mesas sin consumos, usamos 'anular_cuenta'. Esta función es más simple
        # y directa para este caso de uso, evitando la condición de carrera en la BD.
        services.anular_cuenta(data.get('folio'))
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad_request'}, status=400)

@custom_login_required
def api_get_variedades(request, clase, grupo, producto):
    """Devuelve las variedades disponibles para un producto específico."""
    variedades = services.obtener_variedades_producto(clase, grupo, producto)
    return JsonResponse({'variedades': variedades})