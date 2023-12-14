from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from django.core.validators import (MaxValueValidator, MinValueValidator)
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
import datetime

is_error = -1
is_exito = 1
tiporespuestac = (
    (is_error, 'ERROR'),
    (is_exito, 'EXITO'),
)

is_inactive = -1
is_active = 1
tipoestadoc = (
    (is_inactive, 'INACTIVE'),
    (is_active, 'ACTIVE'),
)

#tributos
secc_is_resumen = 1
secc_is_cuerpo = 2
secc_is_advalorem = 3
secciontributos = (
    (secc_is_resumen, 'TRIBUTOS APLICADOS POR ÍTEMS REFLEJADOS EN EL RESUMEN DEL DTE'),
    (secc_is_cuerpo, 'TRIBUTOS APLICADOS POR ÍTEMS REFLEJADOS EN EL CUERPO DEL DOCUMENTO'),
    (secc_is_advalorem, 'IMPUESTOS AD-VALOREM APLICADOS POR ÍTEM DE USO INFORMATIVO REFLEJADOS EL RESUMEN DEL DOCUMENTO'),
)

secc_monto = 1
secc_porcentual = 2
secc_nd = 3
secciontributostipovalor = (
    (secc_monto, 'Monto'),
    (secc_porcentual, 'Porcentual'),
    (secc_nd, 'No Definido'),
)





class wsentorno(models.Model):
    codigo = models.CharField(max_length=10, null=False, blank=False, unique=True)
    nombre = models.CharField(max_length=200, null=False, blank=False)
    url = models.CharField(max_length=1000, null=False, blank=False)
    user_creation = CurrentUserField(related_name='user_creation_wentorno')
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    user_last_update = CurrentUserField(on_update=True)
    history = HistoricalRecords()

    class Meta:
            ordering = ['nombre']

    def __str__(self):
        return self.nombre


class wsurl(models.Model):
    codigo = models.CharField(max_length=10, null=False, blank=False,unique=True)
    url = models.CharField(max_length=1000, null=False, blank=False)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    wsentorno = models.ForeignKey(wsentorno,on_delete=models.DO_NOTHING,blank=False,null=False)
    user_creation = CurrentUserField(related_name='user_creation_wsurl')
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    user_last_update = CurrentUserField(on_update=True)

    history = HistoricalRecords()

    class Meta:
            ordering = ['nombre']

    def __str__(self):
        return self.nombre

#Comunicacion de token con hacienda
class ws_autenticacion_log(models.Model):
    user_enviado = models.TextField(null=False, blank=False)
    jenviado = models.JSONField(null=True, blank=True)
    jrespuesta = models.JSONField(null=True, blank=True)
    token = models.TextField(null=True, blank=True)
    tiporespuesta = models.IntegerField(choices=tiporespuestac, null=False, blank=False,
                                                 help_text='Tipo de Respuesta', default=1)
    mensajeerror = models.TextField(null=True, blank=True)
    date_creation = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
            ordering = ['id']

    def __str__(self):
        return self.nombre

#Categorias de actividades
class catactividadeco(models.Model):
    descripcion = models.CharField(max_length=200, blank=False, null=False)
    nm_estado = models.IntegerField(choices=tipoestadoc, null=False, blank=False,
                                    help_text='Activo o Inactivo el Registro', default=1)

    def __str__(self):
        return self.descripcion
#Modelo medico    


class subactividadeco(models.Model):
    catactividadeco = models.ForeignKey(catactividadeco, on_delete=models.DO_NOTHING, blank=False, null=False)
    descripcion = models.CharField(max_length=200,blank=False, null=False)
    nm_estado = models.IntegerField(choices=tipoestadoc, null=False, blank=False,
                                    help_text='Activo o Inactivo el Registro', default=1)

    def __str__(self):
        return self.descripcion


class actividadeco(models.Model):
    subactividadeco = models.ForeignKey(subactividadeco, on_delete=models.DO_NOTHING, blank=False, null=False)
    codigo = models.CharField(max_length=20, blank=False, null=False)
    descripcion = models.CharField(max_length=200, blank=False, null=False)
    nm_estado = models.IntegerField(choices=tipoestadoc, null=False, blank=False,
                                    help_text='Activo o Inactivo el Registro', default=1)

    def __str__(self):
        return self.descripcion

