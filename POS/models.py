# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Consumos(models.Model):
    punto = models.CharField(db_column='Punto', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    mesa = models.CharField(db_column='Mesa', max_length=4, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    grupo = models.CharField(db_column='Grupo', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    producto = models.CharField(db_column='Producto', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cantidad = models.DecimalField(db_column='Cantidad', max_digits=19, decimal_places=4)  # Field name made lowercase.
    valor = models.DecimalField(db_column='Valor', max_digits=19, decimal_places=4)  # Field name made lowercase.
    sw = models.CharField(db_column='SW', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    docto = models.CharField(db_column='Docto', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    folio = models.CharField(db_column='Folio', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    turno = models.CharField(db_column='Turno', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    clase = models.CharField(db_column='Clase', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    comanda = models.CharField(db_column='Comanda', max_length=10, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    flag = models.CharField(db_column='Flag', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    idanula = models.CharField(db_column='IdAnula', max_length=5, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cuenta = models.CharField(db_column='Cuenta', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    id = models.CharField(db_column='Id', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    mclase = models.CharField(db_column='mClase', max_length=1, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mgrupo = models.CharField(db_column='mGrupo', max_length=2, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mcodigo = models.CharField(db_column='mCodigo', max_length=5, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    indice = models.IntegerField(db_column='Indice')  # Field name made lowercase.
    subindice = models.AutoField(db_column='SubIndice', primary_key=True)  # Field name made lowercase.
    valorreal = models.DecimalField(db_column='Valorreal', max_digits=19, decimal_places=4)  # Field name made lowercase.
    menu = models.CharField(db_column='Menu', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    hora = models.CharField(db_column='Hora', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    atencion = models.CharField(db_column='Atencion', max_length=1, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nota = models.CharField(db_column='Nota', max_length=200, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    pc = models.CharField(db_column='Pc', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    valorusd = models.DecimalField(db_column='ValorUsd', max_digits=19, decimal_places=4)  # Field name made lowercase.
    valorusdreal = models.DecimalField(db_column='ValorUsdReal', max_digits=19, decimal_places=4)  # Field name made lowercase.
    fanula = models.DateTimeField(db_column='FAnula', blank=True, null=True)  # Field name made lowercase.
    motivoanula = models.CharField(db_column='MotivoAnula', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    hanula = models.CharField(db_column='HAnula', max_length=8, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nueva_fecha = models.DateTimeField(db_column='Nueva_Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Consumos'


class Controlmesas(models.Model):
    pk = models.CompositePrimaryKey('PVenta', 'NumMesa')
    pventa = models.CharField(db_column='PVenta', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nummesa = models.CharField(db_column='NumMesa', max_length=4, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    pc = models.CharField(db_column='Pc', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ControlMesas'


class Ctasmesas(models.Model):
    punto = models.CharField(db_column='Punto', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    mesa = models.CharField(db_column='Mesa', max_length=4, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    garzon = models.CharField(db_column='Garzon', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cubiertos = models.SmallIntegerField(db_column='Cubiertos')  # Field name made lowercase.
    hora = models.CharField(db_column='Hora', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    docto = models.CharField(db_column='Docto', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    folio = models.CharField(db_column='Folio', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    turno = models.CharField(db_column='Turno', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    dscto = models.SmallIntegerField(db_column='Dscto')  # Field name made lowercase.
    cuenta = models.CharField(db_column='Cuenta', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    hab = models.CharField(db_column='Hab', max_length=4, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cliente = models.CharField(db_column='Cliente', max_length=15, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    propina = models.FloatField(db_column='Propina')  # Field name made lowercase.
    sw = models.CharField(max_length=1, db_collation='Modern_Spanish_CI_AS')
    cuentas = models.IntegerField(db_column='Cuentas')  # Field name made lowercase.
    total = models.FloatField(db_column='Total')  # Field name made lowercase.
    convenio = models.FloatField(db_column='Convenio')  # Field name made lowercase.
    atencion = models.FloatField(db_column='Atencion')  # Field name made lowercase.
    habitacion = models.FloatField(db_column='Habitacion')  # Field name made lowercase.
    foliocnv = models.CharField(db_column='FolioCnv', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    sucursal = models.CharField(db_column='Sucursal', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    paquete = models.FloatField(db_column='Paquete')  # Field name made lowercase.
    admin = models.FloatField(db_column='Admin')  # Field name made lowercase.
    ccosto = models.SmallIntegerField(db_column='CCosto')  # Field name made lowercase.
    personal = models.IntegerField(db_column='Personal')  # Field name made lowercase.
    totalpersonal = models.FloatField(db_column='TotalPersonal')  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombrecta = models.CharField(db_column='NombreCta', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    pc = models.CharField(db_column='Pc', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CtasMesas'


class Familias(models.Model):
    clase = models.CharField(db_column='Clase', primary_key=True, max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nclase = models.CharField(db_column='NClase', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Familias'


class Garzones(models.Model):
    codigo = models.CharField(db_column='Codigo', primary_key=True, max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    vigente = models.CharField(db_column='Vigente', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    grupo = models.IntegerField(db_column='Grupo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Garzones'


class Grupopuntos(models.Model):
    pk = models.CompositePrimaryKey('Clase', 'Grupo', 'Punto')
    clase = models.CharField(db_column='Clase', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    grupo = models.CharField(db_column='Grupo', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    punto = models.CharField(db_column='Punto', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GrupoPuntos'


class Grupos(models.Model):
    pk = models.CompositePrimaryKey('Grupo', 'Clase')
    grupo = models.CharField(db_column='Grupo', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    ngrupo = models.CharField(db_column='NGrupo', max_length=30, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    clase = models.CharField(db_column='Clase', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    happy = models.BooleanField(db_column='Happy')  # Field name made lowercase.
    vigente = models.CharField(db_column='Vigente', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Grupos'


class Menus(models.Model):
    familia = models.CharField(db_column='Familia', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    seccion = models.CharField(db_column='Seccion', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    producto = models.CharField(db_column='Producto', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nproducto = models.CharField(db_column='NProducto', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    valor = models.DecimalField(db_column='Valor', max_digits=19, decimal_places=4)  # Field name made lowercase.
    grupo = models.CharField(db_column='Grupo', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    exento = models.BooleanField(db_column='Exento')  # Field name made lowercase.
    despacho = models.CharField(db_column='Despacho', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    clase = models.CharField(db_column='Clase', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    bodega = models.CharField(db_column='Bodega', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    menu = models.CharField(db_column='Menu', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Menus'


class Mesas(models.Model):
    pk = models.CompositePrimaryKey('Punto', 'Mesa')
    punto = models.CharField(db_column='Punto', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    mesa = models.CharField(db_column='Mesa', max_length=4, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    garzon = models.CharField(db_column='Garzon', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mesas'


class Numtables(models.Model):
    folio = models.CharField(db_column='Folio', primary_key=True, max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NumTables'


class Productos(models.Model):
    producto = models.CharField(db_column='Producto', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nproducto = models.CharField(db_column='NProducto', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    valor = models.DecimalField(db_column='Valor', max_digits=19, decimal_places=4)  # Field name made lowercase.
    grupo = models.CharField(db_column='Grupo', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    exento = models.BooleanField(db_column='Exento')  # Field name made lowercase.
    despacho = models.CharField(db_column='Despacho', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    clase = models.CharField(db_column='Clase', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero')  # Field name made lowercase.
    bodega = models.CharField(db_column='Bodega', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    menu = models.CharField(db_column='Menu', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    baja = models.CharField(db_column='Baja', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    despacho2 = models.CharField(db_column='Despacho2', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    valorusd = models.DecimalField(db_column='ValorUSD', max_digits=19, decimal_places=4)  # Field name made lowercase.
    happy = models.CharField(db_column='Happy', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Productos'
        unique_together = (('producto', 'grupo', 'clase'),)


class Puntos(models.Model):
    codigo = models.CharField(db_column='Codigo', primary_key=True, max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=30, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    centro = models.CharField(max_length=3, db_collation='Modern_Spanish_CI_AS')
    afectotip = models.CharField(db_column='AfectoTip', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Puntos'


class Tarifas(models.Model):
    pk = models.CompositePrimaryKey('Punto', 'Clase', 'Grupo', 'Codigo')
    punto = models.CharField(db_column='Punto', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    clase = models.CharField(db_column='Clase', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    grupo = models.CharField(db_column='Grupo', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    valor = models.DecimalField(db_column='Valor', max_digits=19, decimal_places=4)  # Field name made lowercase.
    valorusd = models.DecimalField(db_column='ValorUSD', max_digits=19, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tarifas'


class Turno(models.Model):
    turno = models.CharField(db_column='Turno', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    horainicio = models.CharField(db_column='HoraInicio', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fechaproceso = models.DateField(db_column='FechaProceso', blank=True, null=True)  # Field name made lowercase.
    hrainicio = models.CharField(db_column='HraInicio', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    mininicio = models.CharField(db_column='MinInicio', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    hratermino = models.CharField(db_column='HraTermino', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    mintermino = models.CharField(db_column='MinTermino', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    descuento = models.IntegerField(db_column='Descuento')  # Field name made lowercase.
    lunes = models.CharField(db_column='Lunes', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    martes = models.CharField(db_column='Martes', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    miercoles = models.CharField(db_column='Miercoles', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    jueves = models.CharField(db_column='Jueves', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    viernes = models.CharField(db_column='Viernes', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    sabado = models.CharField(db_column='Sabado', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    domingo = models.CharField(db_column='Domingo', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Turno'


class Usuarios(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=25, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    password = models.CharField(db_column='Password', unique=True, max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cargo = models.CharField(db_column='Cargo', max_length=25, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    setup = models.BooleanField(db_column='Setup')  # Field name made lowercase.
    pos = models.BooleanField(db_column='Pos')  # Field name made lowercase.
    reportes = models.BooleanField(db_column='Reportes')  # Field name made lowercase.
    boffice = models.BooleanField(db_column='BOffice')  # Field name made lowercase.
    recetas = models.BooleanField(db_column='Recetas')  # Field name made lowercase.
    claveanula = models.CharField(db_column='ClaveAnula', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    garzon = models.CharField(db_column='Garzon', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    supervisor = models.BooleanField(db_column='Supervisor')  # Field name made lowercase.
    admin = models.BooleanField(db_column='Admin')  # Field name made lowercase.
    idcard = models.CharField(db_column='IdCard', max_length=10, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    vigente = models.CharField(db_column='Vigente', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Usuarios'


class Valorespos(models.Model):
    ncliente = models.CharField(db_column='NCliente', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    existencia = models.CharField(db_column='Existencia', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cocina = models.CharField(db_column='Cocina', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    bar = models.CharField(db_column='Bar', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    hotel = models.CharField(db_column='Hotel', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    comanda = models.CharField(db_column='Comanda', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    imprimebol = models.CharField(db_column='ImprimeBol', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    exentodocto = models.CharField(db_column='ExentoDocto', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    garzonadicionista = models.CharField(db_column='GarzonAdicionista', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    accesocardcliente = models.CharField(db_column='AccesoCardCliente', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    velocidad = models.CharField(db_column='Velocidad', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    paridad = models.CharField(db_column='Paridad', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    bitsdato = models.CharField(db_column='BitsDato', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    bitsparo = models.CharField(db_column='BitsParo', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    puerta = models.IntegerField(db_column='Puerta')  # Field name made lowercase.
    bsize = models.IntegerField(db_column='BSize')  # Field name made lowercase.
    cflujo = models.IntegerField(db_column='CFlujo')  # Field name made lowercase.
    parrilla = models.CharField(db_column='Parrilla', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    frio = models.CharField(db_column='Frio', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    reposteria = models.CharField(db_column='Reposteria', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    copiascuenta = models.SmallIntegerField(db_column='CopiasCuenta')  # Field name made lowercase.
    garzoncajero = models.CharField(db_column='GarzonCajero', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    garzondscto = models.CharField(db_column='GarzonDscto', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    copiasbar = models.CharField(db_column='CopiasBar', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    copiascocina = models.CharField(db_column='CopiasCocina', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    copiascocinafria = models.CharField(db_column='CopiasCocinaFria', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    copiasparrilla = models.CharField(db_column='CopiasParrilla', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    copiasreposteria = models.CharField(db_column='CopiasReposteria', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    controlcantidadesmenu = models.CharField(db_column='ControlCantidadesMenu', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    habantescta = models.CharField(db_column='HabAntesCta', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    autoturno = models.CharField(db_column='AutoTurno', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    e_bol = models.CharField(db_column='e_Bol', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    e_fnac = models.CharField(db_column='e_FNac', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    eproveedor = models.CharField(db_column='eProveedor', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    rutrl = models.CharField(db_column='RutRL', max_length=15, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    numresolucion = models.CharField(db_column='NumResolucion', max_length=10, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fecharesolucion = models.DateField(db_column='FechaResolucion', blank=True, null=True)  # Field name made lowercase.
    ipfacturacion = models.CharField(db_column='IPFacturacion', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    keygdexpress = models.CharField(db_column='KeyGDExpress', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    rutcliente = models.CharField(db_column='RutCliente', max_length=15, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    rsocial = models.CharField(db_column='RSocial', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    giro = models.CharField(db_column='Giro', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', max_length=30, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    comuna = models.CharField(db_column='Comuna', max_length=30, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    acteco = models.CharField(db_column='Acteco', max_length=10, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    ebol_ini = models.IntegerField(db_column='eBol_Ini')  # Field name made lowercase.
    ebol_fin = models.IntegerField(db_column='eBol_Fin')  # Field name made lowercase.
    efnac_ini = models.IntegerField(db_column='eFNac_Ini')  # Field name made lowercase.
    efnac_fin = models.IntegerField(db_column='eFNac_Fin')  # Field name made lowercase.
    encnac_ini = models.IntegerField(db_column='eNCNac_Ini')  # Field name made lowercase.
    encnac_fin = models.IntegerField(db_column='eNCNac_Fin')  # Field name made lowercase.
    detallefact = models.CharField(db_column='DetalleFact', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    ambiente = models.CharField(db_column='Ambiente', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    offline = models.CharField(db_column='OffLine', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    copiasbol = models.SmallIntegerField(db_column='CopiasBol')  # Field name made lowercase.
    copiasfnac = models.SmallIntegerField(db_column='CopiasFNac')  # Field name made lowercase.
    copiasncnac = models.SmallIntegerField(db_column='CopiasNCNac')  # Field name made lowercase.
    informanow = models.CharField(db_column='InformaNow', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    avisofincaf = models.SmallIntegerField(db_column='AvisoFinCaf')  # Field name made lowercase.
    namefilecaf39 = models.CharField(db_column='NameFileCaf39', max_length=100, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    namefilecaf41 = models.CharField(db_column='NameFileCaf41', max_length=100, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    namefilecaf33 = models.CharField(db_column='NameFileCaf33', max_length=100, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    namefilecaf34 = models.CharField(db_column='NameFileCaf34', max_length=100, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    namefilecaf61 = models.CharField(db_column='NameFileCaf61', max_length=100, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    namefilecaf56 = models.CharField(db_column='NameFileCaf56', max_length=100, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    namefilecaf110 = models.CharField(db_column='NameFileCaf110', max_length=100, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    namefilecaf112 = models.CharField(db_column='NameFileCaf112', max_length=100, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    namefilecaf111 = models.CharField(db_column='NameFileCaf111', max_length=100, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    printeranulacion = models.CharField(db_column='PrinterAnulacion', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    dsctocard = models.CharField(db_column='DsctoCard', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ValoresPOS'


class Variedades(models.Model):
    vclase = models.CharField(db_column='VClase', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    vgrupo = models.CharField(db_column='VGrupo', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    vproducto = models.CharField(db_column='VProducto', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    variedad = models.CharField(db_column='Variedad', max_length=30, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Variedades'

