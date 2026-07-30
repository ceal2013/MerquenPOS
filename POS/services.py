from django.db import connection

# =====================================================================
# BLOQUE 1: CONFIGURACIÓN GLOBAL Y LOGIN
# Maneja el acceso al sistema y variables del entorno del local.
# =====================================================================

def obtener_nombre_local():
    """Obtiene el nombre del local desde la base de datos.

    Busca en la tabla `ValoresPOS` el nombre del cliente/restaurante.
    Utiliza `TOP 1` para asegurar que solo se retorne un resultado,
    evitando problemas con configuraciones antiguas o duplicadas.

    Returns:
        str: El nombre del local, o un mensaje de error/default si no se encuentra.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT TOP 1 NCliente FROM ValoresPOS")
            fila = cursor.fetchone()
            if fila and fila[0]:
                return fila[0].strip() # .strip() limpia espacios en blanco sobrantes
            return "Nombre del Local no configurado"
        except Exception:
            return "Restaurante"

def obtener_usuarios_activos():
    """Obtiene una lista de usuarios activos.

    Consulta la tabla `Usuarios` para obtener los nombres de todos los usuarios
    cuyo estado es 'Vigente' ('S'). Los resultados se ordenan por nombre.

    Returns:
        list[dict]: Una lista de diccionarios, cada uno con la clave 'nombre'
                    y el nombre del usuario como valor.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT Nombre FROM Usuarios WHERE Vigente = 'S' ORDER BY Nombre")
        usuarios = [{'nombre': fila[0]} for fila in cursor.fetchall()]
        return usuarios

def verificar_login(nombre_usuario, password):
    """Verifica las credenciales de un usuario y recupera sus datos.

    Comprueba si el nombre de usuario y la contraseña coinciden con un registro
    vigente en la tabla `Usuarios`. Si la validación es exitosa, retorna
    un diccionario con los datos y permisos del usuario.

    Args:
        nombre_usuario (str): El nombre del usuario a validar.
        password (str): La contraseña del usuario.

    Returns:
        dict | None: Un diccionario con los datos del usuario ('id', 'nombre',
                     'cargo', 'es_admin', 'es_supervisor') si las credenciales
                     son correctas, o None si la validación falla.
    """
    with connection.cursor() as cursor:
        sql = """
            SELECT Id, Nombre, Cargo, Admin, Supervisor 
            FROM Usuarios 
            WHERE Nombre = %s AND Password = %s AND Vigente = 'S'
        """
        cursor.execute(sql, [nombre_usuario, password])
        fila = cursor.fetchone()
        
        if fila:
            return {
                'id': fila[0],
                'nombre': fila[1],
                'cargo': fila[2],
                'es_admin': fila[3],
                'es_supervisor': fila[4]
            }
        return None
    
def obtener_turno_activo():
    """Obtiene la fecha de proceso y el turno activo desde la base de datos.

    Consulta la tabla `Turno` para obtener el último turno registrado,
    ordenando por `FechaProceso` de forma descendente. Esto asegura que se
    utilice la fecha contable del sistema y no la del sistema operativo.

    Returns:
        dict: Un diccionario con 'fecha' y 'turno_texto'. En caso de error o
              si no hay turnos, retorna valores indicando la situación.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT TOP 1 FechaProceso, Turno FROM Turno ORDER BY FechaProceso DESC")
            fila = cursor.fetchone()
            if fila:
                fecha = fila[0]
                numero_turno = str(fila[1]).strip()
                
                # Mapeo visual para la pantalla
                nombres_turnos = {'1': 'Desayuno', '2': 'Almuerzo', '3': 'Cena'}
                texto_turno = nombres_turnos.get(numero_turno, f"Turno {numero_turno}")
                
                return {'fecha': fecha, 'turno_texto': texto_turno}
            return {'fecha': 'Sin Fecha', 'turno_texto': 'Sin Turno'}
        except Exception:
            return {'fecha': 'Error BD', 'turno_texto': 'Error BD'}

# =====================================================================
# BLOQUE 2: PLANO DE MESAS
# Dibuja la pantalla inicial y los estados de color de las mesas.
# =====================================================================

def getPuntosVenta():
    """Obtiene todos los puntos de venta configurados.

    Consulta la tabla `Puntos` para obtener una lista de todos los puntos de
    venta (sectores del local como 'Bar', 'Terraza', etc.).

    Returns:
        list[dict]: Una lista de diccionarios, donde cada uno representa un
                    punto de venta con su 'codigo' y 'nombre'.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT Codigo, Nombre FROM Puntos ORDER BY Nombre")
        puntos = [{'codigo': fila[0], 'nombre': fila[1]} for fila in cursor.fetchall()]
        return puntos

