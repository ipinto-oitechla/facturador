from wsentidad import ws_autenticacion,ws_autenticacion_log,ws_firmador_documento
from django.conf import settings
from .models import tiporespuestac
from datetime import datetime, timedelta


def crea_object_ws_autenticacion_log(user_enviado,jenviado,jrespuesta,token,tiporespuesta,mensajeerror):
    ows_autenticacion_log = ws_autenticacion_log();
    ows_autenticacion_log.user_enviado = user_enviado;
    ows_autenticacion_log.token = token;
    ows_autenticacion_log.tiporespuesta=tiporespuesta;
    ows_autenticacion_log.mensajeerror=mensajeerror
    if not getattr(settings, 'WS_DEBUG', None):
        ows_autenticacion_log.jenviado = jenviado
        ows_autenticacion_log.jrespuesta = jrespuesta
    ows_autenticacion_log.save()


def fn_valida_vigencia_token(fecha_ultima):
    fecha_actual = datetime.now()
    tiempohrs = timedelta(hours=getattr(settings, 'WS_TOKEN_VIGENCIA', None))
    diferencia = fecha_actual - fecha_ultima
    if diferencia > tiempohrs:
        return tiporespuestac.is_error
    else:
        return tiporespuestac.is_exito


def fn_firmar_documento(url, nit, activo, passwordPri, dteJson):
    response_json = ws_firmador_documento(url,nit, activo, passwordPri, dteJson)
    status = response_json["status"]
    if status == 'OK':
        return tiporespuestac.is_exito,response_json
    else:
        body = response_json["body"]
        return tiporespuestac.is_error,body


def fn_obtener_token():
    user_agent = getattr(settings, 'WS_USER_AGENT', None)
    user = getattr(settings, 'WS_USER', None)
    pwd = getattr(settings, 'WS_USER_PWD', None)

    jenviado, response_json = ws_autenticacion(user_agent, user, pwd)
    status = response_json["status"]
    mensajeerror = None;
    token = None;
    if status=='OK':
        tipo_respuesta = tiporespuestac.is_exito
        body = response_json["body"]
        token = body["token"]
        token_type = body["tokenType"]
        roles = body["roles"]
        rol = roles[0]  # Suponiendo que solo se quiere el primer rol en la lista
    else:
        mensajeerror = response_json["error"] +'-'+ response_json["message"]
        tipo_respuesta = tiporespuestac.is_error

    crea_object_ws_autenticacion_log(user,jenviado,response_json,token,tipo_respuesta,mensajeerror)
    return token;


def fn_token_vigente():
    qry = ws_autenticacion_log.objects.filter(tiporespuesta= tiporespuestac.is_exito).order_by("id")
    ultimo_objeto = qry.last()
    if ultimo_objeto is not None:
        if fn_valida_vigencia_token(ultimo_objeto.date_creation):
            return ultimo_objeto.token;
    else:
        return fn_obtener_token;