class mastercat(models.Model):
    codigo = models.CharField(max_length=20,unique=True)
    descripcion = models.CharField(max_length=200)
    nm_estado = models.IntegerField(choices=tipoestadoc, null=False, blank=False,
                                    help_text='Activo o Inactivo el Registro', default=1)

    def __str__(self):
        return self.descripcion


class detallemastercat(models.Model):
    mastercat = models.ForeignKey(mastercat, on_delete=models.DO_NOTHING, blank=False, null=False)
    codigo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=200)
    nm_estado = models.IntegerField(choices=tipoestadoc, null=False, blank=False,
                                                 help_text='Activo o Inactivo el Registro', default=1)

    def __str__(self):
        return self.descripcion
    
class param_version_dte(models.Model):
    codigo = models.CharField(max_length=5, blank=False,null=True)
    descripcion = models.CharField(max_length=100, blank=False, null=True)
    valor = models.CharField(max_length=100, blank=False,null=True)
    tipoDato = models.CharField(max_length=100, blank=False, null=True)

    def __str__(self):
        return self.descripcion
    
    
class medico(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    nit = models.CharField(max_length=17, null=False, blank=False)
    docidentificacion = models.CharField(max_length=25, null=False, blank=False)
    tiposervicio = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, blank=True, null=True,
                                       related_name='docasoc_medtipos')
    
class departamento(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=200, null=False, blank=False)
    nm_estado = models.IntegerField(choices=tipoestadoc, null=False, blank=False,
                                    help_text='Activo o Inactivo el Registro', default=1)

    def __str__(self):
        return self.descripcion


class municipio(models.Model):
    departamento = models.ForeignKey(departamento, on_delete=models.DO_NOTHING, blank=False, null=False)
    codigo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=200, null=False, blank=False)
    nm_estado = models.IntegerField(choices=tipoestadoc, null=False, blank=False,
                                    help_text='Activo o Inactivo el Registro', default=1)

    def __str__(self):
        return self.descripcion
    
class tributo(models.Model): #Tributo sumarizado
    seccion = models.IntegerField(choices=secciontributos, null=False, blank=False, help_text='Sección donde se ve reflejado', default=1)
    codigo = models.CharField(max_length=20, blank=False, null=False)
    valor = models.DecimalField(max_digits=6, decimal_places=2,blank=True, null=True)
    tipo = models.IntegerField(choices=secciontributostipovalor, null=False, blank=False,help_text='Tipo de Valor',default=1)
    descripcion = models.CharField(max_length=200)
    nm_estado = models.IntegerField(choices=tipoestadoc, null=False, blank=False,
                                    help_text='Activo o Inactivo el Registro', default=1)
    def __str__(self):
        return self.descripcion
    
class Identification(models.Model):
    version = models.CharField(max_length=2, null=False, blank=False)
    ambiente = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, max_length=2, null=False, blank=False, related_name='iden_ambnt')
    tipoDte = models.ForeignKey(detallemastercat,on_delete=models.DO_NOTHING, null=False, blank=False, related_name='iden_tipodte')
    numeroControl = models.CharField(max_length=31, null=False, blank=False)#Considerar obviar guiones e incluirlos automaticamente
    codigoGeneracion = models.CharField(max_length=36, null=False, blank=False)
    tipoModelo = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, blank=False, null=False)
    tipoOperacion = models.ForeignKey(detallemastercat,on_delete=models.DO_NOTHING, blank=False, null = False, related_name='iden_tipOper')
    tipoContingencia = models.IntegerField(blank=True, null=True)
    motivoContin = models.CharField(max_length=500, blank=True, null=True)
    fecEmi = models.DateField(null=False, blank=False)
    horEmi = models.CharField(max_length=8, null=False, blank=False)
    tipoMoneda = models.CharField(max_length=4, null=False, blank=False)

    
    def __str__(self):
        return f"{self.tipoDte}-{self.numeroControl}"
    
class DocumentoRelacionado(models.Model):
    tipoDocumento = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='docrel_tipodocs')
    tipoGeneracion = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='docrel_tipogener')
    numeroDocumento = models.CharField(max_length=36, null=True, blank=True)
    fechaEmision = models.DateField()

class EmisorN(models.Model):
    nit = models.CharField(max_length=18, null=False, blank=False)
    nrc = models.CharField(max_length=8, null=False, blank=False)
    nombre = models.CharField(max_length=250, null=False, blank=False)
    natural = models.CharField(max_length=1, null=True, blank=False, choices=[
                                                                                    ('S', 'Sí'),
                                                                                    ('N', 'No'),
                                                                                ])   
    actividadeco = models.ForeignKey(actividadeco, on_delete=models.DO_NOTHING, blank=True, null=True,
                                     related_name='emi_actividadecon')
    nombrecomercial = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    logo = models.ImageField(upload_to='uploaded/profiles_medicos', blank=True, null=True)

    def __str__(self):
        return self.nombre
    

