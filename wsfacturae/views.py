from datetime import datetime
import traceback
from typing import Any, Dict, List
from django.db.models.query import QuerySet
from django.views import View
from .models import EmisorN, Establecimiento, Identificacion, JsonFac, PuntoVenta, pagosfactura, param_version_dte,\
    wsentorno,wsurl,mastercat,detallemastercat,catactividadeco,subactividadeco,actividadeco,departamento,municipio,\
        tributo, ReceptorN,Productos, Factura, DetalleFactura, Descuento, Hacienda, Estado, SMTP
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView,DetailView, FormView,TemplateView)
from django.http import FileResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from .forms import AgregarMetodoPagoForm, EmisorNUpdateForm, EstablecimientoAddForm, EstablecimientoUpdateForm, PuntoVentaAddForm, ReceptorAddForm, ReceptorSearchForm, ReceptorUpdateForm, WsEntornoAddForm,WsEntornoUpdateForm,WsUrlAddForm,WsUrlUpdateForm,MastercatAddForm,\
    MastercatUpdateForm,DetalleMastercatAddForm,DetalleMastercatUpdateForm,CategoriaAEAddForm,CategoriaAEUpdForm,\
    SubCategoriaAEAddForm,SubCategoriaAEUpdForm,ActividadecoUpdForm,ActividadecoAddForm,ActividadecoSearchForm,\
    DepartamentoAddForm,DepartamentoUpdateForm,MunicipioUpdateForm, MunicipioAddForm,TributoAddForm,TributoUpdateForm,\
    ConsultaDteSearchForm, InsertarDteForm, AgregarProductoForm, AddProductoForm, DescuentoAddForm, SMTPUpdateForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.http import Http404
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError, models, transaction
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.mixins import UserPassesTestMixin
#----------------------------O-------------------------------
import requests, qrcode, base64, json
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.core.mail import EmailMultiAlternatives
from wsfacturae import utils
from cobrox.templatetags.filter_functions import round_numbers



