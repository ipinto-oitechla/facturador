import requests
import json
from .models import wsurl,wsentorno
from django.conf import settings


def ws_url_firma(codigo_url):
    owe = wsentorno.objects.get(codigo=getattr(settings, 'WS_ENTORNO_FIRMA', None))
    owurl = wsurl.objects.get(codigo=codigo_url)
    return owe.url + owurl.url


def ws_url(codigo_url):
    owe = wsentorno.objects.get(codigo=getattr(settings, 'WS_ENTORNO', None))
    owurl = wsurl.objects.get(codigo=codigo_url)
    return owe.url + owurl.url


def ws_autenticacion(contenttype,url,user_agent, user, pwd):
    headers = {
        "Content-Type": contenttype,
        "User-Agent": user_agent
    }
    data = {
        "user": user,
        "pwd": pwd
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.dumps(data), response.json()


def ws_firmador_documento(contenttype, url, nit, activo, passwordPri, dteJson):
    headers = {
        "Content-Type": contenttype,
    }
    data = {
        "nit": nit,
        "activo": activo,
        "passwordPri":passwordPri,
        "dteJson":dteJson
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.dumps(data), response.json()


def ws_recepciondte(contenttype, url, token,user_agent, ambiente, idEnvio, version,tipoDte,documento,codigoGeneracion):
    headers = {
        "Authorization": token,
        "User-Agent":user_agent,
        "content-Type": contenttype,
    }
    data = {
        "ambiente": ambiente,
        "idEnvio": idEnvio,
        "version": version,
        "tipoDte": tipoDte,
        "documento": documento,
        "codigoGeneracion": codigoGeneracion,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.dumps(data), response.json()


def ws_recepcionlote(contenttype, url, token,user_agent, ambiente, idEnvio, version,nitemisor, documentos):
    headers = {
        "Authorization": token,
        "User-Agent":user_agent,
        "content-Type": contenttype,
    }
    data = {
        "ambiente": ambiente,
        "idEnvio": idEnvio,
        "version": version,
        "nitEmisor": nitemisor,
        "documentos": documentos,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.dumps(data), response.json()


def ws_consultadte(contenttype, url, token,user_agent, nitemisor, tipoDte, codigoGeneracion):
    headers = {
        "Authorization": token,
        "User-Agent":user_agent,
        "content-Type": contenttype,
    }
    data = {
        "nitEmisor": nitemisor,
        "tdte": tipoDte,
        "codigoGeneracion": codigoGeneracion,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.dumps(data), response.json()


def ws_consultadtelote(contenttype, url, token,user_agent, codigolote):
    headers = {
        "Authorization": token,
        "User-Agent":user_agent,
        "content-Type": contenttype,
    }
    data = {
        "codigoLote": codigolote,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.dumps(data), response.json()


def ws_contingencia(contenttype, url, token,user_agent, nitemisor,documento):
    headers = {
        "Authorization": token,
        "User-Agent":user_agent,
        "content-Type": contenttype,
    }
    data = {
        "nit": nitemisor,
        "documento":documento
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.dumps(data), response.json()


def ws_anulardte(contenttype, url, token,user_agent, ambiente,idenvio,version,documento):
    headers = {
        "Authorization": token,
        "User-Agent":user_agent,
        "content-Type": contenttype,
    }
    data = {
        "ambiente": ambiente,
        "idEnvio": idenvio,
        "version": version,
        "documento": documento,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.dumps(data), response.json()


def ws_forma_data_facturacion(oidentificacion,odocumentorelacionados,oemisor,oreceptor,
                              ootrosdocumento,otercero,ocuerpodocumento,oresumen,oextension,
                              oapendice):
    data = {
        "identificacion": {
            "version": oidentificacion.version,
            "ambiente": oidentificacion.ambiente,
            "tipoDte": oidentificacion.tipoDte,
            "numeroControl": oidentificacion.numeroControl,
            "codigoGeneracion":oidentificacion.codigoGeneracion,
            "tipoModelo":oidentificacion.tipoModelo,
            "tipoOperacion": oidentificacion.tipoOperacion,
            "tipoContingencia": oidentificacion.tipoContingencia,
            "motivoContin": oidentificacion.motivoContin,
            "fecEmi": oidentificacion.fecEmi,
            "horEmi":oidentificacion.horEmi,
            "tipoMoneda":oidentificacion.tipoMoneda,
        },
        "documentoRelacionado": {
            "tipoDocumento": odocumentorelacionados.tipoDocumento,
            "tipoGeneracion": odocumentorelacionados.tipoGeneracion,
            "numeroDocumento": odocumentorelacionados.numeroDocumento,
            "fechaEmision":  odocumentorelacionados.fechaEmision,
        },
        "emisor": {
            "nit": oemisor.nit,
            "nrc": oemisor.nrc,
            "nombre": oemisor.nombre,
            "codActividad": oemisor.codActividad,
            "desActividad": oemisor.desActividad,
            "nombreComercial": oemisor.nombreComercial,
            "tipoEstablecimiento": oemisor.tipoEstablecimiento,
            "direccion": {
                "departamento": oemisor.departamento,
                "municipio": oemisor.municipio,
                "complemento": oemisor.complemento,
            },
            "telefono":  oemisor.telefono,
            "codEstableMH": oemisor.codEstableMH,
            "codEstable": oemisor.codEstable,
            "codPuntoVentaMH": oemisor.codPuntoVentaMH,
            "codPuntoVenta": oemisor.codPuntoVenta,
            "correo": oemisor.correo,
        },
        "receptor": {
            "tipoDocumento": oreceptor.tipoDocumento,
            "numDocumento": oreceptor.numDocumento,
            "nrc": oreceptor.nrc,
            "nombre": oreceptor.nombre,
            "codActividad": oreceptor.codActividad,
            "desActividad": oreceptor.desActividad,
            "direccion": {
                "departamento": oreceptor.departamento,
                "municipio": oreceptor.municipio,
                "complemento": oreceptor.complemento,
            },
            "telefono": oreceptor.telefono,
            "correo": oreceptor.correo,
        },
        "otrosDocumentos": {
            "codDocAsociado": ootrosdocumento.codDocAsociado,
            "descDocumento": ootrosdocumento.descDoccumento,
            "detalleDocumento": ootrosdocumento.detalleDocumento,
            "medico": {
                "nombre":ootrosdocumento.medico.nombre,
                "nit": ootrosdocumento.medico.nit,
                "docIdentificacion": ootrosdocumento.medico.docIdentificacion,
                "tipoServicio": ootrosdocumento.medico.tipoServicio,
            },
            "tipoGeneracion": odocumentorelacionados.tipoGeneracion,
            "numeroDocumento": odocumentorelacionados.numeroDocumento,
            "fechaEmision": odocumentorelacionados.fechaEmision,
        },
        "ventaTercero": {
            "nit": otercero.nit,
            "nombre": otercero.nombre,
        },
        "cuerpoDocumento": {
            "numItem": ocuerpodocumento.numItem,
            "tipoItem": ocuerpodocumento.tipoItem,
            "numeroDocumento": ocuerpodocumento.numeroDocumento,
            "cantidad": ocuerpodocumento.cantidad,
            "codigo": ocuerpodocumento.codigo,
            "codTributo": ocuerpodocumento.codTributo,
            "uniMedida": ocuerpodocumento.uniMedida,
            "descripcion": ocuerpodocumento.descripcion,
            "precioUni": ocuerpodocumento.precioUni,
            "montoDescu": ocuerpodocumento.montoDescu,
            "ventaNoSuj": ocuerpodocumento.ventaNoSuj,
            "ventaExenta": ocuerpodocumento.ventaExenta,
            "ventaGravada": ocuerpodocumento.ventaGravada,
            "tributos": ocuerpodocumento.tributos,
            "psv": ocuerpodocumento.psv,
            "noGravado": ocuerpodocumento.noGravado,
            "ivaItem": ocuerpodocumento.ivaItem,
        },
        "resumen": {
            "totalNoSuj": oresumen.totalNoSuj,
            "totalExenta": oresumen.totalExenta,
            "totalGravada": oresumen.totalGravada,
            "subTotalVentas":  oresumen.subTotalVentas,
            "descuNoSuj":  oresumen.descuNoSuj,
            "descuExenta":  oresumen.descuExenta,
            "descuGravada":  oresumen.descuGravada,
            "porcentajeDescuento":  oresumen.porcentajeDescuento,
            "totalDescu":  oresumen.totalDescu,
            "tributos":{
                "codigo":  oresumen.tributos.codigo,
                "descripcion": oresumen.tributos.descripcion,
                "valor": oresumen.tributos.valor,
            },
            "subTotal": oresumen.subTotal,
            "ivaRete1": oresumen.ivaRete1,
            "reteRenta": oresumen.reteRenta,
            "montoTotalOperacion":oresumen.montoTotalOperacion,
            "totalNoGravado":oresumen.totalNoGravado,
            "totalPagar":oresumen.totalPagar,
            "totalLetras":oresumen.totalLetras,
            "totalIva": oresumen.totalIva,
            "saldoFavor": oresumen.saldoFavor,
            "condicionOperacion": oresumen.condicionOperacion,
            "pagos":{
                "codigo":oresumen.pagos.codigo,
                "montoPago": oresumen.pagos.montoPago,
                "referencia": oresumen.pagos.referencia,
                "plazo": oresumen.pagos.plazo,
                "periodo": oresumen.pagos.periodo,
                "numPagoElectronico": oresumen.pagos.numPagoElectronico,
                },
        },
        "extension": {
            "nombreEntrega": oextension.nombreEntrega,
            "docuEntrega": oextension.docuEntrega,
            "nombreRecibe": oextension.nombreRecibe,
            "docuRecibe": oextension.docuRecibe,
            "observaciones": oextension.observaciones,
            "placaVehiculo": oextension.placaVehiculo,
        },
        "apendice": {
            "campo": oapendice.campo,
            "etiqueta": oextension.etiqueta,
            "valor": oextension.valor,
        }
    }
    return data