def getEstadoMesas(codigoPunto):
    """Obtiene el estado consolidado de todas las mesas de un punto de venta.

    Realiza una consulta compleja que une `Mesas`, `CtasMesas`, `ControlMesas`,
    `Usuarios` y `Garzones` para determinar el estado visual de cada mesa.
    Agrupa la información si una mesa tiene múltiples cuentas, sumando los
    totales y priorizando el estado más crítico (ej. 'impresa' sobre 'ocupada').

    Args:
        codigoPunto (str): El código del punto de venta a consultar.

    Returns:
        list[dict]: Una lista de diccionarios, cada uno representando el estado
                    de una mesa con detalles como 'numero', 'estado', 'total', etc.
    """
    with connection.cursor() as cursor:
        sql = """
            SELECT 
                m.Mesa,
                c.Status AS EstadoCta,
                c.Cuenta AS CuentaImpresa,
                c.Total,
                cm.Status AS MesaBloqueada,
                u.Nombre AS UsuarioBloqueo,
                g.Nombre AS NombreGarzon,
                c.Fecha,
                c.Hora
            FROM Mesas m
            LEFT JOIN CtasMesas c 
                ON m.Mesa = c.Mesa AND m.Punto = c.Punto AND c.Status = '0'
            LEFT JOIN ControlMesas cm 
                ON m.Mesa = cm.NumMesa AND m.Punto = cm.PVenta
            LEFT JOIN Usuarios u 
                ON cm.Usuario = u.Id
            LEFT JOIN Garzones g
                ON c.Garzon = g.Codigo
            WHERE m.Punto = %s
            ORDER BY LEN(m.Mesa), m.Mesa
        """
        cursor.execute(sql, [codigoPunto])
        mesas_dict = {} 
        
        for fila in cursor.fetchall():
            numeroMesa = fila[0].strip()
            estadoCta = fila[1]
            cuentaImpresa = fila[2]
            total = fila[3] if fila[3] else 0
            mesaBloqueada = fila[4]
            usuarioBloqueo = fila[5]
            nombreGarzon = fila[6]
            fecha_cta = fila[7]
            hora_cta = fila[8]

            # Definir estado visual base
            estadoVisual = 'libre'
            if estadoCta == '0':
                if cuentaImpresa == '1':
                    estadoVisual = 'impresa' 
                else:
                    estadoVisual = 'ocupada' 

            if numeroMesa not in mesas_dict:
                # 1ra vez que vemos la mesa: La creamos
                mesas_dict[numeroMesa] = {
                    'numero': numeroMesa,
                    'estado': estadoVisual,
                    'total': total,
                    'bloqueada': True if str(mesaBloqueada) == '1' else False,
                    'usuarioBloqueo': usuarioBloqueo.strip() if usuarioBloqueo else "",
                    'nombreGarzon': nombreGarzon.strip() if nombreGarzon else "",
                    'fecha': fecha_cta.strftime("%d/%m") if fecha_cta else "",
                    'hora': hora_cta if hora_cta else ""
                }
            else:
                # Ya existía (múltiples cuentas en 1 mesa): Priorizamos estado e incrementamos total
                if estadoVisual == 'impresa':
                    mesas_dict[numeroMesa]['estado'] = 'impresa'
                elif estadoVisual == 'ocupada' and mesas_dict[numeroMesa]['estado'] == 'libre':
                    mesas_dict[numeroMesa]['estado'] = 'ocupada'
                
                mesas_dict[numeroMesa]['total'] += total
                
                # Rescatamos el garzón si la primera cuenta no lo tenía
                if nombreGarzon and not mesas_dict[numeroMesa]['nombreGarzon']:
                    mesas_dict[numeroMesa]['nombreGarzon'] = nombreGarzon.strip()
            
        return list(mesas_dict.values())

# =====================================================================
# BLOQUE 3: GESTIÓN DE CUENTAS (Apertura, Cierre y Validaciones)
# Administra la tabla CtasMesas y generación de Folios.
# =====================================================================

