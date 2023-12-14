from django.shortcuts import render,redirect
from django.views.generic import (ListView,CreateView,UpdateView,DeleteView)
from django.http import HttpResponseRedirect
from .models import filial
from .forms import FilialAddForm,FilialUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.urls import reverse_lazy,reverse
from django.utils.timezone import make_aware
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.mixins import UserPassesTestMixin
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.template.defaultfilters import date as _date

from django.core.validators import validate_email
from django.contrib.auth.decorators import user_passes_test

from urllib.request import urlopen

class LogoutIfNotSuperUserMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            logout(request)
            return self.handle_no_permission()
        return super(LogoutIfNotSuperUserMixin, self).dispatch(request, *args, **kwargs)


class LogoutIfNotStaffMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            logout(request)
            return self.handle_no_permission()
        return super(LogoutIfNotStaffMixin, self).dispatch(request, *args, **kwargs)


class Viewindex(LoginRequiredMixin, ListView):
    success_url = reverse_lazy('cobrox/index.html')
    template_name = "cobrox/index.html"

    def get_context_data(self, **kwargs):
        context = super(Viewindex, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        pass

    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)


class FilialDelete(SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = filial
    success_url = reverse_lazy('cobrox:FilialList')
    form_valid_message = 'La Filial fue eliminada satisfactoriamente!'

    def get(self, request, *args, **kwargs):
        try:
            obj = filial.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "La filial ha sido eliminado satisfactoriamente.")
            my_render = reverse_lazy('cobrox:FilialList')
        except IntegrityError as e:
            messages.error(request, "La filial no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse_lazy('cobrox:FilialList')
        return HttpResponseRedirect(my_render)

    def test_func(self):
        return self.request.user.is_staff


class FilialUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = filial
    form_class = FilialUpdateForm
    success_url = reverse_lazy('cobrox:FilialList')
    template_name = 'cobrox/filial_add_upd.html'
    success_message = 'Informacion del Filial Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def test_func(self):
        return self.request.user.is_staff


class FilialList(UserPassesTestMixin, ListView):
    model = filial
    template_name = 'cobrox/filial_list.html'
    permission_required = ('user.is_staff')

    def get_queryset(self):
        return filial.objects.all()

    def test_func(self):
        return self.request.user.is_staff


class FilialAdd(SuccessMessageMixin, UserPassesTestMixin, CreateView):
    form_class = FilialAddForm
    template_name = 'cobrox/filial_add_upd.html'
    success_url = reverse_lazy('cobrox:FilialList')
    success_message = 'Informacion del Filial Almacenada Correctamente!!!!'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()
    
    def test_func(self):
        return self.request.user.is_staff
