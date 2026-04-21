from django.db import connection

# =====================================================================
# BLOQUE 1: CONFIGURACIÓN GLOBAL Y LOGIN
# Maneja el acceso al sistema y variables del entorno del local.
# =====================================================================

def obtener_nombre_local():
    """
    Va a la tabla ValoresPOS y rescata el nombre del restaurante.
    Usamos TOP 1 por si hay varias filas de configuración antigua.
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
    """Trae todos los usuarios vigentes para el combobox del Login."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT Nombre FROM Usuarios WHERE Vigente = 'S' ORDER BY Nombre")
        usuarios = [{'nombre': fila[0]} for fila in cursor.fetchall()]
        return usuarios

def verificar_login(nombre_usuario, password):
    """Valida credenciales y rescata los permisos clave (Admin/Supervisor)."""
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
    """
    LÓGICA CRÍTICA: Jamás usar la fecha del sistema Windows.
    Siempre obtenemos la fecha contable del último Turno abierto en la BD.
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
    """Obtiene los sectores del local (Bar, Terraza, etc) para armar las pestañas."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT Codigo, Nombre FROM Puntos ORDER BY Nombre")
        puntos = [{'codigo': fila[0], 'nombre': fila[1]} for fila in cursor.fetchall()]
        return puntos

def getEstadoMesas(codigoPunto):
    """
    LÓGICA ANTI-DUPLICADOS: Cruza Mesas con CtasMesas y ControlMesas.
    Si una mesa tiene 3 cuentas divididas, las agrupa en 1 sola tarjeta en pantalla,
    dando prioridad al color rojo (estado 'impresa').
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
                g.Nombre AS NombreGarzon
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
    """Busca si la mesa ya tiene una cuenta abierta."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Folio FROM CtasMesas 
            WHERE Punto = %s AND Mesa = %s AND Status = '0'
        """, [punto, numero_mesa])
        fila = cursor.fetchone()
        return fila[0] if fila else None

def verificar_tiene_consumos(folio):
    """LÓGICA: Verifica si la mesa está 'Fantasma' (abierta pero sin productos)."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM Consumos WHERE Folio = %s AND (sw IS NULL OR sw = '' OR sw = '0')", [folio])
        return cursor.fetchone()[0] > 0

def generar_nuevo_folio():
    """Busca el último folio en NumTables, le suma 1, rellena con ceros (0000001) y reserva."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(CAST(Folio AS INT)) FROM NumTables")
        fila = cursor.fetchone()
        ultimo_folio = fila[0] if fila[0] else 0
        
        nuevo_folio_int = ultimo_folio + 1
        nuevo_folio_str = str(nuevo_folio_int).zfill(7) 
        
        cursor.execute("INSERT INTO NumTables (Folio) VALUES (%s)", [nuevo_folio_str])
        return nuevo_folio_str

def obtener_garzon_usuario(usuario_id):
    """
    REGLA DE NEGOCIO: Transforma el Usuario web en Código de Garzón.
    Si es un supervisor sin código propio, asigna venta directa ('000').
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
    """Cruza CtasMesas con Garzones para imprimir el nombre real en el Ticket."""
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
    """Obtiene la cantidad de personas sentadas en la mesa."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT Cubiertos FROM CtasMesas WHERE Folio = %s AND Status = '0'", [folio])
        fila = cursor.fetchone()
        return fila[0] if fila else 1

def crear_nueva_cuenta(punto, numero_mesa, usuario_id, cubiertos):
    """
    Genera el INSERT base en CtasMesas. 
    Se encarga de limpiar los campos (sw vacío, cuenta vacía, etc) según el estándar de Visual Basic.
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
    """Acción rápida para mesas vacías: Pone sw='1' y libera el Status."""
    with connection.cursor() as cursor:
        sql = "UPDATE CtasMesas SET sw = '1', Status = '1' WHERE Folio = %s"
        cursor.execute(sql, [folio])


# =====================================================================
# BLOQUE 4: CATÁLOGO DE MENÚ (Carga dinámica)
# Trae las familias, grupos y productos filtrados por Punto de Venta.
# =====================================================================

def get_familias_punto(punto):
    """REGLA DE NEGOCIO: Solo trae familias que estén habilitadas para el Punto (GrupoPuntos)."""
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
    """Devuelve los grupos de una familia que están vigentes."""
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
    """
    CRÍTICO: Cruza con la tabla Tarifas para obtener el valor real 
    del producto en este punto de venta específico. Ignora dados de baja.
    """
    with connection.cursor() as cursor:
        sql = """
            SELECT p.Producto, p.NProducto, t.Valor, p.Menu
            FROM Productos p
            JOIN Tarifas t ON p.Producto = t.Codigo AND p.Clase = t.Clase AND p.Grupo = t.Grupo
            WHERE p.Clase = %s AND p.Grupo = %s AND t.Punto = %s AND p.Baja <> 'S'
            ORDER BY p.NProducto
        """
        cursor.execute(sql, [clase, grupo, punto])
        return [{'codigo': f[0], 'nombre': f[1].strip(), 'precio': float(f[2]), 'es_menu': f[3] == '1'} for f in cursor.fetchall()]