def obtener_cuenta_activa(punto, numero_mesa):
    """Busca el folio de una cuenta activa para una mesa específica.

    Consulta la tabla `CtasMesas` para encontrar una cuenta con `Status = '0'`
    (activa) para la combinación de punto de venta y número de mesa.

    Args:
        punto (str): El código del punto de venta.
        numero_mesa (str): El número de la mesa.

    Returns:
        str | None: El número de folio si se encuentra una cuenta activa,
                    de lo contrario, None.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Folio FROM CtasMesas 
            WHERE Punto = %s AND Mesa = %s AND Status = '0'
        """, [punto, numero_mesa])
        fila = cursor.fetchone()
        return fila[0] if fila else None

def verificar_tiene_consumos(folio):
    """Verifica si una cuenta (folio) tiene productos consumidos.

    Cuenta el número de registros en la tabla `Consumos` para un folio dado
    que no estén marcados como anulados (sw='0' o nulo). Se usa para detectar
    mesas "fantasma" (abiertas sin consumo).

    Args:
        folio (str): El folio de la cuenta a verificar.

    Returns:
        bool: True si la cuenta tiene al menos un producto, False en caso contrario.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM Consumos WHERE Folio = %s AND (sw IS NULL OR sw = '' OR sw = '0')", [folio])
        return cursor.fetchone()[0] > 0

def generar_nuevo_folio():
    """Genera y reserva un nuevo número de folio único.

    Obtiene el máximo folio de la tabla `NumTables`, le suma 1, y lo formatea
    a una cadena de 7 dígitos rellenando con ceros a la izquierda.
    Finalmente, inserta el nuevo folio en `NumTables` para reservarlo.

    Returns:
        str: El nuevo número de folio generado (ej: '0000001').
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(CAST(Folio AS INT)) FROM NumTables")
        fila = cursor.fetchone()
        ultimo_folio = fila[0] if fila[0] else 0
        
        nuevo_folio_int = ultimo_folio + 1
        nuevo_folio_str = str(nuevo_folio_int).zfill(7) 
        
        cursor.execute("INSERT INTO NumTables (Folio) VALUES (%s)", [nuevo_folio_str])
        return nuevo_folio_str

def obtener_garzon_usuario(usuario_id):
    """Obtiene el código de garzón asociado a un ID de usuario.

    Busca en la tabla `Usuarios` el código de garzón correspondiente a un
    ID de usuario. Si el usuario es supervisor y no tiene un código de garzón
    asignado, se le asigna el código '000' (venta directa).

    Args:
        usuario_id (int): El ID del usuario.

    Returns:
        str: El código de garzón asociado o '000' por defecto.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT Garzon, Supervisor FROM Usuarios WHERE Id = %s", [usuario_id])
        fila = cursor.fetchone()
        if fila:
            garzon_cod = fila[0]
            es_supervisor = fila[1]
            if garzon_cod and garzon_cod.strip():
                return garzon_cod.strip()
            if es_supervisor == 'S': 
                return '000' 
        return '000'

def obtener_nombre_garzon(folio):
    """Obtiene el nombre del garzón asignado a una cuenta.

    A partir de un folio, consulta `CtasMesas` para obtener el código del garzón
    y luego lo cruza con la tabla `Garzones` para obtener su nombre.

    Args:
        folio (str): El folio de la cuenta.

    Returns:
        str: El nombre del garzón o 'Sin Garzón' si no se encuentra.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT g.Nombre 
            FROM CtasMesas c
            JOIN Garzones g ON c.Garzon = g.Codigo
            WHERE c.Folio = %s
        """, [folio])
        fila = cursor.fetchone()
        return fila[0].strip() if fila else 'Sin Garzón'

def obtener_cubiertos_cuenta(folio):
    """Obtiene la cantidad de cubiertos registrados para una cuenta.

    Consulta la tabla `CtasMesas` para obtener el número de cubiertos
    de una cuenta activa (`Status = '0'`) a partir de su folio.

    Args:
        folio (str): El folio de la cuenta.

    Returns:
        int: La cantidad de cubiertos, o 1 por defecto si no se encuentra.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT Cubiertos FROM CtasMesas WHERE Folio = %s AND Status = '0'", [folio])
        fila = cursor.fetchone()
        return fila[0] if fila else 1

