from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView,FormView,DetailView

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.db import transaction
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied

from io import BytesIO
from urllib.request import urlopen
from django.core.files import File
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .models import rol,Login_cv
from .forms import RolUpdateForm,RolAddForm,UserAddForm,UserUpdateForm,SetPasswordForm
from user.models import user_rol_filial
import datetime


class Login(FormView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'

    def form_valid(self, form):
        redirect_to = settings.LOGIN_REDIRECT_URL
        auth_login(self.request, form.get_user())
        obj_user = User.objects.get(id= self.request.user.id)
        log = Login_cv(usuario=obj_user)
        log.save()
        return HttpResponseRedirect(reverse_lazy(redirect_to))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(Login, self).dispatch(request, *args, **kwargs)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'La constraseña fue registrada satisfactoriamente')
            return redirect('user:change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {
        'form': form
    })


class RolDelete(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    model = rol
    success_url = reverse_lazy('user:RolList')
    form_valid_message = 'El Rol fue eliminada satisfactoriamente!'
    permission_required = ('is_staff')

    def get(self, request, *args, **kwargs):
        try:
            obj = rol.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El rol ha sido eliminado satisfactoriamente.")
            my_render = reverse_lazy('user:RolList')
        except IntegrityError as e:
            messages.error(request, "El rol no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse_lazy('user:RolList')
        return HttpResponseRedirect(my_render)


class RolUpdate(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = rol
    form_class = RolUpdateForm
    success_url = reverse_lazy('user:RolList')
    template_name = 'user/rol_add_upd.html'
    success_message = 'Informacion del Rol Almacenada Correctamente!!!!'
    permission_required = ('is_staff')

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()


class RolList(PermissionRequiredMixin, ListView):
    model = rol
    template_name = 'user/rol_list.html'
    permission_required = ('is_staff')

    def get_queryset(self):
        return rol.objects.all().order_by("id")


class RolAdd(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    form_class = RolAddForm
    template_name = 'user/rol_add_upd.html'
    success_url = reverse_lazy('user:RolList')
    success_message = 'Informacion del Rol Almacenada Correctamente!!!!'
    permission_required = ('is_staff')

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            return super().form_valid(form)
        return HttpResponseBadRequest()


class UserDelete(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('user:UserList')
    form_valid_message = 'El User fué eliminado satisfactoriamente!'
    permission_required = ('is_staff')

    def get(self, request, *args, **kwargs):
        try:
            cant_staf_activos = User.objects.filter(is_staff=True).filter(is_active=True).count()
            obj = User.objects.get(id=self.kwargs[self.pk_url_kwarg])
            if cant_staf_activos == 1 and obj.is_staff:
                messages.error(request,
                               "No puede eliminar  al presente usuario ya que es el único usuario con el atributo Staff activo, la aplicación requiere que al menos exista un usuario activo con el atributo Staff ")
            elif request.user.id == obj.id:
                messages.error(request,
                               "No puede borrarse a si mismo")
            else:
                with transaction.atomic():
                    try:
                        userobj = user_rol_filial.objects.get(usuario__id=self.kwargs[self.pk_url_kwarg])
                        userobj.delete()
                    except ObjectDoesNotExist:
                        None
                    obj.delete()
                messages.success(request, "El User ha sido eliminado satisfactoriamente.")
            my_render = reverse_lazy('user:UserList')
        except IntegrityError as e:
            messages.error(request, "El User no puede ser eliminado ya que tiene registros asociados")
            my_render = reverse_lazy('user:UserList')
        return HttpResponseRedirect(my_render)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            obj = User.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class UserUpdate(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('user:UserList')
    template_name = 'user/user_add_upd.html'
    success_message = 'Información del User Almacenada Correctamente!!!!'
    permission_required = ('is_staff')

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            with transaction.atomic():
                usr = form.save(commit=False)
                try:
                    obj_us_filial_rol = user_rol_filial.objects.get(usuario=usr)
                    obj_us_filial_rol.rol = form.cleaned_data['rol']
                    obj_us_filial_rol.filial = form.cleaned_data['filial']
                except ObjectDoesNotExist:
                    obj_us_filial_rol = user_rol_filial(
                            usuario=usr, rol=form.cleaned_data['rol'], filial=form.cleaned_data['filial'])
                obj_us_filial_rol.save()
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def get_initial(self):
        initial = super(UserUpdate, self).get_initial()
        try:
            obj= user_rol_filial.objects.get(usuario__id=self.kwargs['pk'])
            initial.update({
                'filial': obj.filial,
                'rol': obj.rol,
            })
        except ObjectDoesNotExist:
            None
        return initial


class UserList(PermissionRequiredMixin, ListView):
    model = User
    template_name = 'user/user_list.html'
    permission_required = ('is_staff')

    def get_queryset(self):
        return User.objects.all().order_by("last_name","id")


class UserAdd(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    form_class = UserAddForm
    template_name = 'user/user_add_upd.html'
    success_url = reverse_lazy('user:UserList')
    success_message = 'Informacion del User Almacenada Correctamente!!!!'
    permission_required = ('is_staff')

    def form_valid(self, form):
        action = self.request.POST.get('action')
        form = self.form_class(self.request.POST)
        if action == 'SAVE':
            with transaction.atomic():
                usr = form.save(commit=False)
                usr.save()
                obj_us_filial_rol = user_rol_filial(usuario=usr, rol=form.cleaned_data['rol'], filial=form.cleaned_data['filial'])
                obj_us_filial_rol.save()
            return super().form_valid(form)
        return HttpResponseBadRequest()

    def get_success_url(self):
        return reverse('user:PasswordResetConfirmView',
                       kwargs={'pk':self.object.id}
                       )


class PasswordResetConfirmView(FormView):
    template_name = "user/set_new_pass.html"
    success_url = reverse_lazy('user:UserList')
    form_class = SetPasswordForm

    def user(self):
        return User.objects.get(pk=self.kwargs['pk'])

    def post(self, request, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        form = self.form_class(request.POST)

        user = User.objects.get(pk=self.kwargs['pk'])
        if form.is_valid():
            new_password = form.cleaned_data['new_password2']
            user.set_password(new_password)
            user.save()
            messages.success(request, 'El password ha sido reseteado para ' + user.username +'. Ingresa con el nuevo password')
            return self.form_valid(form)
        else:
            messages.error(request, 'El reset del password no ha sido exitoso')
            return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            obj = User.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CambiarEstado(PermissionRequiredMixin,DetailView):
    success_url = reverse_lazy('user:UserList')
    form_valid_message = 'El registro fue actualizado satisfactoriamente!'
    permission_required = ('is_staff')

    def get(self, request, *args, **kwargs):
        obj = User.objects.get(id=self.kwargs['pk'])
        if obj.is_active:
            cant_staf_activos = User.objects.filter(is_staff=True).filter(is_active=True).count()
            if cant_staf_activos == 1 and obj.is_staff:
                messages.error(request,
                                 "No puede desactivar al presente usuario ya que es el único usuario con el atributo Staff activo, la aplicación requiere que al menos exista un usuario activo con el atributo Staff ")
            else:
                obj.is_active = False
                obj.save()
                messages.success(request,
                                 "El usuario ha sido desactivado satisfactoriamente")
        else:
            obj.is_active = True
            obj.save()
            messages.success(request,
                             "El usuario ha sido activado satisfactoriamente")
        my_render = reverse_lazy('user:UserList')
        return HttpResponseRedirect(my_render)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            obj = User.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CambiarTipo(PermissionRequiredMixin,DetailView):
    success_url = reverse_lazy('user:UserList')
    form_valid_message = 'El registro fue actualizado satisfactoriamente!'
    permission_required = ('is_staff')

    def get(self, request, *args, **kwargs):

        obj = User.objects.get(id=self.kwargs['pk'])
        if obj.is_staff:

            if User.objects.filter(is_staff=True).count() >= 2:
                obj.is_staff= False
                obj.save()
                messages.success(request,
                                 "El usuario ha sido retirado el atributo de staff satisfactoriamente")
            else:
                messages.error(request,
                               "No puede removerse el atributo de Staff ya que es el único usuario con este atributo activo, la aplicación requiere que al menos exista un usuario con el atributo Staff ")
        else:
            obj.is_staff = True
            obj.save()
            messages.success(request,
                             "El usuario ha sido asignado el atributo de staff satisfactoriamente")

        my_render = reverse_lazy('user:UserList')
        return HttpResponseRedirect(my_render)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            obj = User.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)