class Establecimiento(models.Model):
    tipoEstable = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='cod_tipoEstable')
    complementodir = models.CharField(max_length=200, null=False, blank=False)
    direccionMun = models.ForeignKey(municipio, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='cod_munip')
    telefono = models.CharField(max_length=30, null=False, blank=False)
    celular = models.CharField(max_length=30, null=False, blank=False)
    codestablemh = models.CharField(max_length=4, null=True, blank=True)
    codestablec = models.CharField(max_length=4,null=True, blank=True)
    def __str__(self):
        return self.tipoEstable
class PuntoVenta(models.Model):
    establecimiento_fk = models.ForeignKey(Establecimiento, on_delete=models.DO_NOTHING, null=True, blank=False)
    codpuntoventamh = models.CharField(max_length=4, null=True, blank=True)
    codpuntoventa = models.CharField(max_length=4, null=True, blank=True)

class ReceptorN(models.Model):
    tipodocumento = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, blank=False, null=False, related_name='recep_tipodoc')
    nodocumento = models.CharField(max_length=20, null=False, blank=False,unique=True)
    nrc = models.CharField(max_length=8, null=True, blank=True, unique=True)
    nombre = models.CharField(max_length=250, null=True, blank=True)
    nombreComercial = models.CharField(max_length=255, null=True, blank=True)
    actividadeco = models.ForeignKey(actividadeco, on_delete=models.DO_NOTHING, blank=True, null=True,
                                     related_name='recep_actividadecon')
    municipio = models.ForeignKey(municipio, on_delete=models.DO_NOTHING, blank=True, null=True)
    complementodir = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    celular = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    gran_contr = models.CharField(max_length=1, null=True, blank=False, choices=[
                                                                                    ('S', 'Sí'),
                                                                                    ('N', 'No'),
                                                                                ])    

    user_creation = CurrentUserField(related_name='reccep_user_creationc')
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    user_last_update = CurrentUserField(on_update=True)

    def __str__(self):
        return self.nombre

class OtrosDocAsoc(models.Model):
    coddocasociado = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='doc_asoc_tipodoc')
    descdocumento = models.CharField(max_length=100, null=True, blank=True)
    detalledocumento = models.CharField(max_length=300, null=True, blank=True)
    medico = models.ForeignKey(medico, on_delete=models.DO_NOTHING, blank=True, null=True)
    user_creation = CurrentUserField(related_name='docasoc_user_creationc')
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    user_last_update = CurrentUserField(on_update=True)
    history = HistoricalRecords()

class VentaTercero(models.Model):
    nit = models.CharField(max_length=14, null=False, blank=False)
    nombre = models.CharField(max_length=250, blank=False, null=False)
    user_creation = CurrentUserField(related_name='ventater_user_creationc')
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    user_last_update = CurrentUserField(on_update=True)

    history = HistoricalRecords()
class Extension(models.Model):

    nombentrega = models.CharField(max_length=100, null=True, blank=False)
    docuentrega = models.CharField(max_length=25, null=True, blank=False)
    nombrecibe = models.CharField(max_length=100, null=True, blank=False)
    docurecibe = models.CharField(max_length=25, null=True, blank=False)
    observaciones = models.CharField(max_length=3000, null=True, blank=True)
    placavehiculo = models.CharField(max_length=10, null=True, blank=True)

    user_creation = CurrentUserField(related_name='extensionfactura_user_creationc')
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    user_last_update = CurrentUserField(on_update=True)

    history = HistoricalRecords()

class Productos(models.Model):
        codigo = models.CharField(max_length=25, null=True, blank=True, unique=True)
        descripcion = models.CharField(max_length=1000, blank=False, null=False )
        tributo = models.ForeignKey(tributo, on_delete=models.DO_NOTHING, blank=False, null=True)
        preciouni = models.DecimalField(max_digits=11, decimal_places=8, blank=False, null=False,)
        tipoitem = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, blank=False, null=True,
                                       related_name='detallefac_tipoitm')
        unimedida = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, blank=False, null=True,
                                   related_name='detallefac_unimed')
        exentoIva = models.CharField(max_length=1, null=True, blank=False, choices=[
                                                                                    ('S', 'Sí'),
                                                                                    ('N', 'No'),
                                                                                ])    
        user_creation = CurrentUserField(related_name='Producto_user_creationc')
        date_creation = models.DateTimeField(default=datetime.datetime.now)
        user_last_update = CurrentUserField(on_update=True)
        
        def __str__(self):
            return self.descripcion