def crear_nueva_cuenta(punto, numero_mesa, usuario_id, cubiertos):
    """Crea un nuevo registro de cuenta en la tabla `CtasMesas`.

    Genera un nuevo folio, obtiene los datos del turno activo y el código de
    garzón, y luego inserta una nueva fila en `CtasMesas` para abrir una
    nueva cuenta en una mesa.

    Args:
        punto (str): Código del punto de venta.
        numero_mesa (str): Número de la mesa.
        usuario_id (int): ID del usuario que abre la mesa.
        cubiertos (int): Cantidad de comensales.

    Returns:
        str: El folio de la nueva cuenta creada.
    """
    datos_turno = obtener_turno_activo()
    fecha_proceso = datos_turno['fecha']
    turno_actual = datos_turno['turno_texto'] 
    
    # Mapeo a BD (Por si se guarda número de turno y no nombre)
    turno_bd = '1'
    if turno_actual == 'Almuerzo': turno_bd = '2'
    elif turno_actual == 'Cena': turno_bd = '3'

    nuevo_folio = generar_nuevo_folio()
    garzon_id = obtener_garzon_usuario(usuario_id)
    
    with connection.cursor() as cursor:
        sql = """
            INSERT INTO CtasMesas (
                Punto, Mesa, Garzon, Cubiertos, Hora, Status, Tipo, Docto, 
                Fecha, Folio, Turno, Dscto, Cuenta, Hab, Propina, 
                sw, Cuentas, Total, Convenio, Atencion, Habitacion, FolioCnv, 
                Sucursal, Paquete, Admin, CCosto, Personal, TotalPersonal, 
                Moneda
            ) VALUES (
                %s, %s, %s, %s, CONVERT(varchar(5), GETDATE(), 108), '0', '', '', 
                %s, %s, %s, 0, '', '', 0, 
                '', 1, 0, 0, 0, 0, '', 
                '', 0, 0, 0, 0, 0, 
                'P'
            )
        """
        cursor.execute(sql, [
            punto, numero_mesa, garzon_id, cubiertos, 
            fecha_proceso, nuevo_folio, turno_bd
        ])
        
    return nuevo_folio

def anular_cuenta(folio):
    """Anula una cuenta específica, típicamente una que está vacía.

    Actualiza el registro en `CtasMesas` para un folio dado, estableciendo
    `sw = '1'` y `Status = '1'` para marcarla como anulada y liberada.

    Args:
        folio (str): El folio de la cuenta a anular.
    """
    with connection.cursor() as cursor:
        sql = "UPDATE CtasMesas SET sw = '1', Status = '1' WHERE Folio = %s"
        cursor.execute(sql, [folio])

def actualizar_cubiertos_cuenta(folio, cantidad):
    """Actualiza la cantidad de cubiertos para una cuenta activa.

    Modifica el campo `Cubiertos` en la tabla `CtasMesas` para un folio
    dado, siempre que la cuenta esté activa (`Status = '0'`).

    Args:
        folio (str): El folio de la cuenta a actualizar.
        cantidad (int): El nuevo número de cubiertos.
    """
    with connection.cursor() as cursor:
        sql = "UPDATE CtasMesas SET Cubiertos = %s WHERE Folio = %s AND Status = '0'"
        cursor.execute(sql, [cantidad, folio])

def obtener_cuentas_folio(folio):
    """Obtiene los números de las sub-cuentas activas para un folio.

    Consulta `CtasMesas` para un folio específico y `Status = '0'`,
    y retorna una lista con los identificadores de cada sub-cuenta ('Cuentas').

    Args:
        folio (str): El folio principal de la mesa.

    Returns:
        list[str]: Una lista de strings, donde cada string es el número
                   de una sub-cuenta activa.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT Cuentas FROM CtasMesas WHERE Folio = %s AND Status = '0' ORDER BY CAST(Cuentas AS INT)", [folio])
        return [str(fila[0]).strip() for fila in cursor.fetchall()]

def crear_cuenta_extra(folio):
    """Crea una sub-cuenta adicional para una mesa ya abierta.

    Clona el registro principal de `CtasMesas` para un folio dado,
    asignándole un nuevo número de sub-cuenta (`Cuentas`) que es el
    máximo actual + 1.

    Args:
        folio (str): El folio de la mesa para la cual se creará la sub-cuenta.

    Returns:
        str: El número de la nueva sub-cuenta creada.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT ISNULL(MAX(CAST(Cuentas AS INT)), 0) + 1 FROM CtasMesas WHERE Folio = %s", [folio])
        nueva_cuenta = str(cursor.fetchone()[0])
        
        sql_clone = """
            INSERT INTO CtasMesas (
                Punto, Mesa, Garzon, Cubiertos, Hora, Status, Tipo, Docto, 
                Fecha, Folio, Turno, Dscto, Cuenta, Hab, Propina, 
                sw, Cuentas, Total, Convenio, Atencion, Habitacion, FolioCnv, 
                Sucursal, Paquete, Admin, CCosto, Personal, TotalPersonal, Moneda
            )
            SELECT TOP 1 
                Punto, Mesa, Garzon, Cubiertos, CONVERT(varchar(5), GETDATE(), 108), Status, Tipo, Docto, 
                Fecha, Folio, Turno, Dscto, Cuenta, Hab, Propina, 
                sw, %s, 0, Convenio, Atencion, Habitacion, FolioCnv, 
                Sucursal, Paquete, Admin, CCosto, Personal, TotalPersonal, Moneda
            FROM CtasMesas WHERE Folio = %s AND Status = '0'
        """
        cursor.execute(sql_clone, [nueva_cuenta, folio])
        return nueva_cuenta

