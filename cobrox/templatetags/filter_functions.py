from django import template

import datetime
from django.utils.safestring import mark_safe
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Max, Min, Sum
from user.models import user_rol_filial
from django.core.exceptions import ObjectDoesNotExist
from wsfacturae.models  import mastercat,detallemastercat,subactividadeco,actividadeco,municipio, PuntoVenta, param_version_dte

register = template.Library()

@register.simple_tag
def get_rol_by_user(user_id):
    try:
        obj = user_rol_filial.objects.get(usuario__id=user_id).rol.nombre
    except ObjectDoesNotExist:
        obj = '-'
    return obj

@register.simple_tag
def get_filial_by_user(user_id):
    try:
        obj = user_rol_filial.objects.get(usuario__id=user_id).filial.nombre
    except ObjectDoesNotExist:
        obj = '-'
    return obj


@register.simple_tag
def find_hashtag(consulta):
    if consulta:
        while 1:
            hashcount = consulta.find('#')
            if hashcount>0:
                endhas= consulta.find(' ', hashcount)
                if endhas==-1:
                    endhas = len(consulta)
                reempl=consulta[hashcount:endhas]
                consulta = consulta.replace(reempl, '<span class=\"label label-danger\">' + consulta[hashcount+1:endhas] + '</span>')
            else:
                break
    return  mark_safe(consulta)




@register.simple_tag
def filter_sum(monto1, monto2):
    if monto1 is None:
        monto1 = 0
    if monto2 is None:
        monto2 = 0
    return monto1 + monto2



@register.simple_tag
def mostrar_field_obs(nombre):
    if nombre[0:10]=='customobs_':
        return 1
    else:
        return 0


@register.simple_tag
def edad_anos(fecha_nacimiento, consulta):
    anio=  consulta.fecha.year - fecha_nacimiento.year
    return anio

@register.simple_tag
def dia_semana(dia):
    dow = "XX"
    if dia == 0:
        dow = "Lunes"
    elif dia == 1:
        dow = "Martes"
    elif dia == 2:
        dow = "Miércoles"
    elif dia == 3:
        dow = "Jueves"
    elif dia == 4:
        dow = "Viernes"
    elif dia == 5:
        dow = "Sábado"
    elif dia == 6:
        dow = "Domingo"
    return dow


@register.simple_tag
def credito_original(orefinanc):
    try:
        ocredfinanc = creditofinanc.objects.get(credito_nvo=orefinanc)
    except ObjectDoesNotExist:
        return None
    return ocredfinanc.credito_financia

@register.simple_tag
def changeZona(zonaid):
    return zonaid

@register.simple_tag
def suma_objs(mon,actual):
    suma= (mon + actual)
    return suma


@register.simple_tag
def count_catalogo(codigo):
    return detallemastercat.objects.filter(mastercat__codigo= codigo).count()


@register.simple_tag
def muestra_catdet(id_master):
    qs = detallemastercat.objects.filter(mastercat__id=id_master).order_by("codigo")
    devolver = ""
    for entry in qs:
        devolver =devolver+ "<tr>" \
                  "<td>" + entry.codigo +"</td>" \
                  "<td>" + entry.descripcion + "</td>"
        if entry.nm_estado == 1:
            devolver =devolver+"<td>ACTIVO</td>"
        else:
            devolver = devolver + "<td>INACTIVO</td>"
        devolver = devolver + "<td><a href=\"/facturae/detallemastercatUpdate/" + str(entry.id) + "\" ><button type=\"button\" class=\"btn btn-outline btn-warning\"><i class=\"fa fa-edit\"></i></button></a></td>"
        devolver = devolver + "<td><a class =\"confirmacion\" href=\"/facturae/detallemastercatDel/"+ str(entry.id)+ "\" ><button type=\"button\" class=\"btn btn-outline btn-danger\"><i class=\"fa fa-times-circle\"></i></button></a></td></tr>"
    return mark_safe(devolver)


