from django.db import connection

def obtener_nombre_local():
    """
    Va a la tabla ValoresPOS y rescata el nombre del restaurante.
    Usamos TOP 1 por si acaso hay más de una fila de configuración.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT TOP 1 NCliente FROM ValoresPOS")
            fila = cursor.fetchone()
            if fila and fila[0]:
                return fila[0].strip() # .strip() limpia los espacios en blanco sobrantes
            return "Nombre del Local no configurado"
        except Exception:
            return "Restaurante"

def obtener_usuarios_activos():
    """Trae todos los usuarios vigentes para el combobox."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT Nombre FROM Usuarios WHERE Vigente = 'S' ORDER BY Nombre")
        usuarios = [{'nombre': fila[0]} for fila in cursor.fetchall()]
        return usuarios

def verificar_login(nombre_usuario, password):
    """Valida credenciales en SQL Server."""
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
    """Obtiene la fecha de proceso y el turno activo."""
    with connection.cursor() as cursor:
        try:
            # Seleccionamos el último turno abierto o el activo
            cursor.execute("SELECT TOP 1 FechaProceso, Turno FROM Turno ORDER BY FechaProceso DESC")
            fila = cursor.fetchone()
            if fila:
                fecha = fila[0]
                numero_turno = str(fila[1]).strip()
                
                # Transformamos el número a texto
                nombres_turnos = {
                    '1': 'Desayuno',
                    '2': 'Almuerzo',
                    '3': 'Cena'
                }
                texto_turno = nombres_turnos.get(numero_turno, f"Turno {numero_turno}")
                
                return {'fecha': fecha, 'turno_texto': texto_turno}
            return {'fecha': 'Sin Fecha', 'turno_texto': 'Sin Turno'}
        except Exception:
            return {'fecha': 'Error BD', 'turno_texto': 'Error BD'}
    
def getPuntosVenta():
    """Obtiene los sectores del local para armar las pestañas."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT Codigo, Nombre FROM Puntos ORDER BY Nombre")
        puntos = [{'codigo': fila[0], 'nombre': fila[1]} for fila in cursor.fetchall()]
        return puntos

def getEstadoMesas(codigoPunto):
    """Obtiene todas las mesas de un punto y fusiona las que tienen múltiples cuentas."""
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
        mesas_dict = {} # Usamos un diccionario para evitar duplicados
        
        for fila in cursor.fetchall():
            numeroMesa = fila[0].strip()
            estadoCta = fila[1]
            cuentaImpresa = fila[2]
            total = fila[3] if fila[3] else 0
            mesaBloqueada = fila[4]
            usuarioBloqueo = fila[5]
            nombreGarzon = fila[6]

            estadoVisual = 'libre'
            if estadoCta == '0':
                if cuentaImpresa == '1':
                    estadoVisual = 'impresa' 
                else:
                    estadoVisual = 'ocupada' 

            # LÓGICA ANTI-DUPLICADOS:
            if numeroMesa not in mesas_dict:
                # Si la mesa no existe, la creamos
                mesas_dict[numeroMesa] = {
                    'numero': numeroMesa,
                    'estado': estadoVisual,
                    'total': total,
                    'bloqueada': True if str(mesaBloqueada) == '1' else False,
                    'usuarioBloqueo': usuarioBloqueo.strip() if usuarioBloqueo else "",
                    'nombreGarzon': nombreGarzon.strip() if nombreGarzon else ""
                }
            else:
                # Si ya existe (tiene más de 1 cuenta), le damos prioridad al estado rojo (impresa)
                if estadoVisual == 'impresa':
                    mesas_dict[numeroMesa]['estado'] = 'impresa'
                elif estadoVisual == 'ocupada' and mesas_dict[numeroMesa]['estado'] == 'libre':
                    mesas_dict[numeroMesa]['estado'] = 'ocupada'
                
                mesas_dict[numeroMesa]['total'] += total
                
                # Si esta subcuenta tiene el nombre del garzón, lo guardamos
                if nombreGarzon and not mesas_dict[numeroMesa]['nombreGarzon']:
                    mesas_dict[numeroMesa]['nombreGarzon'] = nombreGarzon.strip()
            
        # Convertimos el diccionario de vuelta a una lista para enviarlo al HTML
        return list(mesas_dict.values())
    
def obtener_cuenta_activa(punto, numero_mesa):
    """Busca si la mesa ya tiene una cuenta abierta."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Folio FROM CtasMesas 
            WHERE Punto = %s AND Mesa = %s AND Status = '0'
        """, [punto, numero_mesa])
        fila = cursor.fetchone()
        return fila[0] if fila else None

def generar_nuevo_folio():
    """Obtiene el último folio de NumTables, le suma 1 y lo actualiza."""
    with connection.cursor() as cursor:
        # Obtenemos el último folio
        cursor.execute("SELECT MAX(CAST(Folio AS INT)) FROM NumTables")
        fila = cursor.fetchone()
        ultimo_folio = fila[0] if fila[0] else 0
        
        nuevo_folio_int = ultimo_folio + 1
        nuevo_folio_str = str(nuevo_folio_int).zfill(7) # Rellena con ceros, ej: '0001234'
        
        # Insertamos el nuevo folio en la tabla para reservarlo
        cursor.execute("INSERT INTO NumTables (Folio) VALUES (%s)", [nuevo_folio_str])
        
        return nuevo_folio_str

def obtener_garzon_usuario(usuario_id):
    """Obtiene el código del garzón asociado al usuario. 
       Si no tiene o es supervisor, retorna '000'."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT Garzon, Supervisor FROM Usuarios WHERE Id = %s", [usuario_id])
        fila = cursor.fetchone()
        if fila:
            garzon_cod = fila[0]
            es_supervisor = fila[1]
            if garzon_cod and garzon_cod.strip():
                return garzon_cod.strip()
            if es_supervisor == 'S': # O el valor que indique 'Sí' en tu BD
                return '000' 
        return '000' # Por defecto, si hay algún error o no tiene.