def verificar_estado_ocupacion(punto, numero):
    """Verifica si una mesa activa está vacía (sin consumos).

    Primero, encuentra el folio activo de la mesa. Luego, comprueba si ese
    folio tiene algún producto registrado en la tabla `Consumos`.

    Args:
        punto (str): El código del punto de venta.
        numero (str): El número de la mesa.

    Returns:
        dict | None: Un diccionario con el 'folio' y un booleano 'vacia'
                     si la mesa está activa. Retorna None si la mesa no
                     tiene una cuenta activa.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT Folio FROM CtasMesas WHERE Punto = %s AND Mesa = %s AND Status = '0'", [punto, numero])
        fila_folio = cursor.fetchone()
        if not fila_folio:
            return None
        
        folio = fila_folio[0]
        cursor.execute("SELECT COUNT(*) FROM Consumos WHERE Folio = %s AND Status = '0' AND (sw IS NULL OR sw = '' OR sw = '0')", [folio])
        tiene_productos = cursor.fetchone()[0] > 0
        
        return {'folio': folio, 'vacia': not tiene_productos}

def anular_mesa_completa(folio):
    """Anula todas las sub-cuentas vacías asociadas a un folio.

    Actualiza el estado a 'anulada' (`Status='1'`, `sw='1'`) en `CtasMesas`
    para todas las sub-cuentas de un folio que no tengan ningún producto
    registrado en la tabla `Consumos`.

    Args:
        folio (str): El folio de la mesa cuyas sub-cuentas vacías se anularán.
    """
    with connection.cursor() as cursor:
        sql = """
            UPDATE CtasMesas 
            SET Status = '1', sw = '1' 
            WHERE Folio = %s 
              AND LTRIM(RTRIM(Cuentas)) NOT IN (
                  SELECT DISTINCT LTRIM(RTRIM(ISNULL(Cuenta, '1'))) 
                  FROM Consumos 
                  WHERE Folio = %s
              )
        """
        # Le pasamos el folio dos veces (uno para el UPDATE y otro para el SELECT interno)
        cursor.execute(sql, [folio, folio])

# =====================================================================
# BLOQUE 4: CATÁLOGO DE MENÚ (Carga dinámica)
# Trae las familias, grupos y productos filtrados por Punto de Venta.
# =====================================================================

def get_familias_punto(punto):
    """Obtiene las familias de productos disponibles para un punto de venta.

    Consulta las tablas `Familias` y `GrupoPuntos` para retornar solo
    aquellas familias de productos que están explícitamente habilitadas
    para el punto de venta especificado.

    Args:
        punto (str): El código del punto de venta.

    Returns:
        list[dict]: Una lista de diccionarios, cada uno representando una
                    familia con su 'clase' (código) y 'nombre'.
    """
    with connection.cursor() as cursor:
        sql = """
            SELECT DISTINCT f.Clase, f.NClase
            FROM Familias f
            JOIN GrupoPuntos gp ON f.Clase = gp.Clase
            WHERE gp.Punto = %s
            ORDER BY f.NClase
        """
        cursor.execute(sql, [punto])
        return [{'clase': f[0], 'nombre': f[1].strip()} for f in cursor.fetchall()]

def get_grupos_punto(punto, clase):
    """Obtiene los grupos de productos vigentes para una familia y punto de venta.

    Consulta las tablas `Grupos` y `GrupoPuntos` para retornar los grupos
    que pertenecen a una familia, están habilitados para un punto de venta
    y se encuentran vigentes (`Vigente = 'S'`).

    Args:
        punto (str): El código del punto de venta.
        clase (str): El código de la familia de productos.

    Returns:
        list[dict]: Una lista de diccionarios, cada uno representando un
                    grupo con su 'grupo' (código) y 'nombre'.
    """
    with connection.cursor() as cursor:
        sql = """
            SELECT g.Grupo, g.NGrupo
            FROM Grupos g
            JOIN GrupoPuntos gp ON g.Grupo = gp.Grupo AND g.Clase = gp.Clase
            WHERE gp.Punto = %s AND g.Clase = %s AND g.Vigente = 'S'
            ORDER BY g.NGrupo
        """
        cursor.execute(sql, [punto, clase])
        return [{'grupo': f[0], 'nombre': f[1].strip()} for f in cursor.fetchall()]

def get_productos_grupo(punto, clase, grupo):
    """Obtiene los productos de un grupo con precios específicos del punto de venta.

    Consulta la tabla `Productos` y la une con `Tarifas` para obtener el
    precio correcto. Si existe una tarifa específica para el punto de venta,
    se usa ese precio; de lo contrario, se usa el precio base del producto.

    Args:
        punto (str): El código del punto de venta para buscar tarifas.
        clase (str): El código de la familia del producto.
        grupo (str): El código del grupo del producto.

    Returns:
        list[dict]: Una lista de diccionarios, cada uno representando un
                    producto con 'codigo', 'nombre', 'precio' y 'es_menu'.
    """
    with connection.cursor() as cursor:
        sql = """
            SELECT 
                p.Producto, 
                p.NProducto, 
                ISNULL(t.Valor, p.Valor) AS PrecioUnitario, 
                p.Menu
            FROM Productos p
            LEFT JOIN Tarifas t 
                ON p.Producto = t.Codigo 
                AND p.Clase = t.Clase 
                AND p.Grupo = t.Grupo 
                AND t.Punto = %s
            WHERE p.Clase = %s 
              AND p.Grupo = %s 
              AND p.Baja <> 'S'
            ORDER BY p.NProducto
        """
        cursor.execute(sql, [punto, clase, grupo])
        return [{'codigo': f[0], 'nombre': f[1].strip(), 'precio': float(f[2]), 'es_menu': f[3] == '1'} for f in cursor.fetchall()]


# =====================================================================
# BLOQUE 5: GESTIÓN DE LA COMANDA (Consumos)
# Maneja la lectura, escritura y envío de platos a la tabla de Consumos.
# =====================================================================

def obtener_consumos_mesa(folio):
    """Obtiene todos los productos consumidos y no pagados de una cuenta.

    Recupera de la tabla `Consumos` todos los ítems asociados a un folio que
    tienen `Status = '0'` (no pagado) y no están anulados. Incluye información
    sobre si el ítem ya fue comandado (`Flag`).

    Args:
        folio (str): El folio de la cuenta a consultar.

    Returns:
        list[dict]: Una lista de diccionarios, cada uno representando un
                    producto consumido con sus detalles.
    """
    with connection.cursor() as cursor:
        sql = """
            SELECT 
                c.Producto, p.NProducto, c.Valor, c.Cantidad, 
                c.Clase, c.Grupo, c.Nota, c.Cuenta, c.Flag
            FROM Consumos c
            JOIN Productos p ON c.Producto = p.Producto AND c.Clase = p.Clase AND c.Grupo = p.Grupo
            WHERE c.Folio = %s 
              AND c.Status = '0'
              AND (c.sw IS NULL OR c.sw = '' OR c.sw = '0') 
            ORDER BY c.SubIndice
        """
        cursor.execute(sql, [folio])
        consumos = []
        for fila in cursor.fetchall():
            consumos.append({
                'codigo': fila[0].strip(),
                'nombre': fila[1].strip(),
                'precio': float(fila[2]),
                'cantidad': float(fila[3]),
                'clase': fila[4].strip(),
                'grupo': fila[5].strip(),
                'nota': fila[6].strip() if fila[6] else '',
                'cuenta': str(fila[7]).strip() if fila[7] else '1',
                'flag': str(fila[8]).strip() if fila[8] else '0'
            })
        return consumos
    
def agregar_producto_consumo(folio, punto, clase, grupo, producto, precio, cantidad, usuario_id, cuenta='1'):
    """Agrega un producto a la comanda (tabla Consumos) o actualiza su cantidad.

    Si el producto (en la misma sub-cuenta) ya existe en la comanda y no ha
    sido comandado (`Flag='0'`), incrementa su cantidad. De lo contrario,
    inserta un nuevo registro en la tabla `Consumos`.

    Args:
        folio (str): Folio de la cuenta.
        punto (str): Código del punto de venta.
        clase (str): Código de la familia del producto.
        grupo (str): Código del grupo del producto.
        producto (str): Código del producto.
        precio (float): Precio del producto.
        cantidad (float): Cantidad a agregar.
        usuario_id (int): ID del usuario que agrega el producto.
        cuenta (str, optional): Número de la sub-cuenta. Defaults to '1'.
    """
    datos_turno = obtener_turno_activo()
    fecha_proceso = datos_turno['fecha']
    turno_bd = '2' if datos_turno['turno_texto'] == 'Almuerzo' else ('3' if datos_turno['turno_texto'] == 'Cena' else '1')

    with connection.cursor() as cursor:
        # Filtramos por Cuenta para no mezclar un mismo producto en cuentas separadas
        cursor.execute("""
            SELECT SubIndice FROM Consumos 
            WHERE Folio = %s AND Producto = %s AND Clase = %s AND Grupo = %s 
              AND Cuenta = %s
              AND (Flag = '0' OR Flag IS NULL OR Flag = '') 
              AND (sw IS NULL OR sw = '' OR sw = '0')
        """, [folio, producto, clase, grupo, cuenta])
        fila = cursor.fetchone()

        if fila:
            subindice = fila[0]
            cursor.execute("UPDATE Consumos SET Cantidad = Cantidad + %s WHERE SubIndice = %s", [cantidad, subindice])
        else:
            cursor.execute("SELECT Mesa FROM CtasMesas WHERE Folio = %s", [folio])
            fila_mesa = cursor.fetchone()
            mesa = fila_mesa[0] if fila_mesa else ''

            # Inyectamos el valor 'cuenta' en el campo 'Cuenta' de Consumos
            sql_insert = """
                INSERT INTO Consumos (
                    Punto, Mesa, Grupo, Producto, Cantidad, Valor, sw, Tipo, Docto,
                    Status, Folio, Fecha, Turno, Clase, Comanda, Flag,
                    Cuenta, Id, mClase, mGrupo, mCodigo, Indice, Valorreal,
                    Menu, Hora, Nota, Pc, ValorUsd, ValorUsdReal
                ) 
                OUTPUT INSERTED.SubIndice
                VALUES (
                    %s, %s, %s, %s, %s, %s, '', '', '',
                    '0', %s, %s, %s, %s, '', '0',
                    %s, %s, %s, %s, %s, 0, %s,
                    '0', CONVERT(varchar(5), GETDATE(), 108), '', 'WEB_POS', 0, 0
                )
            """
            cursor.execute(sql_insert, [
                punto, mesa, grupo, producto, cantidad, precio,
                folio, fecha_proceso, turno_bd, clase,
                cuenta, usuario_id, clase, grupo, producto, precio
            ])
            
            subindice_generado = cursor.fetchone()[0]
            if subindice_generado:
                cursor.execute("UPDATE Consumos SET Indice = %s WHERE SubIndice = %s", [subindice_generado, subindice_generado])

def borrar_producto_consumo(folio, producto, clase, grupo):
    """Elimina un producto de la comanda si aún no ha sido comandado.

    Borra un registro de la tabla `Consumos` que coincida con los parámetros
    proporcionados, solo si su `Flag` es '0' o nulo (no comandado).

    Args:
        folio (str): Folio de la cuenta.
        producto (str): Código del producto a borrar.
        clase (str): Código de la familia del producto.
        grupo (str): Código del grupo del producto.
    """
    with connection.cursor() as cursor:
        sql = """
            DELETE FROM Consumos 
            WHERE Folio = %s 
              AND Producto = %s 
              AND Clase = %s 
              AND Grupo = %s 
              AND (Flag = '0' OR Flag IS NULL OR Flag = '')
        """
        cursor.execute(sql, [folio, producto, clase, grupo])

def comandar_ticket(folio):
    """Procesa el envío de productos a las áreas de preparación (cocina, bar, etc.).

    1. Selecciona todos los productos de un folio que no han sido comandados (`Flag='0'`).
    2. Para cada producto, determina las áreas de despacho (ej. 'PCocina', 'PBar')
       según los campos `Despacho` y `Despacho2` de la tabla `Productos`.
    3. Inserta los productos en las tablas de despacho correspondientes para que
       sean procesados por los sistemas de impresión.
    4. Actualiza el `Flag` a '1' en `Consumos` para todos los productos procesados,
       marcando que ya fueron enviados a preparación.

    Args:
        folio (str): El folio de la cuenta a comandar.
    """
    # Diccionario de destinos: Mapea el número de Despacho con la tabla real
    destinos_impresion = {
        1: 'PCocina',
        2: 'PBar',
        3: 'PParrilla',
        4: 'PReposteria',
        5: 'PFrio'
    }

    def parse_despacho(valor):
        """Función interna para evitar errores si el Despacho viene vacío o con letras"""
        try:
            return int(valor)
        except (ValueError, TypeError):
            return 0

    with connection.cursor() as cursor:
        
        # PASO 1: Obtener productos no comandados y cruzar con la tabla Productos
        sql_nuevos = """
            SELECT 
                c.Indice, c.SubIndice, c.Cantidad, c.Folio, c.Nota,
                p.NProducto, p.Menu, p.Despacho, p.Despacho2
            FROM Consumos c
            JOIN Productos p ON c.Producto = p.Producto AND c.Clase = p.Clase AND c.Grupo = p.Grupo
            WHERE c.Folio = %s AND (c.Flag = '0' OR c.Flag IS NULL OR c.Flag = '')
        """
        cursor.execute(sql_nuevos, [folio])
        productos_a_despachar = cursor.fetchall()

        # PASO 2: Repartir cada producto a sus áreas de impresión
        for prod in productos_a_despachar:
            indice = prod[0]
            subindice = prod[1]
            cantidad = prod[2]
            folio_consumo = prod[3]
            nota = prod[4] if prod[4] else ''
            nombre_producto = prod[5]
            es_menu = prod[6]
            desp1 = parse_despacho(prod[7])
            desp2 = parse_despacho(prod[8])

            # Usamos un 'Set' (conjunto) para evitar que si desp1 y desp2 son iguales, 
            # se imprima dos veces en la misma zona.
            tablas_a_insertar = set()
            if desp1 in destinos_impresion:
                tablas_a_insertar.add(destinos_impresion[desp1])
            if desp2 in destinos_impresion:
                tablas_a_insertar.add(destinos_impresion[desp2])

            # Insertamos en cada tabla requerida
            for nombre_tabla in tablas_a_insertar:
                # Al armar SQL dinámico, el nombre de la tabla no puede ser un parámetro %s por seguridad/sintaxis,
                # se inyecta directamente con f-strings (esto es seguro porque viene de nuestro propio diccionario hardcodeado)
                sql_insert_despacho = f"""
                    INSERT INTO {nombre_tabla} 
                    (Indice, SubIndice, Nproducto, Cantidad, folio, menu, nota)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert_despacho, [
                    indice, subindice, nombre_producto, cantidad, 
                    folio_consumo, es_menu, nota
                ])

        # PASO 3: BOTÓN CONFIRMAR: Cambia todo a Flag '1' (Comandados) bloqueándolos para el garzón
        sql_update_flag = """
            UPDATE Consumos 
            SET Flag = '1' 
            WHERE Folio = %s AND (Flag = '0' OR Flag IS NULL OR Flag = '')
        """
        cursor.execute(sql_update_flag, [folio])

def mover_producto_cuenta(folio, producto, clase, grupo, cuenta_origen, cuenta_destino):
    """Mueve un producto de una sub-cuenta a otra dentro de la misma mesa.

    Actualiza el campo `Cuenta` de un registro en la tabla `Consumos`,
    efectivamente moviendo el ítem de una sub-cuenta de origen a una de destino.
    Funciona para ítems comandados y no comandados.

    Args:
        folio (str): El folio de la mesa.
        producto (str): Código del producto a mover.
        clase (str): Código de la familia del producto.
        grupo (str): Código del grupo del producto.
        cuenta_origen (str): La sub-cuenta de origen del producto.
        cuenta_destino (str): La sub-cuenta de destino del producto.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE Consumos 
            SET Cuenta = %s 
            WHERE Folio = %s AND Producto = %s AND Clase = %s AND Grupo = %s AND Cuenta = %s 
              AND (sw IS NULL OR sw = '' OR sw = '0')
        """, [cuenta_destino, folio, producto, clase, grupo, cuenta_origen])