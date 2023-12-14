from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cobrox.models import filial
from uuid import uuid4


class Login_cv(models.Model):
    usuario = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    fecha = models.DateTimeField(auto_now_add=True)


# Create your models here.
class rol(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    codigo = models.CharField(max_length=3, null=False, blank=False)

    class Meta:
            ordering = ['nombre']

    def __str__(self):
        return self.nombre


class user_rol_filial(models.Model):
    usuario = models.ForeignKey(User, null=False, on_delete=models.DO_NOTHING)
    rol = models.ForeignKey(rol, null=False, on_delete=models.DO_NOTHING)
    filial = models.ForeignKey(filial, null=False, on_delete=models.DO_NOTHING)
