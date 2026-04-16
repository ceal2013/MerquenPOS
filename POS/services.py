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

def crear_nueva_cuenta(punto, numero_mesa, garzon_id, cubiertos):
    """Crea el registro inicial en CtasMesas usando la fecha del Turno."""
    datos_turno = obtener_turno_activo() # Usamos la función que creamos antes
    fecha_proceso = datos_turno['fecha']
    turno_actual = datos_turno['turno_texto'] # Ojo: en tu BD quizás guardan 1, 2 o 3. Lo ajustamos si es necesario.
    
    # Mapeo inverso temporal (si en BD guardan el número y no el texto)
    turno_bd = '1'
    if turno_actual == 'Almuerzo': turno_bd = '2'
    elif turno_actual == 'Cena': turno_bd = '3'

    nuevo_folio = generar_nuevo_folio()
    
    with connection.cursor() as cursor:
        sql = """
            INSERT INTO CtasMesas (
                Punto, Mesa, Garzon, Cubiertos, Hora, Status, Tipo, Docto, 
                Fecha, Folio, Turno, Dscto, Cuenta, Hab, Cliente, Propina, 
                sw, Cuentas, Total, Convenio, Atencion, Habitacion, FolioCnv, 
                Sucursal, Paquete, Admin, CCosto, Personal, TotalPersonal, 
                Moneda, NombreCta, Usuario, Pc
            ) VALUES (
                %s, %s, %s, %s, CONVERT(varchar(5), GETDATE(), 108), '0', '', '', 
                %s, %s, %s, 0, '0', '', 'Paso', 0, 
                '0', 1, 0, 0, 0, 0, '', 
                '', 0, 0, 0, 0, 0, 
                'P', 'MESA ' + %s, %s, 'WEB_POS'
            )
        """
        cursor.execute(sql, [
            punto, numero_mesa, garzon_id, cubiertos, 
            fecha_proceso, nuevo_folio, turno_bd, 
            numero_mesa, garzon_id
        ])
        
    return nuevo_folio