class WsEntornoDelete(SuccessMessageMixin, UserPassesTestMixin,LoginRequiredMixin, DeleteView):
    model = wsentorno
    success_url = reverse_lazy('wsfacturae:WsEntornoList')
    form_valid_message = 'La WsEntorno fué eliminada satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = wsentorno.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El wsentorno ha sido eliminado satisfactoriamente.")
            my_render = reverse_lazy('wsfacturae:WsEntornoList')
        except IntegrityError as e:
            messages.error(request, "El wsentorno no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse_lazy('wsfacturae:WsEntornoList')
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff


class WsEntornoUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = wsentorno
    form_class = WsEntornoUpdateForm
    success_url = reverse_lazy('wsfacturae:WsEntornoList')
    template_name = 'wsfacturae/wsentorno_add_upd.html'
    success_message = 'Información del WsEntorno Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff


class WsEntornoList(UserPassesTestMixin,LoginRequiredMixin, ListView):
    model = wsentorno
    template_name = 'wsfacturae/wsentorno_list.html'
    permission_required = ('user.is_staff')

    def get_queryset(self):
        return wsentorno.objects.all()

    def test_func(self):
        return self.request.user.is_staff


class WsEntornoAdd(SuccessMessageMixin, UserPassesTestMixin,LoginRequiredMixin, CreateView):
    form_class = WsEntornoAddForm
    template_name = 'wsfacturae/wsentorno_add_upd.html'
    success_url = reverse_lazy('wsfacturae:WsEntornoList')
    success_message = 'Información del WsEntorno Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff


class WsUrlDelete(SuccessMessageMixin, UserPassesTestMixin,LoginRequiredMixin, DeleteView):
    model = wsurl
    success_url = reverse_lazy('wsfacturae:WsUrlList')
    form_valid_message = 'La WsUrl fué eliminada satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = wsurl.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El wsurl ha sido eliminado satisfactoriamente.")
            my_render = reverse_lazy('wsfacturae:WsUrlList')
        except IntegrityError as e:
            messages.error(request, "El wsurl no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse_lazy('wsfacturae:WsUrlList')
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff


class WsUrlUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = wsurl
    form_class = WsUrlUpdateForm
    success_url = reverse_lazy('wsfacturae:WsUrlList')
    template_name = 'wsfacturae/wsurl_add_upd.html'
    success_message = 'Información del WsUrl Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff


class WsUrlList(UserPassesTestMixin,LoginRequiredMixin, ListView):
    model = wsurl
    template_name = 'wsfacturae/wsurl_list.html'
    permission_required = ('user.is_staff')

    def get_queryset(self):
        return wsurl.objects.all()

    def test_func(self):
        return self.request.user.is_staff


class WsUrlAdd(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = WsUrlAddForm
    template_name = 'wsfacturae/wsurl_add_upd.html'
    success_url = reverse_lazy('wsfacturae:WsUrlList')
    success_message = 'Información del WsUrl Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff


class MastercatDelete(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = mastercat
    success_url = reverse_lazy('wsfacturae:MastercatList')
    form_valid_message = 'La Mastercat fué eliminada satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = mastercat.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El mastercat ha sido eliminado satisfactoriamente.")
            my_render = reverse_lazy('wsfacturae:MastercatList')
        except IntegrityError as e:
            messages.error(request, "El mastercat no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse_lazy('wsfacturae:MastercatList')
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff


class MastercatUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = mastercat
    form_class = MastercatUpdateForm
    success_url = reverse_lazy('wsfacturae:MastercatList')
    template_name = 'wsfacturae/mastercat_add_upd.html'
    success_message = 'Información del Mastercat Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff


class MastercatList(UserPassesTestMixin,LoginRequiredMixin, ListView):
    model = mastercat
    template_name = 'wsfacturae/mastercat_list.html'
    permission_required = ('user.is_staff')

    def get_queryset(self):
        return mastercat.objects.all().order_by("codigo")

    def test_func(self):
        return self.request.user.is_staff


class MastercatAdd(SuccessMessageMixin, UserPassesTestMixin,LoginRequiredMixin, CreateView):
    form_class = MastercatAddForm
    template_name = 'wsfacturae/mastercat_add_upd.html'
    success_url = reverse_lazy('wsfacturae:MastercatList')
    success_message = 'Información del Mastercat Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        return {
            'nm_estado': 1
        }


class DetalleMastercatAdd(SuccessMessageMixin, UserPassesTestMixin,LoginRequiredMixin, CreateView):
    form_class = DetalleMastercatAddForm
    template_name = 'wsfacturae/detallemastercat_add_upd.html'
    success_url = reverse_lazy('wsfacturae:MastercatList')
    success_message = 'Información del Detalle Mastercat Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def catalogo(self):
        return mastercat.objects.get(id=self.kwargs[self.pk_url_kwarg])

    def get_initial(self):
        return {
            'nm_estado': 1,
            'mastercat': self.kwargs[self.pk_url_kwarg]
        }

    def get_context_data(self, **kwargs):
        context = super(DetalleMastercatAdd, self).get_context_data(**kwargs)
        context['detalle'] = detallemastercat.objects.filter(mastercat__id=self.kwargs['pk']).order_by("codigo")
        return context

    def get_success_url(self):
        return reverse('wsfacturae:DetalleMastercatAdd',kwargs={'pk': self.kwargs[self.pk_url_kwarg]})




class DetalleMastercatDelete(SuccessMessageMixin, UserPassesTestMixin,LoginRequiredMixin, DeleteView):
    model = detallemastercat
    success_url = reverse_lazy('wsfacturae:MastercatList')
    form_valid_message = 'El Ítem fué eliminado satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = detallemastercat.objects.get(id=self.kwargs[self.pk_url_kwarg])
            master = obj.mastercat.id
            obj.delete()
            messages.success(request, "El ítem ha sido eliminado satisfactoriamente.")
            my_render = reverse('wsfacturae:DetalleMastercatAdd',kwargs={'pk':master})
        except IntegrityError as e:
            messages.error(request, "El ítem no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse('wsfacturae:DetalleMastercatAdd',kwargs={'pk': master})
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff


class DetalleMastercatUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = detallemastercat
    form_class = DetalleMastercatUpdateForm
    success_url = reverse_lazy('wsfacturae:MastercatList')
    template_name = 'wsfacturae/detallemastercat_add_upd.html'
    success_message = 'Información del ítem Almacenada Correctamente!!!!'

    def catalogo(self):
        return detallemastercat.objects.get(id=self.kwargs[self.pk_url_kwarg]).mastercat

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        idm= detallemastercat.objects.get(id=self.kwargs[self.pk_url_kwarg]).mastercat.id
        return reverse('wsfacturae:DetalleMastercatAdd',kwargs={'pk': idm})


class CatactividadecoDelete(SuccessMessageMixin, UserPassesTestMixin,LoginRequiredMixin, DeleteView):
    model = catactividadeco
    success_url = reverse_lazy('wsfacturae:CatactividadecoList')
    form_valid_message = 'La Catactividadeco fué eliminada satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = catactividadeco.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El catactividadeco ha sido eliminado satisfactoriamente.")
            my_render = reverse_lazy('wsfacturae:CatactividadecoList')
        except IntegrityError as e:
            messages.error(request, "El catactividadeco no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse_lazy('wsfacturae:CatactividadecoList')
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff


class CatactividadecoUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = catactividadeco
    form_class = CategoriaAEUpdForm
    success_url = reverse_lazy('wsfacturae:CatactividadecoList')
    template_name = 'wsfacturae/categoria_ae_add_upd.html'
    success_message = 'Información del Catactividadeco Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff


class CatactividadecoList(UserPassesTestMixin,LoginRequiredMixin, ListView):
    model = catactividadeco
    template_name = 'wsfacturae/categoria_ae_list.html'
    permission_required = ('user.is_staff')

    def get_queryset(self):
        return catactividadeco.objects.all().order_by("descripcion")

    def test_func(self):
        return self.request.user.is_staff


class CatactividadecoAdd(SuccessMessageMixin, UserPassesTestMixin,LoginRequiredMixin, CreateView):
    form_class = CategoriaAEAddForm
    template_name = 'wsfacturae/categoria_ae_add_upd.html'
    success_url = reverse_lazy('wsfacturae:CatactividadecoList')
    success_message = 'Información del Catactividadeco Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        return {
            'nm_estado': 1
        }


class SubCatactividadecoDelete(SuccessMessageMixin, UserPassesTestMixin,LoginRequiredMixin, DeleteView):
    model = subactividadeco
    success_url = reverse_lazy('wsfacturae:SubCatactividadecoList')
    form_valid_message = 'La SubCatactividadeco fué eliminada satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = subactividadeco.objects.get(id=self.kwargs[self.pk_url_kwarg])
            master = obj.catactividadeco.id
            obj.delete()
            messages.success(request, "El subcatactividadeco ha sido eliminado satisfactoriamente.")
            my_render = reverse_lazy('wsfacturae:SubCatactividadecoAdd',kwargs={'pk':master})
        except IntegrityError as e:
            messages.error(request, "El subcatactividadeco no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse_lazy('wsfacturae:SubCatactividadecoAdd',kwargs={'pk':master})
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff


class SubCatactividadecoUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = subactividadeco
    form_class = SubCategoriaAEUpdForm
    success_url = reverse_lazy('wsfacturae:SubCatactividadecoList')
    template_name = 'wsfacturae/subcategoria_ae_add_upd.html'
    success_message = 'Información del SubCatactividadeco Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def catactividadeco(self):
        return subactividadeco.objects.get(id=self.kwargs[self.pk_url_kwarg]).catactividadeco

    def get_success_url(self):
        idm= subactividadeco.objects.get(id=self.kwargs[self.pk_url_kwarg]).catactividadeco.id
        return reverse('wsfacturae:SubCatactividadecoAdd',kwargs={'pk': idm})


class SubCatactividadecoList(UserPassesTestMixin,LoginRequiredMixin, ListView):
    model = subactividadeco
    template_name = 'wsfacturae/subcategoria_ae_list.html'
    permission_required = ('user.is_staff')

    def get_queryset(self):
        return subactividadeco.objects.all().order_by("descripcion")

    def test_func(self):
        return self.request.user.is_staff


class SubCatactividadecoAdd(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = SubCategoriaAEAddForm
    template_name = 'wsfacturae/subcategoria_ae_add_upd.html'
    success_url = reverse_lazy('wsfacturae:SubCatactividadecoList')
    success_message = 'Información del SubCatactividadeco Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        return {
            'nm_estado': 1,
            'catactividadeco': self.kwargs[self.pk_url_kwarg]
        }

    def catactividadeco(self):
        return catactividadeco.objects.get(id=self.kwargs[self.pk_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super(SubCatactividadecoAdd, self).get_context_data(**kwargs)
        context['detalle'] = subactividadeco.objects.filter(catactividadeco__id=self.kwargs['pk']).order_by("descripcion")
        return context;

    def get_success_url(self):
        return reverse('wsfacturae:SubCatactividadecoAdd', kwargs={'pk': self.kwargs[self.pk_url_kwarg]})


class ActividadecoDelete(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = actividadeco
    success_url = reverse_lazy('wsfacturae:ActividadecoList')
    form_valid_message = 'El actividadeco fue eliminado satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = actividadeco.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El actividadeco ha sido eliminado satisfactoriamente.")
            my_render = reverse_lazy('wsfacturae:ActividadecoList')
        except IntegrityError as e:
            messages.error(request, "La actividadeco no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse_lazy('wsfacturae:ActividadecoList')
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff


class ActividadecoUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = actividadeco
    form_class = ActividadecoUpdForm
    success_url = reverse_lazy('wsfacturae:ActividadecoList')
    template_name = 'wsfacturae/actividadeco_add_upd.html'
    success_message = 'Informacion de Actividadeco Almacenada Correctamente!!!!'

    def form_valid(self, form ):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        initial = super().get_initial()
        catactividadeco_id = self.object.subactividadeco.catactividadeco.id if self.object.subactividadeco.catactividadeco else None

        if catactividadeco_id:
            opciones_catactividadeco = catactividadeco.objects.filter(id=catactividadeco_id).filter(nm_estado=1).order_by("descripcion")
            initial['catactividadeco'] = opciones_catactividadeco.first()

        else:
            initial['catactividadeco'] = None
            initial['subactividadeco'] = []
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['query_subactividadeco'] = subactividadeco.objects.filter(nm_estado=1).order_by("descripcion")
        return kwargs


class ActividadecoList(UserPassesTestMixin,LoginRequiredMixin, FormMixin,ListView):
    paginate_by = getattr(settings, 'NUM_RECS_BY_PAG', None)
    form_class = ActividadecoSearchForm
    template_name = 'wsfacturae/actividadeco_list.html'
    ajax_template_name = 'wsfacturae/actividadeco_list_results.html'

    def get_initial(self):
        return {
            'descripcion': '',
        }

    def get_queryset(self):
        qry = actividadeco.objects.all().order_by("descripcion", "id")
        return qry

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        return [self.template_name]

    def get_form_kwargs(self):
        return {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'data': self.request.GET or None
        }

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            self.object_list = form.filter_queryset(request, self.object_list)
        context = self.get_context_data(form=form, object_list=self.object_list)
        return self.render_to_response(context)

    def paginate_queryset(self, queryset, page_size):
        try:
            return super(ActividadecoList, self).paginate_queryset(queryset, page_size)
        except Http404:
            self.kwargs['page'] = 'last'
            return super(ActividadecoList, self).paginate_queryset(queryset, page_size)

    def test_func(self):
        return self.request.user.is_staff


class ActividadecoAdd(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ActividadecoAddForm
    template_name = 'wsfacturae/actividadeco_add_upd.html'
    success_url = reverse_lazy('wsfacturae:ActividadecoList')
    success_message = 'Informacion de Actividadeco Almacenada Correctamente!!!!'

    def get_success_url(self):
        return reverse('wsfacturae:ActividadecoList')

    def form_valid(self, form ):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff


class DepartamentoDelete(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = departamento
    success_url = reverse_lazy('wsfacturae:DepartamentoList')
    form_valid_message = 'La Departamento fué eliminada satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = departamento.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El departamento ha sido eliminado satisfactoriamente.")
            my_render = reverse_lazy('wsfacturae:DepartamentoList')
        except IntegrityError as e:
            messages.error(request, "El departamento no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse_lazy('wsfacturae:DepartamentoList')
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff


class DepartamentoUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = departamento
    form_class = DepartamentoUpdateForm
    success_url = reverse_lazy('wsfacturae:DepartamentoList')
    template_name = 'wsfacturae/departamento_add_upd.html'
    success_message = 'Información del Departamento Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff


class DepartamentoList(UserPassesTestMixin,LoginRequiredMixin, ListView):
    model = departamento
    template_name = 'wsfacturae/departamento_list.html'
    permission_required = ('user.is_staff')

    def get_queryset(self):
        return departamento.objects.all().order_by("codigo")

    def test_func(self):
        return self.request.user.is_staff


class DepartamentoAdd(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = DepartamentoAddForm
    template_name = 'wsfacturae/departamento_add_upd.html'
    success_url = reverse_lazy('wsfacturae:DepartamentoList')
    success_message = 'Información del Departamento Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        return {
            'nm_estado': 1
        }


class MunicipioAdd(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = MunicipioAddForm
    template_name = 'wsfacturae/municipio_add_upd.html'
    success_url = reverse_lazy('wsfacturae:DepartamentoList')
    success_message = 'Información del Detalle Departamento Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def departamento(self):
        return departamento.objects.get(id=self.kwargs[self.pk_url_kwarg])

    def get_initial(self):
        return {
            'nm_estado': 1,
            'departamento': self.kwargs[self.pk_url_kwarg]
        }

    def get_context_data(self, **kwargs):
        context = super(MunicipioAdd, self).get_context_data(**kwargs)
        context['detalle'] = municipio.objects.filter(departamento__id=self.kwargs['pk']).order_by("codigo")
        return context;

    def get_success_url(self):
        return reverse('wsfacturae:MunicipioAdd',kwargs={'pk': self.kwargs[self.pk_url_kwarg]})


class MunicipioDelete(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = municipio
    success_url = reverse_lazy('wsfacturae:DepartamentoList')
    form_valid_message = 'El Ítem fué eliminado satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = municipio.objects.get(id=self.kwargs[self.pk_url_kwarg])
            master = obj.departamento.id
            obj.delete()
            messages.success(request, "El ítem ha sido eliminado satisfactoriamente.")
            my_render = reverse('wsfacturae:MunicipioAdd',kwargs={'pk':master})
        except IntegrityError as e:
            messages.error(request, "El ítem no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse('wsfacturae:MunicipioAdd',kwargs={'pk': master})
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff


class MunicipioUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = municipio
    form_class = MunicipioUpdateForm
    success_url = reverse_lazy('wsfacturae:DepartamentoList')
    template_name = 'wsfacturae/municipio_add_upd.html'
    success_message = 'Información del ítem Almacenada Correctamente!!!!'

    def departamento(self):
        return municipio.objects.get(id=self.kwargs[self.pk_url_kwarg]).departamento

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        idm= municipio.objects.get(id=self.kwargs[self.pk_url_kwarg]).departamento.id
        return reverse('wsfacturae:MunicipioAdd',kwargs={'pk': idm})


def load_subact(request):
    cat_id = request.GET.get('categoria')
    subacts = subactividadeco.objects.filter(catactividadeco__id=cat_id).filter(nm_estado=1).order_by('descripcion')
    return render(request, 'wsfacturae/items_dropdown_list.html', {'items': subacts})


def load_muni(request):
    dep_id = request.GET.get('departamento')
    munis = municipio.objects.filter(departamento__id=dep_id).filter(nm_estado=1).order_by('descripcion')
    return render(request, 'wsfacturae/items_dropdown_list.html', {'items': munis})


def load_acteco(request):
    subcat_id = request.GET.get('subcategoria')
    actecos = actividadeco.objects.filter(subactividadeco__id=subcat_id).filter(nm_estado=1).order_by('descripcion')
    return render(request, 'wsfacturae/items_dropdown_list.html', {'items': actecos})


class TributoAdd(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = TributoAddForm
    template_name = 'wsfacturae/tributo_add_upd.html'
    success_url = reverse_lazy('wsfacturae:TributoList')
    success_message = 'Información del Detalle Tributo Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        return {
            'nm_estado': 1,
        }

    def get_context_data(self, **kwargs):
        context = super(TributoAdd, self).get_context_data(**kwargs)
        context['detalle'] = tributo.objects.all().order_by("seccion","codigo")
        return context;

    def get_success_url(self):
        return reverse('wsfacturae:TributoAdd')


class TributoDelete(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = tributo
    success_url = reverse_lazy('wsfacturae:TributoList')
    form_valid_message = 'El Ítem fué eliminado satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = tributo.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El ítem ha sido eliminado satisfactoriamente.")
            my_render = reverse('wsfacturae:TributoAdd')
        except IntegrityError as e:
            messages.error(request, "El ítem no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse('wsfacturae:TributoAdd')
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff


class TributoUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = tributo
    form_class = TributoUpdateForm
    success_url = reverse_lazy('wsfacturae:TributoList')
    template_name = 'wsfacturae/tributo_add_upd.html'
    success_message = 'Información del ítem Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('wsfacturae:TributoAdd')

    def get_context_data(self, **kwargs):
        context = super(TributoUpdate, self).get_context_data(**kwargs)
        context['detalle'] = tributo.objects.all().order_by("seccion","codigo")
        return context;


class TributoList(UserPassesTestMixin,LoginRequiredMixin, ListView):
    model = tributo
    template_name = 'wsfacturae/tributo_list.html'
    permission_required = ('user.is_staff')

    def get_queryset(self):
        return tributo.objects.all().order_by("seccion","codigo")

    def test_func(self):
        return self.request.user.is_staff
    
class DteList(UserPassesTestMixin,FormMixin,LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = 'wsfacturae/documtrib_list.html'
    ajax_template_name='wsfacturae/documtrib_list_result.html'
    form_class = ConsultaDteSearchForm

    def get_queryset(self):
        qry = Factura.objects.order_by("-fecha")
        return qry
    
    def get_context_data(self, **kwargs):
        estado_choices = {
            '1': 'Enviado',
            '2': 'En Proceso',
            '3': 'Entregado',
            }
        context = super().get_context_data(**kwargs)
        
        return context
    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        return [self.template_name]
    
    def get_form_kwargs(self):
        return {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'data': self.request.GET or None
        }
    

    def get(self, request):
        self.object_list = self.get_queryset()
        form = self.get_form(self.get_form_class())
        if form.is_valid():

            self.object_list = form.filter_queryset(request, self.object_list)
        context = self.get_context_data(object_list=self.object_list, form=form)
        return self.render_to_response(context)
    
    def paginate_queryset(self, queryset, page_size):
        try:
            return super(DteList, self).paginate_queryset(queryset, page_size)
        except Http404:
            self.kwargs['page'] = 'last'
            return super(DteList, self).paginate_queryset(queryset, page_size)
    
    def test_func(self):
        return self.request.user.is_staff
    

class DteDetail(LoginRequiredMixin, ListView):
    model = Factura
    template_name = 'wsfacturae/dte_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dte_object'] = Factura.objects.get(id=self.kwargs.get('pk'))
        return context


class MyPDFViewMixin:
    template_path = 'wsfacturae/pdf1.html'

    def get_image_url(self):
        #url statica decodificada en el QR
        url= "https://picsum.photos/id/237/200/300"
        qr = qrcode.QRCode(version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=3,
                        border=4,)
        qr.add_data(url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        #Convertir qr_image a bytes64 para pasarlo al pdf
        buffered = BytesIO()
        qr_image.save(buffered, format="PNG")
        qr_image_base64 = base64.b64encode(buffered.getvalue()).decode()
        return "data:image/png;base64," + qr_image_base64

    def generate_pdf_content(self, context):
        template = get_template(self.template_path)
        html = template.render(context)

        pdf_buffer = BytesIO()
        pisa.CreatePDF(html, dest=pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        pdf_buffer.close()

        return pdf_content

    def get_context_data(self, *args, **kwargs):
        context = {}
        factura = get_object_or_404(Factura, id=self.kwargs.get('pk'))
        detalle = DetalleFactura.objects.filter(fk_factura=factura)
        tributo = DetalleFactura.objects.values_list('fk_Producto__tributo__descripcion', flat=True).distinct()
        valores = DetalleFactura.objects.values_list('fk_Producto__tributo__valor', flat=True).distinct()
        context['factura'] = factura
        context['detalle'] = detalle
        context['tributos']=tributo
        context['valores']=valores
        context['version'] = param_version_dte.objects.get(codigo='1002')
        pos_decimales = param_version_dte.objects.get(codigo="1004")
        context['decimal'] = int(pos_decimales.tipoDato)
        context['img'] = self.get_image_url()
        return context

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
        """
        # This is a dummy implementation, you may need to customize it based on your needs
        return uri

class MyJsonViewMixin:
    def generate_json(self, factura_obj):
        emisor = factura_obj.fk_emisor
        receptor = factura_obj.fk_receptor
        tipoMoneda = param_version_dte.objects.get(codigo='1003')

        identificacion_json={
            'version': int(factura_obj.fk_Identificacion.version),
            'ambiente': str(factura_obj.fk_Identificacion.ambiente.codigo),
            'tipoDte': str(factura_obj.fk_Identificacion.tipoDte.codigo),
            'numeroControl': str(factura_obj.fk_Identificacion.numeroControl),
            'codigoGeneracion': str(factura_obj.fk_Identificacion.codigoGeneracion),
            'tipoModelo': int(factura_obj.fk_Identificacion.tipoOperacion.codigo) if int(factura_obj.fk_Identificacion.tipoOperacion.codigo) == 1 else int(factura_obj.fk_Identificacion.tipoModelo.codigo),
            'tipoOperacion': int(factura_obj.fk_Identificacion.tipoOperacion.codigo),
            'tipoContingencia': None,
            'motivoContin': None,
            'fecEmi': str(factura_obj.fecha.strftime('%Y-%m-%d')),
            'horEmi': str(factura_obj.date_creation.strftime('%H:%M:%S')),
            'tipoMoneda': tipoMoneda.tipoDato
        }

        documento_rel= None

        info_direccion_emisor = {
            'departamento': factura_obj.fk_puntoVenta.establecimiento_fk.direccionMun.departamento.codigo,
            'municipio': factura_obj.fk_puntoVenta.establecimiento_fk.direccionMun.codigo,
            'complemento': factura_obj.fk_puntoVenta.establecimiento_fk.complementodir
        }
        
        emisor_json = {
            'nit': str(utils.quitar_guiones(emisor.nit)),
            'nrc': str(utils.quitar_guiones(emisor.nrc)),
            'nombre': str(emisor.nombre),
            'codActividad': str(emisor.actividadeco.codigo),
            'descActividad': emisor.actividadeco.descripcion,
            'nombreComercial': emisor.nombrecomercial if emisor.nombrecomercial else None,
            'tipoEstablecimiento': str(factura_obj.fk_puntoVenta.establecimiento_fk.tipoEstable.codigo),
            'direccion': info_direccion_emisor,
            'telefono': str(factura_obj.fk_puntoVenta.establecimiento_fk.telefono),
            'correo': str(emisor.email),
            'codEstableMH': factura_obj.fk_puntoVenta.establecimiento_fk.codestablemh,
            'codEstable': factura_obj.fk_puntoVenta.establecimiento_fk.codestablec,
            'codPuntoVentaMH': factura_obj.fk_puntoVenta.codpuntoventamh,
            'codPuntoVenta': factura_obj.fk_puntoVenta.codpuntoventa
        }

        if receptor.municipio :
            info_direccion_receptor = {
                'departamento': receptor.municipio.departamento.codigo,
                'municipio': receptor.municipio.codigo,
                'complemento': receptor.complementodir if receptor.complementodir else None
            }
        else :
            info_direccion_receptor=None

        receptor_json = {
            'nombre': receptor.nombre,
            'codActividad': receptor.actividadeco.codigo if receptor.actividadeco else None,
            'descActividad': receptor.actividadeco.descripcion if receptor.actividadeco else None,
            'direccion': info_direccion_receptor,
            'telefono': receptor.telefono if receptor.telefono else None,
            'correo': receptor.email
        }

        if factura_obj.fk_Identificacion.tipoDte.codigo == '01':
            receptor_json['nrc'] = None
            receptor_json['tipoDocumento'] = str(receptor.tipodocumento.codigo) if receptor.tipodocumento else None
            receptor_json['numDocumento'] = str(receptor.nodocumento) if receptor.tipodocumento.codigo == '36' or receptor.tipodocumento.codigo == '13' else None
        if factura_obj.fk_Identificacion.tipoDte.codigo == '03':
            receptor_json['nrc'] = utils.quitar_guiones(receptor.nrc) if receptor.tipodocumento else None
            receptor_json['nit'] = str(utils.quitar_guiones(receptor.nodocumento))
            receptor_json['nombreComercial'] = str(receptor.nombreComercial) if receptor.nombreComercial else None

        otrosDocumentos = None
        
        ventaTercer = None
        
        detalles = []
        index = 1
        detalles_queryset = DetalleFactura.objects.filter(fk_factura=factura_obj)
        codtributos_factura = ["A8", "57", "90", "D4", "D5", "25", "A6"]
        codtributos_credito_fiscal = ["A8", "57", "90", "D4", "D5", "25", "A6"]
        for detalle in detalles_queryset:
            detalle_dict = {
                'numItem': int(index),
                'tipoItem': int(detalle.fk_Producto.tipoitem.codigo),
                'numeroDocumento': None,
                'cantidad': int(detalle.cantidad),
                'codigo': detalle.fk_Producto.codigo,
                'uniMedida': int(detalle.fk_Producto.unimedida.codigo),
                'descripcion': str(detalle.fk_Producto.descripcion),
                'precioUni': float(detalle.fk_Producto.preciouni),                
                'montoDescu': float(detalle.montoDescu),
                'ventaNoSuj': float(0.00),
                'ventaExenta': float(detalle.total) if detalle.fk_Producto.exentoIva == 'S' else float(0.00),
                'ventaGravada': float(detalle.total) if detalle.fk_Producto.exentoIva == 'N' else float(0.00),
                'tributos': [detalle.fk_Producto.tributo.codigo] if factura_obj.fk_Identificacion.tipoDte.codigo == '03' else None,
                'psv': float(0),
                'noGravado': float(0.00),
            }
            if factura_obj.fk_Identificacion.tipoDte.codigo == '01':
                tributos_producto = tributo.objects.filter(productos__detallefactura__fk_Producto=detalle.fk_Producto, codigo__in=codtributos_factura).distinct()
                detalle_dict['ivaItem'] = float(0)
                detalle_dict['codTributo'] = tributos_producto.codigo if tributos_producto else None
            if factura_obj.fk_Identificacion.tipoDte.codigo == '03':
                tributos_producto = tributo.objects.filter(productos__detallefactura__fk_Producto=detalle.fk_Producto, codigo__in=codtributos_credito_fiscal).distinct()
                detalle_dict['codTributo'] = tributos_producto.codigo if tributos_producto else None
            

            detalles.append(detalle_dict)
            index+=1
        
        pagos = []
        pagos_queryset = pagosfactura.objects.filter(fk_Factura = factura_obj)
        for pago in pagos_queryset:
            pagos_dict={
                'codigo': str(pago.codigo.codigo),
                'montoPago': float(pago.montopago),
                'referencia': None,
                'plazo': None,
                'periodo': None
            }
            pagos.append(pagos_dict)
        
        tributos = []
        if factura_obj.fk_Identificacion.tipoDte.codigo == '01':
            codigos = ["C3", "59", "71", "C8", "D1", "C5", "C6", "C7", "D5", "19", "28", "31", "32", "33", "34", "35", "36", 
                    "37", "38", "39", "42", "43", "44", "50", "51", "52", "53", "54", "55", "58", "77", "78", "79", "85", "86", 
                    "91", "92", "A1", "A5", "A7", "A9"]
            tributos_queryset = tributo.objects.filter(productos__detallefactura__fk_factura=factura_obj, codigo__in=codigos).distinct()
        if factura_obj.fk_Identificacion.tipoDte.codigo == '03':
            tributos_queryset = tributo.objects.filter(productos__detallefactura__fk_factura=factura_obj).distinct()

        for trib in tributos_queryset:
            tributo_dict = {
                'codigo': str(trib.codigo),
                'descripcion': str(trib.descripcion),
                'valor': float(trib.valor )
            }
            tributos.append(tributo_dict)
        
        resumen_json = {
            'totalNoSuj': float(0.00),
            'totalExenta': float(factura_obj.totalExento),
            'totalGravada': float(factura_obj.totalnoExento),
            'subTotalVentas': float(factura_obj.totalOperaciones),
            'descuNoSuj': float(0.00),
            'descuExenta': float(factura_obj.descuExenta),
            'descuGravada': float(factura_obj.descuGravada),
            'porcentajeDescuento': float(0),
            'totalDescu': float(factura_obj.descuTotal),
            'tributos': tributos,
            'subTotal': float(factura_obj.subtotalSinImpuestos),
            'ivaRete1': float(factura_obj.ivaRete),
            'reteRenta': float(factura_obj.reteRenta),
            'montoTotalOperacion': float(factura_obj.totalOperaciones),
            'totalNoGravado': float(0.00),
            'totalPagar': float(factura_obj.totalPagar),
            'totalLetras': str(utils.numero_a_letras(factura_obj.totalPagar)),
            'saldoFavor': float(0),
            'condicionOperacion': int(1),
            'pagos': pagos,
            'numPagoElectronico': None,
        }

        if factura_obj.fk_Identificacion.tipoDte.codigo == '01':
            resumen_json['totalIva'] = float(factura_obj.totalIva)
        if factura_obj.fk_Identificacion.tipoDte.codigo == '03':
            resumen_json['ivaPerci1'] = float(0)
        
        extension=None
        apendice=None

        factu_json = {
            'identificacion': identificacion_json,
            'documentoRelacionado': documento_rel,
            'emisor': emisor_json,
            'receptor': receptor_json,
            'otrosDocumentos':otrosDocumentos,
            'ventaTercero':ventaTercer,
            'cuerpoDocumento': detalles,
            'resumen':resumen_json,
            'extension': extension,
            'apendice': apendice
            
        }

        return factu_json
        

class MyPDFView(View, MyPDFViewMixin):

    def get(self, request, *args, **kwargs):
        factura = get_object_or_404(Factura, id=self.kwargs.get('pk'))
        context = self.get_context_data()
        template_path = self.template_path
        pdf_content = self.generate_pdf_content(context)
        # Crear un objeto de respuesta Django y especificar content_type como pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="report.pdf"'
        # Encontrar la plantilla y renderizarla.
        template = get_template(template_path)
        html = template.render(context)

        # Crear un PDF
        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=self.link_callback)
        # Si hay un error, muestra una vista de error
        if pisa_status.err:
            return HttpResponse('Hubo algunos errores <pre>' + html + '</pre>')
        return response
    def get_template(self,factura, request, *args, **kwargs):
        if(factura.fk_Identificacion.tipoDte.codigo == '01'):
            return 'wsfacturae'
        

class DownloadPDF(View, MyPDFViewMixin):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        pdf_content = self.generate_pdf_content(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        response['Content-Type'] = 'application/pdf'
        response.content = pdf_content

        redirect_url = reverse('wsfacturae:DteList')  #     Cambia 'tipo_dte_value' por el valor adecuado
        response['X-Success-Redirect'] = redirect_url  # Agrega una cabecera personalizada
        return response

class SendPdfMail(LoginRequiredMixin, SuccessMessageMixin, View, MyPDFViewMixin):

    def get(self, request, *args, **kwargs):
        try:
            smtp_config = SMTP.objects.first()
        except SMTP.DoesNotExist:
            smtp_config = None
        pdf_view = MyPDFViewMixin()
        factura = get_object_or_404(Factura, id=self.kwargs.get('pk'))
        json = get_object_or_404(JsonFac, fk_factura = factura)
        json_data = json.json
        pdf_content = pdf_view.generate_pdf_content(self.get_context_data())
        subject = 'PDF con código QR'
        to_email = factura.fk_receptor.email
        from_email = smtp_config.username
        msg = utils.prepareMail(subject, to_email, from_email, pdf_content, json_data, smtp_config)
        msg.send()

        messages.success(request, "El email ha sido enviado satisfactoriamente.")
        my_render = reverse_lazy('wsfacturae:DteDetail', kwargs={'pk': factura.pk})
        return redirect(my_render)

#Vista del Json
class JsonView(View, MyJsonViewMixin):
    template_name = 'wsfacturae/json_view.html'
    
    def get(self, request, *args, **kwargs):
        api_url = 'http://localhost:8113/firmardocumento/'
        json_unformatted = self.generate_json(Factura.objects.get(id=self.kwargs.get('pk')))
        json_file = json.dumps(json_unformatted, indent=4)
  #      headers = {
 #           'Content-Type': 'application/json',
 #           'nit': '34234234234234',
 #           'activo': 'True',
 #           'passwordPri': '123456',
 #       }
 #       
        # Envía el JSON en el cuerpo de la solicitud en lugar de configurarlo como un encabezado
   #     data = {
   #         'dteJson': json_file,
   #     }

   #     response = requests.post(api_url, json=data, headers=headers)

   #     if response.status_code == 200:
            # Si la solicitud fue exitosa (código de estado 200), la respuesta debe contener el JSON firmado
   #         json_firmado = response.json()
            
            # Puedes procesar el JSON firmado según tus necesidades aquí
            # ...

            # Finalmente, puedes devolver la respuesta JSON firmada como parte de la respuesta de tu vista
   #         return JsonResponse(json_firmado)
   #     else:
            # Si la solicitud no fue exitosa, maneja el error de acuerdo a tus requerimientos
    #        return HttpResponse('Error al enviar la solicitud a la API externa', status=response.status_code)
        return render(request, self.template_name, {'json_file': json_file})
    
class SendSMS(DetailView,LoginRequiredMixin, SuccessMessageMixin):
    parrafo_sms = "Adjunto dirección para visualizar el json: {{json}} y el pdf: {{pdf}}."
    def get(self, request, pk, *args, **kwargs):
        parrafo = self.parrafo_sms
        factura = get_object_or_404(Factura, id=pk)
        to_tel = '+503'+str(factura.fk_receptor.celular)
        base_url = request.scheme + "://" + request.get_host()
        parrafo = parrafo.replace('{{json}}', base_url +'/jsonView/' + str(pk))
        parrafo = parrafo.replace('{{pdf}}', base_url +'/pdfView/'  +str(pk))
        utils.prepareSMS(to_tel, parrafo)
        print(to_tel)
        messages.success(request, "El SMS ha sido enviado satisfactoriamente.")
        my_render = reverse_lazy('wsfacturae:DteList')
        
        return redirect(my_render)


class DteFormView(FormView, SuccessMessageMixin,LoginRequiredMixin, MyPDFViewMixin, MyJsonViewMixin):
    template_name = 'wsfacturae/dteform.html'
    form_class = InsertarDteForm
    second_form_class = AgregarProductoForm
    third_form_class = AgregarMetodoPagoForm
    success_url = reverse_lazy('wsfacturae:dteFormView')
    success = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pos_decimales = param_version_dte.objects.get(codigo="1004")
        tipo_dte = self.kwargs.get('tipo_dte')
        context['decimal'] = int(pos_decimales.tipoDato)
        context['form'] = self.form_class()
        context['form_producto'] = self.second_form_class()
        context['form_metodo'] = self.third_form_class()
        context['productos'] = Productos.objects.order_by('descripcion')
        context['establecimientos'] = Establecimiento.objects.order_by('id')
        # Agregar el carrito de productos a la sesión si no existe
        if 'carrito' not in self.request.session:
            self.request.session['carrito'] = []
        if 'receptor' not in self.request.session:
            self.request.session['receptor'] = None
        if 'fecha' not in self.request.session:
            self.request.session['fecha'] = None
        if 'establecimiento' not in self.request.session:
            self.request.session['establecimiento'] = None
        if 'puntoventa' not in self.request.session:
            self.request.session['puntoventa'] = None
        if 'subtotal' not in self.request.session:
            self.request.session['subtotal'] = 0
        if 'subtotalSinImpuesto' not in self.request.session:
            self.request.session['subtotalSinImpuesto'] = 0
        if 'ivaRete' not in self.request.session:
            self.request.session['ivaRete'] = 0
        if 'totalPagado' not in self.request.session:
            self.request.session['totalPagado'] = 0
        if 'pagos' not in self.request.session:
            self.request.session['pagos']=[]
        
        context['carrito_error'] = self.request.session.pop('carrito_error', None)
        context['carrito'] = self.request.session.get('carrito', [])
        context['pagos'] = self.request.session.get('pagos',[])
        context['receptor'] = self.request.session.get('receptor', None)
        context['fecha'] = self.request.session.get('fecha', None)
        context['establecimiento'] = self.request.session.get('establecimiento', None)
        context['puntoventa'] = self.request.session.get('puntoventa', None)
        context['totalPagado'] = self.request.session.get('totalPagado', 0)
        
        # Inicializar el formulario de InsertarDteForm con el valor del receptor
        initial_data = {}
        if context['receptor'] is not None:
            initial_data['receptor'] = context['receptor'].get('id', '')
        if context['fecha'] is not None:
            initial_data['fecha'] = context['fecha'].get('fecha', '')
        if context['establecimiento'] is not None:
            initial_data['establecimiento'] = context['establecimiento'].get('codigo', '')
        if context['establecimiento'] is not None:
            initial_data['puntoventa'] = context['puntoventa'].get('codigo', '')
        

        context['form'] = InsertarDteForm(initial=initial_data)


        # Calcular el total del subtotal
        total_exento = 0
        total_Noexento = 0
        total_descuExento = 0
        total_descuNoExento = 0
        total_Noexento_descuento = 0
        total_exento_descuento = 0
        iva_Retenido = 0 
        rete_Renta = 0
        impuestos = 0
        total_exento_sin_impuesto = 0
        total_noexento_sin_impuesto = 0
        subtotal_descuExento = 0
        
        for item in context['carrito']:
            subtotal = float(item['subtotal'])
            descuento = float(item['descuTotal'])
            subtotalDescu = float(item['totalDescu'])
            totalSinImpuesto = float(item['subtotalSinImpuesto'])
            if item['excento'] == 'S':
                total_descuExento = round_numbers(total_descuExento+descuento)
                if tipo_dte =='01':
                    total_exento = round_numbers(total_exento+subtotal)
                    total_exento_descuento =round_numbers(total_exento_descuento+subtotalDescu)
                    total_exento_sin_impuesto = round_numbers(total_exento_sin_impuesto + totalSinImpuesto)
                    
                elif tipo_dte =='03':
                    total_exento = round_numbers(total_exento + totalSinImpuesto)
                    total_exento_descuento =round_numbers(total_exento_descuento+totalSinImpuesto-descuento)
                    
            else:
                total_descuNoExento=round_numbers(total_descuNoExento+descuento)
                if item['tipo']=='2':
                    rete_Renta = (rete_Renta + float(item['subtotalSinImpuesto']))*0.10
                if tipo_dte =='01':
                    total_Noexento=round_numbers(total_Noexento + subtotal)
                    total_Noexento_descuento =round_numbers(total_Noexento_descuento+subtotalDescu)  
                    total_noexento_sin_impuesto = round_numbers(total_noexento_sin_impuesto + totalSinImpuesto)
                elif tipo_dte =='03':
                    total_Noexento = round_numbers(total_Noexento+totalSinImpuesto)
                    total_Noexento_descuento =round_numbers(total_Noexento_descuento+totalSinImpuesto-descuento)
                    #Calcular impuestos
            impuestos = impuestos +((totalSinImpuesto-descuento)*0.13)        
            subtotal_descuExento = round_numbers(subtotal_descuExento + subtotalDescu)
        
        context['exento'] = total_exento
        context['impuestos'] = impuestos
        context['noexento'] = total_Noexento
        context['totalDescuExento'] = total_exento_descuento
        context['totalDescuNoExento'] = total_Noexento_descuento
        
        if tipo_dte == "01":
            context['subtotal'] = self.request.session['subtotal']
        elif tipo_dte == "03":
            context['subtotal'] = self.request.session['subtotalSinImpuesto']


        # Buscar los descuentos que no están asocidados a productos, es decir que apliquen al subtotal de la factura
        descuentos_dte = Descuento.objects.filter(producto=None)
        descuentos_exentos = 0
        descuentos_noexentos = 0
        total_descuento_dte = 0

        # Cantidad de productos en el carrito
        cantidad_productos_exentos = 0
        cantidad_productos_gravados = 0
        total_productos_exentos = 0
        total_productos_gravados = 0
        subtotal_sin_descuento = 0
        
        # Contar cuantos items hay en el carrito
        for item in context["carrito"]:
            if tipo_dte == "01":
                subtotal_sin_descuento += float(item["subtotal"])
            if item["excento"] == "S":
                cantidad_productos_exentos += item["cantidad"]
                total_productos_exentos += float(item["totalDescu"])
            elif item["excento"] == "N":
                cantidad_productos_gravados += item["cantidad"]
                total_productos_gravados += float(item["subtotalSinImpuesto"])
                
        
        #Subtotal sin descuentos
        context["subtotalSinDescuento"] = subtotal_sin_descuento
        context["IVA"] = 0

        # Calcular el descuento
        for item in descuentos_dte:
            if (
                (item.fecha_inicio is None and item.fecha_fin is None)
                or (item.fecha_inicio is not None and item.fecha_fin is not None and item.fecha_fin >= datetime.now().date())
                or (item.fecha_inicio is not None and item.fecha_fin is None)
            ):
                if item.tipo_producto == "S":
                    if cantidad_productos_exentos >= item.cantidad:
                        cantidad_aplicacion = (cantidad_productos_exentos // float(item.cantidad))
                        if item.tipo_descuento == "MONTO_ITEM":
                            descuentos_exentos += round_numbers(float(cantidad_aplicacion) * float(item.valor_descuento))
                        elif item.tipo_descuento == "PORCENTUAL_ITEM":
                            descuentos_exentos += round_numbers(float(item.valor_descuento / 100) * total_productos_exentos)
                    elif total_productos_exentos >= item.cantidad:
                        cantidad_aplicacion = (total_productos_exentos // float(item.cantidad))
                        if item.tipo_descuento == "MONTO_FACTURA":
                            descuentos_exentos += round_numbers(cantidad_aplicacion * float(item.valor_descuento))
                        elif item.tipo_descuento == "PORCENTUAL_FACTURA":
                            descuentos_exentos = round_numbers(float(item.valor_descuento / 100) * total_productos_exentos)
                elif item.tipo_producto == "N":
                    if cantidad_productos_gravados >= item.cantidad:
                        cantidad_aplicacion = (cantidad_productos_gravados // float(item.cantidad))
                        if item.tipo_descuento == "MONTO_ITEM":
                            descuentos_noexentos += round_numbers(float(cantidad_aplicacion) * float(item.valor_descuento))
                        elif item.tipo_descuento == "PORCENTUAL_ITEM":
                            descuentos_noexentos += round_numbers(float(item.valor_descuento / 100) * total_productos_gravados)
                    elif total_productos_gravados >= item.cantidad:
                        cantidad_aplicacion = (total_productos_gravados // float(item.cantidad))
                        if item.tipo_descuento == "MONTO_FACTURA":
                            descuentos_noexentos += round_numbers(cantidad_aplicacion * float(item.valor_descuento))
                        elif item.tipo_descuento == "PORCENTUAL_FACTURA":
                            descuentos_noexentos += round_numbers(float(item.valor_descuento / 100) * total_productos_gravados)
            
        context['descuentos_exentos_dte'] = descuentos_exentos
        context['descuentos_gravados_dte'] = descuentos_noexentos
        
        if tipo_dte == "01":
            context['descuentos_gravados_dte'] += context['descuentos_gravados_dte'] * 0.13
        
        total_descuento_dte = context['descuentos_exentos_dte'] + context['descuentos_gravados_dte']

        if total_descuento_dte >= context["subtotal"]:
            context["total_descuento_dte"] = context["subtotal"]
        else:
            context["total_descuento_dte"] = total_descuento_dte
        
        if tipo_dte =='01':
            context['total_sin_impuesto'] = total_noexento_sin_impuesto + total_exento_sin_impuesto
        elif tipo_dte =='03':
            context['total_sin_impuesto'] = total_exento_descuento + total_Noexento_descuento
            context["IVA"] = float(total_productos_gravados - descuentos_noexentos) * 0.13
        
        if total_productos_gravados >= 100 and self.request.session['receptor'] is not None and self.request.session['receptor_es_gran_contr'] == 'S':
            iva_Retenido = round_numbers(total_productos_gravados * 0.01)
        
        context['descuExento'] = total_descuExento
        context['descuNoExento'] = total_descuNoExento
        context['ivaRete'] = iva_Retenido
        context['reteRenta']=rete_Renta
        context['descuTotal'] = round_numbers(total_descuExento + total_descuNoExento)
                
        if tipo_dte =='01':
            context['subtotalconDescu'] = subtotal_descuExento
        elif tipo_dte =='03':
            context['subtotalconDescu'] = total_Noexento_descuento + total_exento_descuento
        
        context["totalAPagar"] = (context["subtotal"] - context["total_descuento_dte"]) + context["IVA"] - context["ivaRete"] - context['reteRenta']

        context['dte_object'] = get_object_or_404(detallemastercat, mastercat_id=2, codigo=self.kwargs.get('tipo_dte'))
        context['tipo_dte'] = self.kwargs.get('tipo_dte')
        
        return context

    def form_valid(self, form):
        tipo_dte = self.kwargs['tipo_dte']
        dte_object = get_object_or_404(detallemastercat, mastercat_id=2, codigo=self.kwargs.get('tipo_dte'))
        success_url = reverse_lazy('wsfacturae:dteFormView', kwargs={'tipo_dte': tipo_dte}) 
        if 'producto_add' in self.request.POST:
            try:
                carrito = self.request.session['carrito']
                #Buscar cada producto cuando se añade el producto
                producto = Productos.objects.get(descripcion=self.request.POST.get('producto', ''))

                for item in carrito:
                    if item['producto'] == producto.descripcion:
                        self.request.session['carrito_error'] = 'El producto ya está en el carrito.'
                        return redirect('wsfacturae:dteFormView', tipo_dte)
                
                cantidad = int(self.request.POST.get('cantidad', 0))
                # Buscar los descuentos que tengan asociado un producto
                descuentos_item = Descuento.objects.filter(producto=producto)
                total_descuento_item = 0
                
                for descuento in descuentos_item:
                    if (
                        cantidad >= descuento.cantidad
                        and (
                            (descuento.fecha_inicio is None and descuento.fecha_fin is None)
                            or (descuento.fecha_inicio is not None and descuento.fecha_fin is not None and descuento.fecha_fin >= datetime.now().date())
                            or (descuento.fecha_inicio is not None and descuento.fecha_fin is None)
                            )
                        ):
                        cantidad_aplicacion = (cantidad // descuento.cantidad)
                        if descuento.tipo_descuento == "MONTO_ITEM" and descuento.cantidad != 0:
                            total_descuento_item += round_numbers(cantidad_aplicacion * descuento.valor_descuento)
                        elif descuento.tipo_descuento == "PORCENTUAL_ITEM" and descuento.cantidad != 0:
                            monto_descuento = round_numbers((descuento.valor_descuento / 100) * producto.preciouni)
                            total_descuento_item += round_numbers(cantidad_aplicacion * monto_descuento)

                if float(total_descuento_item) >= (float(producto.preciouni) * float(cantidad)):
                    descuento = producto.preciouni
                else:
                    descuento = total_descuento_item

                
                descuento_con_impuesto = total_descuento_item
                descuento_con_impuesto += descuento * (producto.tributo.valor / 100)

                if producto.exentoIva =='N':
                    #Precio unitario con descuento y el tributo
                    precioUniDescu = float(producto.preciouni + (producto.preciouni * (producto.tributo.valor / 100))) - float(descuento_con_impuesto / cantidad)
                    #Precio unitario con tributo sin descuento
                    precioUni = producto.preciouni + (producto.preciouni * (producto.tributo.valor / 100))
                    #precio unitario sin tributo con descuento
                    precioUniSinImp = float(producto.preciouni) - float(descuento / cantidad)
                else:
                    #solo se quita el descuento porque es exento
                    precioUniDescu = float(producto.preciouni) - float(descuento / cantidad)
                    precioUni = producto.preciouni
                    precioUniSinImp = float(producto.preciouni) - float(descuento / cantidad)
                

                #Precio unitario * cantidad con descuentos y tributos si aplica
                subtotalDescu = round_numbers((precioUniDescu * cantidad))
                #Precio unitario * cantidad sin descuentos con tributo si aplica
                subtotal = round_numbers((precioUni * cantidad))
                #precio unitario sin impuesto por cantidad con descuento
                subtotalSinImpuesto = round_numbers((precioUniSinImp*cantidad))
                
                self.request.session['subtotal'] = float(self.request.session['subtotal']) + float(subtotalDescu)
                self.request.session['subtotalSinImpuesto'] = float(self.request.session['subtotalSinImpuesto']) + float(subtotalSinImpuesto)

                
                elemento = {
                    'producto': producto.descripcion,
                    'cantidad': cantidad,
                    'preciouni': str(round_numbers(precioUni)),
                    'preciouniSinImpuesto':str(round_numbers(producto.preciouni)),
                    'totalDescu':str(round_numbers(subtotalDescu)),
                    'subtotal': str(round_numbers(subtotal)),
                    'tipo':str(producto.tipoitem.codigo),
                    'descuento':str(round_numbers(descuento)),
                    'descuentoConImp':str(round_numbers(descuento_con_impuesto)),
                    'descuTotal':str(round_numbers(descuento)),
                    'subtotalSinImpuesto':str(round_numbers(subtotalSinImpuesto)),
                    'excento':producto.exentoIva,
                }
                
                carrito.append(elemento)
                self.request.session['carrito'] = carrito

            except Productos.DoesNotExist:
                # Manejar el caso cuando el producto no existe
                pass

        elif 'eliminar_producto' in self.request.POST:
            try:
                index = int(self.request.POST.get('eliminar_producto'))
                carrito = self.request.session.get('carrito', [])
                print("ESTE ES EL INDEX: " + str(index))
                if 0 <= index < len(carrito):
                    elemento = carrito[index]
                    self.request.session['subtotal'] = float(self.request.session['subtotal'])-float(elemento['totalDescu'])
                    self.request.session['subtotalSinImpuesto'] = float(self.request.session['subtotalSinImpuesto']) - float(elemento['subtotalSinImpuesto'])
                    del carrito[index]
                    self.request.session['carrito'] = carrito

                # Actualizar el contexto para reflejar el carrito actualizado
                context = self.get_context_data()
                return self.render_to_response(context)

                # Manejar el caso cuando el índice es inválido
            except (ValueError, IndexError):
                pass  # Manejar el caso en que no se puede convertir a entero o el índice es inválido
        elif 'eliminar_pago' in self.request.POST:
            try:
                index = int(self.request.POST.get('eliminar_pago'))
                pagos = self.request.session.get('pagos', [])
                totalPagado = 0
                print("ESTE ES EL INDEX: " + str(index))
                if 0 <= index < len(pagos):
                        # Eliminar el pago del carrito
                    del pagos[index]
                    self.request.session['pagos'] = pagos
                print(self.request.session['pagos'])
                if pagos:
                    for item in pagos:
                        totalPagado +=float(item['monto'])
                        print(totalPagado)
                else:
                    totalPagado = 0
                self.request.session['totalPagado'] = totalPagado
                print(self.request.session['pagos'])
                print(totalPagado)
                print(self.request.session['totalPagado'])
                context = self.get_context_data()
                return self.render_to_response(context)
            except (ValueError, IndexError):
                pass

        # Manejar el formulario principal (InsertarDteForm) si se envía
        elif 'save_form' in self.request.POST:
            # Validar el formulario principal y guardar los datos del receptor en la sesión
            if form.is_valid():
                receptor_data = {
                    'id': self.request.POST.get('receptor', ''),
                }
                fecha_data = {
                    'fecha':self.request.POST.get('fecha','')
                }
                establecimiento_data = {
                    'codigo':self.request.POST.get('establecimiento','')
                }
                puntoventa_data = {
                    'codigo':self.request.POST.get('puntoventa','')
                }
                
                self.request.session.pop('receptor', None)
                self.request.session.pop('fecha', None)
                self.request.session.pop('establecimiento',None)
                self.request.session.pop('puntoventa',None)
                
                self.request.session['receptor'] = receptor_data
                self.request.session['fecha'] = fecha_data
                self.request.session['establecimiento'] = establecimiento_data
                self.request.session['puntoventa'] = puntoventa_data
                
        elif 'enviar_form' in self.request.POST:
                carrito = self.request.session.get('carrito', [])
                pagos = self.request.session.get('pagos', [])
                emisor = get_object_or_404(EmisorN, id=1)
                context = self.get_context_data()
                try:
                    factura = Factura()
                    factura.fecha = datetime.strptime(self.request.POST.get('fecha', ''), '%Y-%m-%d')
                    factura.fk_receptor = ReceptorN.objects.get(id=self.request.POST.get('receptor', ''))
                    factura.fk_puntoVenta = PuntoVenta.objects.get(establecimiento_fk=Establecimiento.objects.get(codestablec=self.request.POST.get('establecimiento')),codpuntoventa=self.request.POST.get('puntoventa',''))
                    factura.codigoFactura = utils.generate_random_code()
                    factura.totalExento = context['totalDescuExento']
                    factura.totalnoExento = context['totalDescuNoExento']
                    factura.totalOperaciones = round_numbers(context['totalAPagar'])
                    factura.ivaRete = context["ivaRete"]
                    factura.reteRenta = context['reteRenta']
                    factura.descuExenta = context['descuentos_exentos_dte']
                    factura.descuGravada = context['descuentos_gravados_dte']
                    factura.impuesTotal = context['impuestos']
                    factura.totalPagar = context['totalAPagar']
                    factura.descuTotal = context['descuExento']+context['descuNoExento']+context['total_descuento_dte']
                    if dte_object.codigo =='01':
                        factura.subtotalconDescu = context['subtotalconDescu']
                        factura.subtotal = factura.subtotalconDescu- context['ivaRete'] - context['reteRenta']
                    if dte_object.codigo =='03':
                        factura.subtotalconDescu = context['subtotalconDescu']+context['impuestos']
                        factura.subtotal = factura.subtotalconDescu- context['ivaRete'] -context['reteRenta']
                    
                    factura.subtotalSinImpuestos = float(context['total_sin_impuesto'])
                    factura.fk_emisor = emisor
                    factura.totalIva = round_numbers(context['totalDescuNoExento'] * 0.13)
                    identificacion = Identificacion()
                    identificacion.tipoDte = dte_object
                    if dte_object.codigo == '01':
                        identificacion.version = int(1)
                    if dte_object.codigo == '01':
                        identificacion.version = int(1)
                    if dte_object.codigo == '03':
                        identificacion.version = int(3)
                    identificacion.ambiente = get_object_or_404(detallemastercat, id=11)
                    identificacion.tipoModelo = get_object_or_404(detallemastercat, id=23)
                    identificacion.tipoOperacion = get_object_or_404(detallemastercat, id=25)
                    try:
                        numero_de_registros = Identificacion.objects.last().id 
                    except Exception as event:
                        numero_de_registros = 1
                    numero_formateado = f'{numero_de_registros:015}'
                    identificacion.numeroControl = 'DTE-'+context['tipo_dte']+'-'+ factura.fk_puntoVenta.establecimiento_fk.codestablec+factura.fk_puntoVenta.codpuntoventa+'-'+numero_formateado
                    identificacion.codigoGeneracion = utils.generate_uuidv4()
                    identificacion.save()
                    factura.fk_Identificacion =identificacion
                    factura.save()
                    for item in carrito:
                        detalle = DetalleFactura()
                        detalle.fk_factura = factura
                        producto_nombre = item['producto']
                        producto_obj = Productos.objects.get(descripcion=producto_nombre)
                        detalle.fk_Producto = producto_obj
                        detalle.cantidad = int(item['cantidad'])
                        detalle.montoDescu = float(item['descuento'])
                        if dte_object.codigo == '01':
                            detalle.precioUnitario = float(item['preciouni'])
                            detalle.total = round_numbers(float(item['totalDescu']))
                        elif dte_object.codigo =='03' :
                            detalle.precioUnitario = float((item['preciouniSinImpuesto']))
                            detalle.total = round_numbers(float(item['subtotalSinImpuesto'])-float(item['descuTotal']))
                        detalle.save()
                    for item in pagos:
                        detallePago = pagosfactura()
                        detallePago.montopago = item['monto']
                        detallePago.codigo = get_object_or_404(detallemastercat, id=item['id'])
                        detallePago.fk_Factura = factura
                        detallePago.save()
                    factu_json = json.dumps(self.generate_json(factura))
                    
                    jsonFac = JsonFac()
                    jsonFac.fk_factura = factura
                    jsonFac.json = factu_json
                    jsonFac.save()
                    
                    self.request.session['carrito'] = []
                    self.request.session['fecha'] = None
                    self.request.session['receptor'] = None
                    self.request.session['puntoventa'] = None
                    self.request.session['establecimiento'] = None
                    self.request.session['subtotal'] = 0
                    self.request.session['pagos'] = []
                    self.request.session['totalPagado']=0
                    self.request.session['subtotalSinImpuesto'] = 0
                    self.success = True
                    
                    # Envio del DTE al backend
                    api_url = 'http://localhost:8080/api/hacienda/'
                    hacienda_user = Hacienda.objects.last() #Encontrar el último registro

                    data = {
                        'user': hacienda_user.user,
                        'pwd': hacienda_user.pwd,
                        'token': hacienda_user.token,
                        'tipo_dte': str(identificacion.tipoDte.codigo),
                        'codigo_generacion': str(identificacion.codigoGeneracion),
                        'ambiente': str(identificacion.ambiente.codigo),
                        'version': int(identificacion.version),
                        'nitemisor': str(utils.quitar_guiones(factura.fk_emisor.nit)),
                        "json_data": json.loads(jsonFac.json)
                    }
                    print("ESTE ES EL TIPO DE DATO DEL JSON QUE SE ENVIA",type(data["json_data"]))
                    headers = {
                         "Content-Type": "application/json"
                    }
                    #print(data)
                    try:
                        
                        response = requests.post(api_url, json=data, headers=headers)
                        print("Este es el contenido de la respuesta: ",response.content)
                        if response.status_code == 200:
                            json_response = response.json()

                            # Crear nuevo registro en tabla hacienda si el token de la respuesta es distinto al actual
                            if hacienda_user.token != json_response.get("token"):
                                new_hacienda_obj = Hacienda(
                                    token = json_response["token"],
                                    user = hacienda_user.user,
                                    pwd = hacienda_user.pwd
                                )
                                new_hacienda_obj.save()
                            
                            factura.sello_hacienda = json_response.get("selloRecibido")
                            factura.hacienda_response = json_response
                            
                            fecha_procesamiento = json_response.get("fhProcesamiento")
                            if fecha_procesamiento:
                                factura.hacienda_fecha_procesamiento = datetime.strptime(fecha_procesamiento, '%d/%m/%Y %H:%M:%S')
                            factura.hacienda_codigo_mansaje = json_response.get("codigoMsg")
                            
                            estado_obj = None
                            if json_response.get("codigoMsg") == '001':
                                estado_obj = Estado.objects.get(codigo_estado='DONE')
                            if json_response.get('codigoMsg') == '002':
                                estado_obj = Estado.objects.get(codigo_estado='RECOB')
                            if json_response.get('codigoMsg') == '003':
                                estado_obj = Estado.objects.get(codigo_estado='CANE')
                            
                            factura.estado_dte = estado_obj

                            factura.save()
                            
                            # Enviar correo y la vista que redirija a detalle de DTE
                            redirect_url = reverse('wsfacturae:pdfList', kwargs={'pk': factura.pk})
                            return HttpResponseRedirect(redirect_url)
                        else:
                            return JsonResponse({"error": "La solicitud falló"}, status=response.status_code)
                    except requests.exceptions.RequestException as e:
                        return JsonResponse({"error": f"Error de solicitud: {str(e)}"}, status=500)
                    
                    return HttpResponseRedirect(redirect_url)
                except Exception as e:
                    print(e)
                    traceback.print_exc()

        # Redireccionar a la URL de éxito
        return HttpResponseRedirect(success_url)
    
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        totalAPagar = context["subtotal"]
        ivaRete = 0
        if self.request.is_ajax():
            if 'receptor' in self.request.POST:
                receptor = self.request.POST.get('receptor')
                receptor_object = get_object_or_404(ReceptorN, id=receptor)
                dte_object = get_object_or_404(detallemastercat, mastercat_id=2, codigo=self.kwargs.get('tipo_dte'))
                response_data = {}  # Inicializa el diccionario
                self.request.session['receptor_es_gran_contr'] = self.request.POST.get('esGranContr', '')

                return JsonResponse(response_data)
            if 'metodoPago' in self.request.POST:
                metodo_pago = get_object_or_404(detallemastercat, mastercat_id=14, id=self.request.POST.get('metodoPago'))
                monto = self.request.POST.get('monto')

                # Obtén la lista actual de pagos de la sesión o crea una lista vacía si aún no existe
                resumen_pagos = self.request.session.get('pagos', [])
                elemento = {
                    'id':self.request.POST.get('metodoPago'),
                    'metodo': metodo_pago.descripcion,
                    'monto': monto,
                }

                # Agrega el nuevo elemento a la lista
                resumen_pagos.append(elemento)

                # Actualiza la lista en la sesión
                self.request.session['pagos'] = resumen_pagos

                response_data = {}
                response_data['pagos'] = self.request.session['pagos']
                self.request.session['totalPagado']+=float(monto)

                return JsonResponse(response_data)
        return self.form_valid(self.get_form())

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            datos_pagos = request.session.get('pagos',[])
            if 'establecimiento_cod' in self.request.GET:
                establecimiento_cod = self.request.GET['establecimiento_cod']
                puntos_venta = PuntoVenta.objects.filter(establecimiento_fk__codestablec=establecimiento_cod)
                puntos_venta_data = []
                for punto_venta in puntos_venta:
                    punto_venta_info = {
                        "id": punto_venta.id,
                        "codpuntoventa": punto_venta.codpuntoventa,
                        "codpuntoventamh": punto_venta.codpuntoventamh,
                    }
                    puntos_venta_data.append(punto_venta_info)
                return JsonResponse(puntos_venta_data, safe=False)
            response_data = {'pagos':datos_pagos}
            return JsonResponse(response_data)
        context = self.get_context_data()
        # Renderizar la plantilla con el contexto
        return self.render_to_response(context)
    
class ProductoListView(LoginRequiredMixin, ListView):
    template_name = "wsfacturae/producto_list.html"
    ajax_template_name='wsfacturae/producto_list_result.html'
    paginate_by = 50
    def get_queryset(self):
        qry = Productos.objects.order_by("id")
        return qry

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        return [self.template_name]

    def get_form_kwargs(self):
        return {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'data': self.request.GET or None
        }

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        #form = self.get_form(self.get_form_class())
        #if form.is_valid():
        #    self.object_list = form.filter_queryset(request, self.object_list)
        context = self.get_context_data(object_list=self.object_list)
        pos_decimales = param_version_dte.objects.get(codigo="1004")
        context['decimal'] = int(pos_decimales.tipoDato)
        return self.render_to_response(context)

    def test_func(self):
        return self.request.user.is_staff
    
class ProductoAddView(LoginRequiredMixin, CreateView):
    form_class = AddProductoForm
    template_name = 'wsfacturae/addproducto.html'
    success_url = reverse_lazy('wsfacturae:ProductoList')
    success_message = 'Información del Producto Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        return {
            'nm_estado': 1
        }

class ProductoDelete(SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Productos
    success_url = reverse_lazy('wsfacturae:ProductoList')
    form_valid_message = 'El Ítem fué eliminado satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = Productos.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El ítem ha sido eliminado satisfactoriamente.")
            my_render = reverse('wsfacturae:ProductoList')
        except IntegrityError as e:
            messages.error(request, "El ítem no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse('wsfacturae:ProductoList')
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff
    
class ProductoUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Productos
    form_class = AddProductoForm
    success_url = reverse_lazy('wsfacturae:ProductoList')
    template_name = 'wsfacturae/addproducto.html'
    
    success_message = 'Información del Producto Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

class EstablecimientoListView(LoginRequiredMixin, ListView):
    model = Establecimiento
    template_name = 'wsfacturae/establecimiento_list.html'
    ajax_template_name =''
    def get_queryset(self):
        qry = Establecimiento.objects.order_by("id")
        return qry

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        return [self.template_name]

    def get_form_kwargs(self):
        return {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'data': self.request.GET or None
        }

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)

class EstablecimientoCreateView(LoginRequiredMixin, CreateView):
    form_class = EstablecimientoAddForm
    template_name = 'wsfacturae/establecimiento_add.html'
    success_url = reverse_lazy('wsfacturae:EstablecimientoList')
    success_message = 'Información del Establecimiento Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        return {
            'nm_estado': 1
        }

class EstablecimientoDeleteView(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Establecimiento
    success_url = reverse_lazy('wsfacturae:EstablecimientoList')
    form_valid_message = 'El Ítem fué eliminado satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = Establecimiento.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El ítem ha sido eliminado satisfactoriamente.")
            my_render = reverse('wsfacturae:EstablecimientoList')
        except IntegrityError as e:
            messages.error(request, "El ítem no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse('wsfacturae:EstablecimientoList')
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff

class EstablecimientoUpdateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Establecimiento
    form_class = EstablecimientoUpdateForm
    success_url = reverse_lazy('wsfacturae:EstablecimientoList')
    template_name = 'wsfacturae/establecimiento_add.html'
    
    success_message = 'Información del Establecimiento almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff
    
    def get_initial(self):
        initial = super().get_initial()
        if self.object.direccionMun:
            departamento_id = self.object.direccionMun.departamento.id if self.object.direccionMun.departamento else None

            if departamento_id:
                opciones_departamento = departamento.objects.filter(id=departamento_id).filter(nm_estado=1).order_by(
                    "descripcion")
                initial['departamento'] = opciones_departamento.first()

            else:
                initial['departamento'] = None
                initial['direccionMun'] = []
        return super().get_initial()
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['query_municipio'] = municipio.objects.filter(nm_estado=1).order_by("descripcion")
        return kwargs
class PuntoVentaCreateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin,CreateView):
    form_class = PuntoVentaAddForm
    model=PuntoVenta
    template_name = 'wsfacturae/puntoventa_add.html'
    success_url = reverse_lazy('wsfacturae:EstablecimientoList')
    success_message = 'Información del punto de venta almacenada correctamente!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        return {
            'establecimiento_fk': self.kwargs[self.pk_url_kwarg]
        }
class PuntoVentaUpdateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = PuntoVenta
    template_name = "wsfacturae/puntoventa_add.html"
    form_class = PuntoVentaAddForm
    success_url = reverse_lazy('wsfacturae:EstablecimientoList')
    success_message = 'Información del punto de venta almacenada correctamente!'
    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

class PuntoVentaDeleteView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = PuntoVenta
    template_name = ".html"
    success_url = reverse_lazy('wsfacturae:EstablecimientoList')
    success_message = 'Información del SubCatactividadeco Almacenada Correctamente!!!!'
    
    def get(self, request, *args, **kwargs):
        try:
            obj = PuntoVenta.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El ítem ha sido eliminado satisfactoriamente.")
            my_render = reverse('wsfacturae:EstablecimientoList')
        except IntegrityError as e:
            messages.error(request, "El ítem no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse('wsfacturae:EstablecimientoList')
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff

class ReceptorNCreateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = ReceptorN
    form_class= ReceptorAddForm
    template_name = "wsfacturae/receptor_add.html"
    success_url = reverse_lazy('wsfacturae:ReceptorList')
    success_message = 'Información del Establecimiento Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        return {
            'nm_estado': 1
        }

class ReceptorNList(LoginRequiredMixin, FormMixin,ListView):
    paginate_by = getattr(settings, 'NUM_RECS_BY_PAG', None)
    form_class = ReceptorSearchForm
    template_name = 'wsfacturae/receptor_list.html'
    ajax_template_name = 'wsfacturae/receptor_list_results.html'

    def get_initial(self):
        return {
            'descripcion': '',
        }

    def get_queryset(self):
        qry = ReceptorN.objects.all().order_by("nombre", "id")
        return qry

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        return [self.template_name]

    def get_form_kwargs(self):
        return {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'data': self.request.GET or None
        }

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            self.object_list = form.filter_queryset(request, self.object_list)
        context = self.get_context_data(form=form, object_list=self.object_list)
        return self.render_to_response(context)

    def paginate_queryset(self, queryset, page_size):
        try:
            return super(ReceptorNList, self).paginate_queryset(queryset, page_size)
        except Http404:
            self.kwargs['page'] = 'last'
            return super(ReceptorNList, self).paginate_queryset(queryset, page_size)

class ReceptorNDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = ReceptorN
    success_url = reverse_lazy('wsfacturae:ReceptorList')
    form_valid_message = 'El receptor fue eliminado satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = ReceptorN.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El receptor ha sido eliminado satisfactoriamente.")
            my_render = reverse_lazy('wsfacturae:ReceptorList')
        except IntegrityError as e:
            messages.error(request, "La receptor no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse_lazy('wsfacturae:ReceptorList')
        return HttpResponseRedirect(my_render)


class ReceptorNUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = ReceptorN
    form_class = ReceptorUpdateForm
    success_url = reverse_lazy('wsfacturae:ReceptorList')
    template_name = 'wsfacturae/receptor_add.html'
    success_message = 'Informacion de Receptor Almacenada Correctamente!!!!'

    def form_valid(self, form ):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def get_initial(self):
        initial = super().get_initial()
        if self.object.municipio:
            departamento_id = self.object.municipio.departamento.id if self.object.municipio.departamento else None

            if departamento_id:
                opciones_departamento = departamento.objects.filter(id=departamento_id).filter(nm_estado=1).order_by(
                    "descripcion")
                initial['departamento'] = opciones_departamento.first()

            else:
                initial['departamento'] = None
                initial['municipio'] = []

        catactividadeco_id = self.object.actividadeco.subactividadeco.catactividadeco.id if self.object.actividadeco else None
        if catactividadeco_id:
            opciones_catactividadeco = catactividadeco.objects.filter(id=catactividadeco_id).filter(
                nm_estado=1).order_by(
                "descripcion")
            initial['catactividadeco'] = opciones_catactividadeco.first()

        else:
            initial['catactividadeco'] = None
            initial['subactividadeco'] = []

        if self.object.actividadeco:
            subactividadeco_id = self.object.actividadeco.subactividadeco.id if self.object.actividadeco.subactividadeco else None
            if subactividadeco_id:
                opciones_subactividadeco = subactividadeco.objects.filter(id=subactividadeco_id).filter(
                    nm_estado=1).order_by(
                    "descripcion")
                initial['subactividadeco'] = opciones_subactividadeco.first()

            else:
                initial['subactividadeco'] = None
                initial['actividadeco'] = []

        return initial
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['query_catactividadeco'] = catactividadeco.objects.filter(nm_estado=1).order_by("descripcion")
        kwargs['query_actividadeco'] = actividadeco.objects.filter(nm_estado=1).order_by("descripcion")
        kwargs['query_subactividadeco'] = subactividadeco.objects.filter(nm_estado=1).order_by("descripcion")
        kwargs['query_municipio'] = municipio.objects.filter(nm_estado=1).order_by("descripcion")
        kwargs['query_tipodocumento'] = detallemastercat.objects.filter(mastercat__codigo='CAT-022').filter(
            nm_estado=1).order_by("descripcion")

        return kwargs

class EmisorDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'wsfacturae/emisor_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['emisor'] = EmisorN.objects.first()  # Obtén el único registro de EmisorN
        return context

class EmisorUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = EmisorN
    form_class = EmisorNUpdateForm
    success_url = reverse_lazy('wsfacturae:emisor-detail')
    template_name = 'wsfacturae/emisor_upd.html'
    success_message = 'Informacion del Emisor Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        initial = super().get_initial()
        catactividadeco_id = self.object.actividadeco.subactividadeco.catactividadeco.id if self.object.actividadeco.subactividadeco.catactividadeco else None
        if catactividadeco_id:
            opciones_catactividadeco = catactividadeco.objects.filter(id=catactividadeco_id).filter(nm_estado=1).order_by(
                "descripcion")
            initial['catactividadeco'] = opciones_catactividadeco.first()

        else:
            initial['catactividadeco'] = None
            initial['subactividadeco'] = []


        subactividadeco_id = self.object.actividadeco.subactividadeco.id if self.object.actividadeco.subactividadeco else None
        if subactividadeco_id:
            opciones_subactividadeco = subactividadeco.objects.filter(id=subactividadeco_id).filter(
                nm_estado=1).order_by(
                "descripcion")
            initial['subactividadeco'] = opciones_subactividadeco.first()

        else:
            initial['subactividadeco'] = None
            initial['actividadeco'] = []

        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['query_subactividadeco'] = subactividadeco.objects.filter(nm_estado=1).order_by("descripcion")
        kwargs['query_actividadeco'] = actividadeco.objects.filter(nm_estado=1).order_by("descripcion")
        kwargs['query_catactividadeco'] = catactividadeco.objects.filter(nm_estado=1).order_by("descripcion")

        return kwargs


class DescuentoListView(LoginRequiredMixin, ListView):
    template_name = "wsfacturae/descuento_list.html"
    ajax_template_name='wsfacturae/descuento_list_result.html'
    paginate_by = 50
    
    def get_queryset(self):
        qry = Descuento.objects.order_by("producto")
        return qry

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        return [self.template_name]

    def get_form_kwargs(self):
        return {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'data': self.request.GET or None
        }

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        pos_decimales = param_version_dte.objects.get(codigo="1004")
        context['decimal'] = int(pos_decimales.tipoDato)
        return self.render_to_response(context)

    def test_func(self):
        return self.request.user.is_staff


class DescuentoAddView(LoginRequiredMixin, CreateView):
    form_class = DescuentoAddForm
    template_name = 'wsfacturae/descuento_add_upd.html'
    success_url = reverse_lazy('wsfacturae:DescuentoList')
    success_message = 'Información del Descuento Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        return {
            'nm_estado': 1
        }

class DescuentoUpdateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Descuento
    form_class = DescuentoAddForm
    success_url = reverse_lazy('wsfacturae:DescuentoList')
    template_name = 'wsfacturae/descuento_add_upd.html'
    
    success_message = 'Información del Descuento Actualizada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff


class DescuentoDelete(SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Descuento
    success_url = reverse_lazy('wsfacturae:DescuentoList')
    form_valid_message = 'El Ítem fué eliminado satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = Descuento.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El ítem ha sido eliminado satisfactoriamente.")
            my_render = reverse('wsfacturae:DescuentoList')
        except IntegrityError as e:
            messages.error(request, "El ítem no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse('wsfacturae:DescuentoList')
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff
    

class SMTPAddView(LoginRequiredMixin, CreateView):
    form_class = SMTPUpdateForm
    template_name = 'wsfacturae/smtp_upd.html'
    success_url = reverse_lazy('wsfacturae:smtp-detail')
    success_message = 'Información del SMTP Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff


class SMTPDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'wsfacturae/smtp_view.html'
    
    def get(self, request, *args, **kwargs):
        smtp_instance = SMTP.objects.first()

        if not smtp_instance:
            return redirect('wsfacturae:SMTPAdd')

        context = {'smtp': smtp_instance}
        return render(request, self.template_name, context)

class SMTPUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = SMTP
    form_class = SMTPUpdateForm
    success_url = reverse_lazy('wsfacturae:smtp-detail')
    template_name = 'wsfacturae/smtp_upd.html'
    success_message = 'Informacion del SMTP Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff

