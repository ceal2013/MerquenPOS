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
    
def getPuntosVenta():
    """Obtiene los sectores del local para armar las pestañas."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT Codigo, Nombre FROM Puntos ORDER BY Nombre")
        puntos = [{'codigo': fila[0], 'nombre': fila[1]} for fila in cursor.fetchall()]
        return puntos

def getEstadoMesas(codigoPunto):
    """Obtiene todas las mesas de un punto y cruza la información para saber su estado visual."""
    with connection.cursor() as cursor:
        sql = """
            SELECT 
                m.Mesa,
                c.Status AS EstadoCta,
                c.Cuenta AS CuentaImpresa,
                c.Total,
                cm.Status AS MesaBloqueada,
                u.Nombre AS UsuarioBloqueo
            FROM Mesas m
            LEFT JOIN CtasMesas c 
                ON m.Mesa = c.Mesa AND m.Punto = c.Punto AND c.Status = '0'
            LEFT JOIN ControlMesas cm 
                ON m.Mesa = cm.NumMesa AND m.Punto = cm.PVenta
            LEFT JOIN Usuarios u 
                ON cm.Usuario = u.Id
            WHERE m.Punto = %s
            ORDER BY CAST(m.Mesa AS INT)
        """
        cursor.execute(sql, [codigoPunto])
        mesas = []
        
        for fila in cursor.fetchall():
            numeroMesa = fila[0].strip() # Quitamos espacios sobrantes del código
            estadoCta = fila[1]
            cuentaImpresa = fila[2]
            total = fila[3] if fila[3] else 0
            mesaBloqueada = fila[4]
            usuarioBloqueo = fila[5]

            # Lógica de VB6 traspasada a Python para definir el color/estado de la mesa
            estadoVisual = 'libre'
            if estadoCta == '0':
                if cuentaImpresa == '1':
                    estadoVisual = 'impresa' # Mesa con cuenta impresa (Amarilla/Azul)
                else:
                    estadoVisual = 'ocupada' # Mesa con consumos activos (Roja)

            mesas.append({
                'numero': numeroMesa,
                'estado': estadoVisual,
                'total': total,
                'bloqueada': True if mesaBloqueada == 1 else False,
                'usuarioBloqueo': usuarioBloqueo.strip() if usuarioBloqueo else ""
            })
            
        return mesas