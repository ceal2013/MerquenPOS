# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Anulaciones(models.Model):
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    folio = models.CharField(db_column='Folio', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    turno = models.CharField(db_column='Turno', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    hora = models.CharField(db_column='Hora', max_length=8, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    mesa = models.CharField(db_column='Mesa', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cantidad = models.DecimalField(db_column='Cantidad', max_digits=19, decimal_places=4)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    valor = models.DecimalField(db_column='Valor', max_digits=19, decimal_places=4)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=30, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    garzon = models.CharField(db_column='Garzon', max_length=30, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    equipo = models.CharField(db_column='Equipo', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    motivo = models.CharField(db_column='Motivo', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fanula = models.DateTimeField(db_column='FAnula', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Anulaciones'


class Arqueo(models.Model):
    tipo = models.CharField(db_column='Tipo', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    docto = models.CharField(db_column='Docto', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    folio = models.CharField(db_column='Folio', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=4)  # Field name made lowercase.
    garzon = models.CharField(db_column='Garzon', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fp1 = models.DecimalField(db_column='FP1', max_digits=19, decimal_places=4)  # Field name made lowercase.
    fp2 = models.DecimalField(db_column='FP2', max_digits=19, decimal_places=4)  # Field name made lowercase.
    fp3 = models.DecimalField(db_column='FP3', max_digits=19, decimal_places=4)  # Field name made lowercase.
    fp4 = models.DecimalField(db_column='FP4', max_digits=19, decimal_places=4)  # Field name made lowercase.
    fp5 = models.DecimalField(db_column='FP5', max_digits=19, decimal_places=4)  # Field name made lowercase.
    fp6 = models.DecimalField(db_column='FP6', max_digits=19, decimal_places=4)  # Field name made lowercase.
    fp7 = models.DecimalField(db_column='FP7', max_digits=19, decimal_places=4)  # Field name made lowercase.
    fp8 = models.DecimalField(db_column='FP8', max_digits=19, decimal_places=4)  # Field name made lowercase.
    fp9 = models.DecimalField(db_column='FP9', max_digits=19, decimal_places=4)  # Field name made lowercase.
    fp10 = models.DecimalField(db_column='FP10', max_digits=19, decimal_places=4)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    neto = models.DecimalField(db_column='Neto', max_digits=19, decimal_places=4)  # Field name made lowercase.
    iva = models.DecimalField(db_column='Iva', max_digits=19, decimal_places=4)  # Field name made lowercase.
    exento = models.DecimalField(db_column='Exento', max_digits=19, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Arqueo'


class Autoturnos(models.Model):
    turno = models.CharField(db_column='Turno', primary_key=True, max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    horainicial = models.CharField(db_column='HoraInicial', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    horafinal = models.CharField(db_column='HoraFinal', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AutoTurnos'


class Ccosto(models.Model):
    codigo = models.SmallIntegerField(db_column='Codigo', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CCosto'


class Cafmae(models.Model):
    tipo = models.CharField(db_column='Tipo', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fechacarga = models.DateTimeField(db_column='FechaCarga', blank=True, null=True)  # Field name made lowercase.
    desde = models.IntegerField(db_column='Desde')  # Field name made lowercase.
    hasta = models.IntegerField(db_column='Hasta')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fechaactiva = models.DateTimeField(db_column='FechaActiva', blank=True, null=True)  # Field name made lowercase.
    sec = models.AutoField(db_column='Sec')  # Field name made lowercase.
    namecaf = models.CharField(db_column='NameCaf', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CafMae'


class Cajabol(models.Model):
    tipo = models.CharField(db_column='Tipo', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    docto = models.CharField(db_column='Docto', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    neto = models.DecimalField(db_column='Neto', max_digits=19, decimal_places=4)  # Field name made lowercase.
    iva = models.DecimalField(db_column='Iva', max_digits=19, decimal_places=4)  # Field name made lowercase.
    exento = models.DecimalField(db_column='Exento', max_digits=19, decimal_places=4)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=4)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    id = models.CharField(db_column='Id', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    hora = models.CharField(db_column='Hora', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CajaBol'


class Cajafn(models.Model):
    tipo = models.CharField(db_column='Tipo', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    docto = models.CharField(db_column='Docto', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    rut = models.CharField(db_column='Rut', max_length=10, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    neto = models.DecimalField(db_column='Neto', max_digits=19, decimal_places=4)  # Field name made lowercase.
    iva = models.DecimalField(db_column='Iva', max_digits=19, decimal_places=4)  # Field name made lowercase.
    exento = models.DecimalField(db_column='Exento', max_digits=19, decimal_places=4)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=4)  # Field name made lowercase.
    id = models.CharField(db_column='Id', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    hora = models.CharField(db_column='Hora', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CajaFN'


class Cajafolios(models.Model):
    punto = models.CharField(db_column='Punto', max_length=30, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    folio = models.CharField(db_column='Folio', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    mesa = models.CharField(db_column='Mesa', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cuenta = models.CharField(db_column='Cuenta', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    garzon = models.CharField(db_column='Garzon', max_length=30, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cubiertos = models.IntegerField(db_column='Cubiertos')  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=4)  # Field name made lowercase.
    hab = models.CharField(db_column='Hab', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    habtotal = models.DecimalField(db_column='HabTotal', max_digits=19, decimal_places=4)  # Field name made lowercase.
    foliocnv = models.CharField(db_column='FolioCnv', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cnvtotal = models.DecimalField(db_column='CnvTotal', max_digits=19, decimal_places=4)  # Field name made lowercase.
    paquete = models.DecimalField(db_column='Paquete', max_digits=19, decimal_places=4)  # Field name made lowercase.
    tip = models.DecimalField(db_column='Tip', max_digits=19, decimal_places=4)  # Field name made lowercase.
    dscto = models.DecimalField(db_column='Dscto', max_digits=19, decimal_places=4)  # Field name made lowercase.
    dsctototal = models.DecimalField(db_column='DsctoTotal', max_digits=19, decimal_places=4)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=10, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    docto = models.CharField(db_column='Docto', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    admintotal = models.DecimalField(db_column='AdminTotal', max_digits=19, decimal_places=4)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    tpagos = models.CharField(db_column='TPagos', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    horapago = models.CharField(db_column='HoraPago', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CajaFolios'


class Cambios(models.Model):
    tipo = models.CharField(db_column='Tipo', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    hora = models.CharField(db_column='Hora', max_length=8, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    mesaini = models.CharField(db_column='MesaIni', max_length=4, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    puntoini = models.CharField(db_column='PuntoIni', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    mesafin = models.CharField(db_column='MesaFin', max_length=4, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    puntofin = models.CharField(db_column='PuntoFin', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nota = models.CharField(db_column='Nota', max_length=200, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    folioini = models.CharField(db_column='FolioIni', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    foliofin = models.CharField(db_column='FolioFin', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    clase = models.CharField(db_column='Clase', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    grupo = models.CharField(db_column='Grupo', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    producto = models.CharField(db_column='Producto', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cambios'


class Clientes(models.Model):
    pk = models.CompositePrimaryKey('Rut', 'Sucursal')
    rut = models.CharField(db_column='Rut', max_length=15, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nfantasia = models.CharField(db_column='NFantasia', max_length=100, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    rsocial = models.CharField(db_column='RSocial', max_length=100, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=40, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', max_length=25, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    comuna = models.CharField(db_column='Comuna', max_length=25, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    giro = models.CharField(db_column='Giro', max_length=40, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fono1 = models.CharField(db_column='Fono1', max_length=15, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fono2 = models.CharField(db_column='Fono2', max_length=15, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=15, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    ejecutivo = models.CharField(db_column='Ejecutivo', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=35, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    codpostal = models.CharField(db_column='CodPostal', max_length=25, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    tarifa = models.CharField(db_column='Tarifa', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    convenio = models.CharField(db_column='Convenio', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    representante = models.CharField(db_column='Representante', max_length=40, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    contacto = models.CharField(db_column='Contacto', max_length=40, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fnac = models.DateTimeField(db_column='Fnac', blank=True, null=True)  # Field name made lowercase.
    cargo = models.CharField(db_column='Cargo', max_length=25, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    saludo = models.CharField(db_column='Saludo', max_length=10, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    inicio = models.DateTimeField(db_column='Inicio', blank=True, null=True)  # Field name made lowercase.
    termino = models.DateTimeField(db_column='Termino', blank=True, null=True)  # Field name made lowercase.
    tipocliente = models.CharField(db_column='TipoCliente', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nota = models.CharField(db_column='Nota', max_length=200, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    tipoiva = models.CharField(db_column='TipoIVA', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    tipodocto = models.SmallIntegerField(db_column='TipoDocto')  # Field name made lowercase.
    tiporesponsable = models.IntegerField(db_column='TipoResponsable')  # Field name made lowercase.
    ncompra = models.DecimalField(db_column='NCompra', max_digits=18, decimal_places=0)  # Field name made lowercase.
    nventa = models.DecimalField(db_column='NVenta', max_digits=18, decimal_places=0)  # Field name made lowercase.
    sucursal = models.CharField(db_column='Sucursal', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    extranjera = models.CharField(db_column='Extranjera', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    dscto = models.DecimalField(db_column='Dscto', max_digits=19, decimal_places=4)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Clientes'


class Comanda(models.Model):
    indice = models.IntegerField(db_column='Indice')  # Field name made lowercase.
    subindice = models.IntegerField(db_column='SubIndice')  # Field name made lowercase.
    clase = models.CharField(db_column='Clase', max_length=1, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nproducto = models.CharField(db_column='NProducto', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cantidad = models.DecimalField(db_column='Cantidad', max_digits=19, decimal_places=4)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=4)  # Field name made lowercase.
    exento = models.BooleanField(db_column='Exento')  # Field name made lowercase.
    folio = models.CharField(db_column='Folio', max_length=7, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    grupo = models.CharField(db_column='Grupo', max_length=2, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    producto = models.CharField(db_column='Producto', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=5, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Comanda'


class Comandas(models.Model):
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=Tr