# =====================================================================
# BLOQUE 5: GESTIÓN DE LA COMANDA (Consumos)
# Maneja la lectura, escritura y envío de platos a la tabla de Consumos.
# =====================================================================

def obtener_consumos_mesa(folio):
    """Obtiene los productos guardados. Excluye los anulados por supervisor (sw=1)."""
    with connection.cursor() as cursor:
        sql = """
            SELECT 
                c.Producto, p.NProducto, c.Valor, c.Cantidad, 
                c.Clase, c.Grupo, c.Nota
            FROM Consumos c
            JOIN Productos p ON c.Producto = p.Producto AND c.Clase = p.Clase AND c.Grupo = p.Grupo
            WHERE c.Folio = %s 
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
                'nota': fila[6].strip() if fila[6] else ''
            })
        return consumos
    
def agregar_producto_consumo(folio, punto, clase, grupo, producto, precio, cantidad, usuario_id):
    """
    LÓGICA UPSERT (OPTIMIZACIÓN):
    Si el producto ya existe en el ticket y no ha sido comandado (Flag=0), 
    le suma la cantidad (UPDATE). Si no existe, crea una línea nueva (INSERT).
    """
    datos_turno = obtener_turno_activo()
    fecha_proceso = datos_turno['fecha']
    turno_bd = '2' if datos_turno['turno_texto'] == 'Almuerzo' else ('3' if datos_turno['turno_texto'] == 'Cena' else '1')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT SubIndice FROM Consumos 
            WHERE Folio = %s AND Producto = %s 
              AND (Flag = '0' OR Flag IS NULL OR Flag = '') 
              AND (sw IS NULL OR sw = '' OR sw = '0')
        """, [folio, producto])
        fila = cursor.fetchone()

        if fila:
            subindice = fila[0]
            cursor.execute("""
                UPDATE Consumos 
                SET Cantidad = Cantidad + %s 
                WHERE SubIndice = %s
            """, [cantidad, subindice])
        else:
            cursor.execute("SELECT Mesa FROM CtasMesas WHERE Folio = %s", [folio])
            fila_mesa = cursor.fetchone()
            mesa = fila_mesa[0] if fila_mesa else ''

            cursor.execute("SELECT ISNULL(MAX(Indice), 0) + 1 FROM Consumos WHERE Folio = %s", [folio])
            nuevo_indice = cursor.fetchone()[0]

            sql = """
                INSERT INTO Consumos (
                    Punto, Mesa, Grupo, Producto, Cantidad, Valor, sw, Tipo, Docto,
                    Status, Folio, Fecha, Turno, Clase, Comanda, Flag,
                    Cuenta, Id, mClase, mGrupo, mCodigo, Indice, Valorreal,
                    Menu, Hora, Nota, Pc, ValorUsd, ValorUsdReal
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, '', '', '',
                    '0', %s, %s, %s, %s, '', '0',
                    '', %s, %s, %s, %s, %s, %s,
                    '0', CONVERT(varchar(5), GETDATE(), 108), '', 'WEB_POS', 0, 0
                )
            """
            cursor.execute(sql, [
                punto, mesa, grupo, producto, cantidad, precio,
                folio, fecha_proceso, turno_bd, clase,
                usuario_id, clase, grupo, producto, nuevo_indice, precio
            ])

def borrar_producto_consumo(folio, producto):
    """
    BORRADO FÍSICO: El garzón eliminó del carrito un producto que AÚN 
    no había sido enviado a la cocina (Flag='0').
    """
    with connection.cursor() as cursor:
        sql = """
            DELETE FROM Consumos 
            WHERE Folio = %s AND Producto = %s AND (Flag = '0' OR Flag IS NULL OR Flag = '')
        """
        cursor.execute(sql, [folio, producto])

def comandar_ticket(folio):
    """
    BOTÓN CONFIRMAR: Pasa todos los productos en espera (Flag='0') 
    al estado comandado (Flag='1'), bloqueando su eliminación por parte del garzón.
    """
    with connection.cursor() as cursor:
        sql = """
            UPDATE Consumos 
            SET Flag = '1' 
            WHERE Folio = %s AND (Flag = '0' OR Flag IS NULL OR Flag = '')
        """
        cursor.execute(sql, [folio])