@register.simple_tag
def muestra_subcatae(id_master):
    qs = subactividadeco.objects.filter(catactividadeco__id=id_master).order_by("descripcion")
    devolver = ""
    for entry in qs:
        devolver =devolver+ "<tr>" \
                  "<td>" + entry.descripcion + "</td>"
        qty = actividadeco.objects.filter(subactividadeco=entry).count()
        devolver = devolver + "<td>"+ str(qty) +"</td>"
        if entry.nm_estado == 1:
            devolver =devolver+"<td>ACTIVO</td>"
        else:
            devolver = devolver + "<td>INACTIVO</td>"
        devolver = devolver + "<td><a href=\"/facturae/subcatactividadecoUpdate/" + str(entry.id) + "\" ><button type=\"button\" class=\"btn btn-outline btn-warning\"><i class=\"fa fa-edit\"></i></button></a></td>"
        devolver = devolver + "<td><a class =\"confirmacion\" href=\"/facturae/subcatactividadecoDelete/"+ str(entry.id)+ "\" ><button type=\"button\" class=\"btn btn-outline btn-danger\"><i class=\"fa fa-times-circle\"></i></button></a></td></tr>"
    return mark_safe(devolver)

@register.simple_tag
def muestra_puntoven(id_master):
    qs = PuntoVenta.objects.filter(establecimiento_fk__id=id_master).order_by("codpuntoventa")
    devolver =""
    for entry in qs:
        devolver =devolver+ "<tr>" \
                  "<td>" +str(id_master)  + "</td>"
                  
        devolver = devolver + "<td>"+ entry.codpuntoventa  +"</td>"\
                    +"<td>"+ entry.codpuntoventamh+"</td>"
        devolver = devolver + "<td><a href=\"/facturae/PuntoVentaUpdate/"+str(entry.id)+"\" ><button type=\"button\" class=\"btn btn-outline btn-warning\" title=\'Editar\'><i class=\"fa fa-pencil\"></i></button></a>"\
                                +"&nbsp;<a class=\"confirmacion\" href=\"/facturae/PuntoVentaDelete/"+str(entry.id) +"\" ><button alt=\"Eliminar\" type=\"button\" class=\"btn btn-outline btn-danger\" title=\'Eliminar\'><i class=\"fa fa-times-circle\"></i></button></a></td></tr>"
                            
    return mark_safe(devolver)

@register.simple_tag
def muestra_municipios(id_master):
    qs = municipio.objects.filter(departamento__id=id_master).order_by("codigo")
    devolver = ""
    for entry in qs:
        devolver =devolver+ "<tr>" \
                  "<td>" + entry.codigo +"</td>" \
                  "<td>" + entry.descripcion + "</td>"
        if entry.nm_estado == 1:
            devolver =devolver+"<td>ACTIVO</td>"
        else:
            devolver = devolver + "<td>INACTIVO</td>"
        devolver = devolver + "<td><a href=\"/facturae/municipioUpdate/" + str(entry.id) + "\" ><button type=\"button\" class=\"btn btn-outline btn-warning\"><i class=\"fa fa-edit\"></i></button></a></td>"
        devolver = devolver + "<td><a class =\"confirmacion\" href=\"/facturae/municipioDel/"+ str(entry.id)+ "\" ><button type=\"button\" class=\"btn btn-outline btn-danger\"><i class=\"fa fa-times-circle\"></i></button></a></td></tr>"
    return mark_safe(devolver)


@register.simple_tag
def count_municipios(codigo):
    return municipio.objects.filter(departamento__codigo= codigo).count()

@register.simple_tag
def round_numbers(number):
    to_round = param_version_dte.objects.get(codigo="1004")
    return round(number, int(to_round.tipoDato))

@register.simple_tag
def custom_floatformat(value):
    to_round = param_version_dte.objects.get(codigo="1004")
    decimals = int(to_round.tipoDato)
    return '{number:.{precision}}'.format(number=value, precision=decimals)