from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.conf import settings
from simple_history.models import HistoricalRecords
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from wsfacturae.models import detallemastercat,municipio,actividadeco

import datetime
import os
ingresado = 0
conciliado = 1
estaoregistroc = (
    (ingresado, 'INGRESADO'),
    (conciliado, 'CONCILIADO'),
)
# Create your models here.


def imagepacexp_directory_path_with_uuid(instance, filename):
    extension = filename.split(".")[1].lower()
    return settings.PROJECT_ROOT + '/static/images/arc_clientes/{}/{}.{}'.format( instance.cliente_id, uuid4(),extension)


def imagecreexp_directory_path_with_uuid(instance, filename):
    extension = filename.split(".")[1].lower()
    return settings.PROJECT_ROOT + '/static/images/arc_clientes/{}/credito/{}/{}.{}'.format(instance.credito.cliente_id, instance.credito_id, uuid4(),extension)

#Preguntar cual tabla es esta dentro del front
class filial(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    user_creation = CurrentUserField(related_name='user_creationcc')
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    user_last_update = CurrentUserField(on_update=True)

    history = HistoricalRecords()


    class Meta:
            ordering = ['nombre']

    def __str__(self):
        return self.nombre