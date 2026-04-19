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
    
    # Pre-cargamos la primera columna del catálogo dinámico
    familias = services.get_familias_punto(punto)
    
    # Obtenemos los datos de la cuenta activa
    cubiertos = services.obtener_cubiertos_cuenta(folio)
    consumos_previos = services.obtener_consumos_mesa(folio)
    
    # LÓGICA DE NEGOCIO: Mostrar el nombre real del Garzón (no del usuario del sistema)
    nombre_garzon = services.obtener_nombre_garzon(folio)
    
    return render(request, 'POS/comanda.html', {
        'punto': punto,
        'numero': numero,
        'folio': folio,
        'cubiertos': cubiertos,
        'familias': familias,
        'consumos_previos': consumos_previos,
        'usuario': usuario,
        'nombre_garzon': nombre_garzon, # Variable nueva para el ticket
        'fecha_proceso': datos_turno['fecha'],
        'turno_activo': datos_turno['turno_texto'],
        'nombre_local': services.obtener_nombre_local()
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
    """
    Recibe la orden desde JS de agregar un producto. 
    Llama al 'services.py' que agrupa cantidades si ya existe con Flag=0.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            folio = data.get('folio')
            punto = data.get('punto')
            clase = data.get('clase')
            grupo = data.get('grupo')
            producto = data.get('producto')
            precio = data.get('precio')
            cantidad = data.get('cantidad')
            
            usuario_id = request.session['usuario_activo']['id']
            
            services.agregar_producto_consumo(
                folio, punto, clase, grupo, producto, precio, cantidad, usuario_id
            )
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'bad_request'}, status=400)


@custom_login_required
def api_borrar_ticket(request):
    """
    Borra físicamente de la tabla Consumos el producto, 
    SI Y SOLO SI no ha sido comandado (Flag = '0' o vacío).
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        folio = data.get('folio')
        producto = data.get('producto')
        
        services.borrar_producto_consumo(folio, producto)
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