class Cuerpo(models.Model):
    numitem = models.PositiveIntegerField(blank=False,null=False)
    producto = models.ForeignKey(Productos, on_delete=models.DO_NOTHING, blank=False, null=True)
    cantidad = models.DecimalField(max_digits=11, decimal_places=8, blank=False, null=False,default=1)


    #Tributo individual Check
    codtributo = models.ForeignKey(tributo, on_delete=models.DO_NOTHING, blank=True, null=True,
                                 related_name='detallefac_codtribuIVA')
    montodescuento = models.DecimalField(max_digits=11, decimal_places=8, blank=False, null=False,default=0 )
    ventanosuj = models.DecimalField(max_digits=11, decimal_places=8, blank=False, null=False,default=0 )
    ventaexenta = models.DecimalField(max_digits=11, decimal_places=8, blank=False, null=False, default=0)
    ventagravada = models.DecimalField(max_digits=11, decimal_places=8, blank=False, null=False, default=0)
    psv = models.DecimalField(max_digits=11, decimal_places=8, blank=False, null=False, default=0)
    nogravado = models.DecimalField(max_digits=11, decimal_places=8, blank=False, null=False, default=0)
    ivaitem = models.DecimalField(max_digits=11, decimal_places=8, blank=False, null=False, default=0)

    user_creation = CurrentUserField(related_name='cuerpofactura_user_creationc')
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    user_last_update = CurrentUserField(on_update=True)


    
class resumen(models.Model):
    totalnosuj = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    totalexenta = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    totalgravada = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    subtotalventas = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    descunosuj = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    descuexenta = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    descugravada = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    porcentajedescuento = models.DecimalField(max_digits=3, decimal_places=2, blank=False, null=False, default=0)
    totaldescu = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    subtotal = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    ivarete1 = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    reterenta = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    montototaloperacion = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    totalnogravado = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    totapagar = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    totalletras = models.CharField(max_length=200,null=False, blank=False)
    totalIva = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    saldofavor = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)
    condicionoperacion = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, blank=False, null=False,
                                      related_name='detallefac_condop')




class ApendiceFactura(models.Model):

    campo = models.CharField(max_length=25, null=False, blank=False)
    etiqueta = models.CharField(max_length=50, null=False, blank=False)
    valor = models.CharField(max_length=150, null=False, blank=False)
    user_creation = CurrentUserField(related_name='apendice_user_creation')
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    user_last_update = CurrentUserField(on_update=True, related_name='apendice_user_update')

    history = HistoricalRecords()


    def __str__(self):
        return self.descripcion
    
class tributoAsociado(models.Model):
    fk_tributo = models.ForeignKey(tributo, on_delete=models.DO_NOTHING, blank=False, null = False)


class Identificacion(models.Model):
    version = models.IntegerField(null=False, blank=False)
    ambiente = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='identificacion_ambiente')
    tipoDte = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, blank=False, null=False, related_name='identificacion_tipodte')
    numeroControl = models.CharField(max_length=32, blank=False, null=True)
    codigoGeneracion = models.CharField(max_length=36, blank=False, null=True)
    tipoModelo = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, blank=False, null=False, related_name='identificacion_tipomodelo')
    tipoOperacion = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, blank=False, null=False, related_name='identificacion_tipooperacion')


class Estado(models.Model):
    descripcion_estado = models.CharField(max_length=100, null=False)
    codigo_estado = models.CharField(max_length=50,null=False)


