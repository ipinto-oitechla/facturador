class Identification:
    def __init__(self, version, ambiente, tipoDte, numeroControl, codigoGeneracion, tipoModelo, tipoOperacion, tipoContingencia, motivoContin, fecEmi, horEmi, tipoMoneda):
        self.version = version
        self.ambiente = ambiente
        self.tipoDte = tipoDte
        self.numeroControl = numeroControl
        self.codigoGeneracion = codigoGeneracion
        self.tipoModelo = tipoModelo
        self.tipoOperacion = tipoOperacion
        self.tipoContingencia = tipoContingencia
        self.motivoContin = motivoContin
        self.fecEmi = fecEmi
        self.horEmi = horEmi
        self.tipoMoneda = tipoMoneda


class DocumentoRelacionado:
    def __init__(self, tipoDocumento, tipoGeneracion, numeroDocumento, fechaEmision):
        self.tipoDocumento = tipoDocumento
        self.tipoGeneracion = tipoGeneracion
        self.numeroDocumento = numeroDocumento
        self.fechaEmision = fechaEmision


class Direccion:
    def __init__(self, departamento, municipio, complemento):
        self.departamento = departamento
        self.municipio = municipio
        self.complemento = complemento


class Emisor:
    def __init__(self, nit, nrc, nombre, codActividad, desActividad, nombreComercial, tipoEstablecimiento, direccion, telefono, codEstableMH, codEstable, codPuntoVentaMH, codPuntoVenta, correo):
        self.nit = nit
        self.nrc = nrc
        self.nombre = nombre
        self.codActividad = codActividad
        self.desActividad = desActividad
        self.nombreComercial = nombreComercial
        self.tipoEstablecimiento = tipoEstablecimiento
        self.direccion = direccion
        self.telefono = telefono
        self.codEstableMH = codEstableMH
        self.codEstable = codEstable
        self.codPuntoVentaMH = codPuntoVentaMH
        self.codPuntoVenta = codPuntoVenta
        self.correo = correo


class Receptor:
    def __init__(self, tipoDocumento, numDocumento, nrc, nombre, codActividad, desActividad, direccion, telefono, correo):
        self.tipoDocumento = tipoDocumento
        self.numDocumento = numDocumento
        self.nrc = nrc
        self.nombre = nombre
        self.codActividad = codActividad
        self.desActividad = desActividad
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo


class OtrosDocumentos:
    def __init__(self, codDocAsociado, descDocumento, detalleDocumento, medico, tipoGeneracion, numeroDocumento,
                 fechaEmision):
        self.codDocAsociado = codDocAsociado
        self.descDocumento = descDocumento
        self.detalleDocumento = detalleDocumento
        self.medico = medico
        self.tipoGeneracion = tipoGeneracion
        self.numeroDocumento = numeroDocumento
        self.fechaEmision = fechaEmision


class Medico:
    def __init__(self, nombre, nit, docIdentificacion, tipoServicio):
        self.nombre = nombre
        self.nit = nit
        self.docIdentificacion = docIdentificacion
        self.tipoServicio = tipoServicio


class VentaTercero:
    def __init__(self, nit, nombre):
        self.nit = nit
        self.nombre = nombre


class CuerpoDocumento:
    def __init__(self, numItem, tipoItem, numeroDocumento, cantidad, codigo, codTributo, uniMedida, descripcion, precioUni, montoDescu, ventaNoSuj, ventaExenta, ventaGravada, tributos, psv, noGravado, ivaItem):
        self.numItem = numItem
        self.tipoItem = tipoItem
        self.numeroDocumento = numeroDocumento
        self.cantidad = cantidad
        self.codigo = codigo
        self.codTributo = codTributo
        self.uniMedida = uniMedida
        self.descripcion = descripcion
        self.precioUni = precioUni
        self.montoDescu = montoDescu
        self.ventaNoSuj = ventaNoSuj
        self.ventaExenta = ventaExenta
        self.ventaGravada = ventaGravada
        self.tributos = tributos
        self.psv = psv
        self.noGravado = noGravado
        self.ivaItem = ivaItem


class Tributos:
    def __init__(self, codigo, descripcion, valor):
        self.codigo = codigo
        self.descripcion = descripcion
        self.valor = valor


class Pagos:
    def __init__(self, codigo, montoPago, referencia, plazo, periodo, numPagoElectronico):
        self.codigo = codigo
        self.montoPago = montoPago
        self.referencia = referencia
        self.plazo = plazo
        self.periodo = periodo
        self.numPagoElectronico = numPagoElectronico


class Resumen:
    def __init__(self, totalNoSuj, totalExenta, totalGravada, subTotalVentas, descuNoSuj, descuExenta, descuGravada,
                 porcentajeDescuento, totalDescu, tributos, subTotal, ivaRete1, reteRenta, montoTotalOperacion,
                 totalNoGravado, totalPagar, totalLetras, totalIva, saldoFavor, condicionOperacion, pagos):
        self.totalNoSuj = totalNoSuj
        self.totalExenta = totalExenta
        self.totalGravada = totalGravada
        self.subTotalVentas = subTotalVentas
        self.descuNoSuj = descuNoSuj
        self.descuExenta = descuExenta
        self.descuGravada = descuGravada
        self.porcentajeDescuento = porcentajeDescuento
        self.totalDescu = totalDescu
        self.tributos = tributos
        self.subTotal = subTotal
        self.ivaRete1 = ivaRete1
        self.reteRenta = reteRenta
        self.montoTotalOperacion = montoTotalOperacion
        self.totalNoGravado = totalNoGravado
        self.totalPagar = totalPagar
        self.totalLetras = totalLetras
        self.totalIva = totalIva
        self.saldoFavor = saldoFavor
        self.condicionOperacion = condicionOperacion
        self.pagos = pagos


class Extension:
    def __init__(self, nombreEntrega, docuEntrega, nombreRecibe, docuRecibe, observaciones, placaVehiculo):
        self.nombreEntrega = nombreEntrega
        self.docuEntrega = docuEntrega
        self.nombreRecibe = nombreRecibe
        self.docuRecibe = docuRecibe
        self.observaciones = observaciones
        self.placaVehiculo = placaVehiculo


class Apendice:
    def __init__(self, campo, etiqueta, valor):
        self.campo = campo
        self.etiqueta = etiqueta
        self.valor = valor