def crear_nueva_cuenta(punto, numero_mesa, usuario_id, cubiertos):
    """Crea el registro inicial en CtasMesas usando la fecha del Turno."""
    datos_turno = obtener_turno_activo()
    fecha_proceso = datos_turno['fecha']
    turno_actual = datos_turno['turno_texto'] 
    
    # Mapeo inverso temporal (si en BD guardan el número y no el texto)
    turno_bd = '1'
    if turno_actual == 'Almuerzo': turno_bd = '2'
    elif turno_actual == 'Cena': turno_bd = '3'

    nuevo_folio = generar_nuevo_folio()
    garzon_id = obtener_garzon_usuario(usuario_id)
    
    with connection.cursor() as cursor:
        # Nota: Se han quitado campos que no se deben enviar y se ha ajustado 'Cuenta' y 'sw'
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

def get_familias_punto(punto):
    """Obtiene las Familias que tienen grupos disponibles en un Punto de Venta."""
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
    """Obtiene los Grupos de una Familia específica para un Punto de Venta."""
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
    """Obtiene los Productos de un Grupo, cruzando con Tarifas para el precio."""
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
    
def obtener_cubiertos_cuenta(folio):
    """Obtiene la cantidad de cubiertos ingresados al abrir la cuenta."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT Cubiertos FROM CtasMesas WHERE Folio = %s AND Status = '0'", [folio])
        fila = cursor.fetchone()
        return fila[0] if fila else 1

def obtener_consumos_mesa(folio):
    """Obtiene los productos que ya fueron enviados a la cocina (guardados en BD)."""
    with connection.cursor() as cursor:
        # Hacemos JOIN con Productos para traer el Nombre real del plato
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
    """Inserta o actualiza (suma) un producto en Consumos con Flag = '0'"""
    datos_turno = obtener_turno_activo()
    fecha_proceso = datos_turno['fecha']
    turno_bd = '2' if datos_turno['turno_texto'] == 'Almuerzo' else ('3' if datos_turno['turno_texto'] == 'Cena' else '1')

    with connection.cursor() as cursor:
        # 1. VERIFICAR SI EL PRODUCTO YA EXISTE (y no ha sido comandado)
        cursor.execute("""
            SELECT SubIndice FROM Consumos 
            WHERE Folio = %s AND Producto = %s 
              AND (Flag = '0' OR Flag IS NULL OR Flag = '') 
              AND (sw IS NULL OR sw = '' OR sw = '0')
        """, [folio, producto])
        fila = cursor.fetchone()

        if fila:
            # SI EXISTE: Actualizamos sumando la cantidad
            subindice = fila[0]
            cursor.execute("""
                UPDATE Consumos 
                SET Cantidad = Cantidad + %s 
                WHERE SubIndice = %s
            """, [cantidad, subindice])
        else:
            # NO EXISTE: Hacemos el INSERT normal que ya tenías
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
    """Elimina físicamente de la BD un producto que AÚN NO ha sido comandado (Flag='0')"""
    with connection.cursor() as cursor:
        sql = """
            DELETE FROM Consumos 
            WHERE Folio = %s AND Producto = %s AND (Flag = '0' OR Flag IS NULL OR Flag = '')
        """
        cursor.execute(sql, [folio, producto])

def comandar_ticket(folio):
    """Pasa los productos nuevos de Flag '0' a '1' (Comandados)"""
    with connection.cursor() as cursor:
        sql = """
            UPDATE Consumos 
            SET Flag = '1' 
            WHERE Folio = %s AND (Flag = '0' OR Flag IS NULL OR Flag = '')
        """
        cursor.execute(sql, [folio])

def anular_cuenta(folio):
    """Anula la cuenta (sw='1') y libera la mesa (Status='1') si no hubo consumos"""
    with connection.cursor() as cursor:
        sql = "UPDATE CtasMesas SET sw = '1', Status = '1' WHERE Folio = %s"
        cursor.execute(sql, [folio])