class Factura(models.Model):
    fk_receptor = models.ForeignKey(ReceptorN, on_delete=models.DO_NOTHING, blank=False, null = True)
    fk_Identificacion = models.ForeignKey(Identificacion, on_delete=models.CASCADE, blank=False, null=True)
    fk_emisor = models.ForeignKey(EmisorN, on_delete = models.DO_NOTHING, blank=False, null=True)
    fk_puntoVenta = models.ForeignKey(PuntoVenta, on_delete=models.DO_NOTHING, blank=False, null=True)
    codigoFactura = models.CharField(max_length=8, blank=False, null=True)
    fecha = models.DateField(blank=False, null=True)
    # Suma de gravados y exentos
    totalOperaciones = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    totalExento = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    totalnoExento = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    descuExenta = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    descuGravada = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    subtotalSinImpuestos = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    ivaRete = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    reteRenta = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    descuTotal = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    impuesTotal = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    subtotalconDescu = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    subtotal = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    totalPagar = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    totalIva = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    
    sello_hacienda = models.TextField(null=True, blank="")
    hacienda_response = models.JSONField(null=True)
    hacienda_fecha_procesamiento = models.DateTimeField(null=True)
    hacienda_codigo_mensaje = models.CharField(max_length=100,null=True)
    estado_dte = models.ForeignKey(Estado, on_delete=models.CASCADE, null=True)
    
    user_creation = CurrentUserField(related_name='factura_user_creation')
    user_last_update = CurrentUserField(on_update=True, related_name='factura_user_update')
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    last_update = models.DateTimeField(auto_now=True)
    
    
class DetalleFactura(models.Model):
    fk_factura = models.ForeignKey(Factura, on_delete=models.DO_NOTHING, blank=False, null=True)
    fk_Producto = models.ForeignKey(Productos, on_delete=models.DO_NOTHING, blank=False, null=True)
    precioUnitario =models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    cantidad = models.IntegerField(blank=False, null=True)
    total = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    totalDescuento = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    montoDescu = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=True)
    

class JsonFac(models.Model):
    fk_factura = models.ForeignKey(Factura,related_name='detalle', on_delete=models.DO_NOTHING, blank=False, null=True)
    json = models.JSONField()


class pagosfactura(models.Model):
    fk_Factura = models.ForeignKey(Factura, related_name='detallePagos',on_delete=models.DO_NOTHING, blank=False, null=True)
    codigo = models.ForeignKey(detallemastercat, on_delete=models.DO_NOTHING, blank=False, null=False, related_name='pagosfactura_tipopag')
    montopago = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0)

    user_creation = CurrentUserField(related_name='pagosfactura_user_creationc')
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    user_last_update = CurrentUserField(on_update=True, related_name='pagosfactura_user_updatec')

    history = HistoricalRecords()   


class Descuento(models.Model):
    TIPO_DESCUENTO = [
        ('MONTO_FACTURA', 'Monto factura'),
        ('MONTO_ITEM', 'Monto item'),
        ('PORCENTUAL_FACTURA', 'Porcentual factura'),
        ('PORCENTUAL_ITEM', 'Porcentual item')
    ]
    TIPO_PRODUCTO = [
        ('S', 'Exento'),
        ('N', 'Gravado')
    ]
    producto = models.ForeignKey('Productos',on_delete=models.CASCADE, null=True,blank=True)
    tipo_producto = models.CharField(max_length=1, null=True, blank=True, choices=TIPO_PRODUCTO)
    cantidad = models.DecimalField(max_digits=11, decimal_places=2) #Cantidad de productos o monto necesaria para aplicar el descuento
    tipo_descuento = models.CharField(max_length=100, choices=TIPO_DESCUENTO)
    valor_descuento = models.DecimalField(max_digits=11, decimal_places=2, null=False, blank=False)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.tipo_descuento


class Hacienda(models.Model):
    token = models.TextField(null=True)
    user = models.CharField(max_length=100, null=False)
    pwd = models.CharField(max_length=100, null=False)

    def save(self, *args, **kwargs):
        if not self.id:
            # Si es un nuevo objeto (es decir, no tiene un ID), utiliza make_password para almacenar la contraseña de manera segura
            self.pwd = make_password(self.pwd)
        super(Hacienda, self).save(*args, **kwargs)

    def check_password(self, raw_password):
        # Utiliza check_password para verificar la contraseña
        return check_password(raw_password, self.pwd)

class HaciendaClasificacionMensajes(models.Model):
    tipo = models.CharField(max_length=100, null=False)
    clasificacion = models.CharField(max_length=50,null=False)

class HaciendaMensajes(models.Model):
    codigo = models.CharField(max_length=100, null=False)
    mensaje = models.CharField(max_length=200,null=False)


class SMTP(models.Model):
    host = models.CharField(max_length=255, null=True, blank=False)
    port = models.IntegerField(null=True, blank=False)
    use_tls = models.BooleanField(null=True, blank=False)
    username = models.CharField(max_length=255, null=True, blank=False)
    password = models.CharField(max_length=255, null=True, blank=False)