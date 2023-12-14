from django import forms
from .models import filial
from django.db.models import Q
from user.models import user_rol_filial
from django.utils.timezone import make_aware
from wsfacturae.models import catactividadeco, subactividadeco,departamento,municipio,detallemastercat,actividadeco
from datetime import datetime
from datetime import timedelta

class FilialAddForm(forms.ModelForm):

    class Meta:
        model = filial
        fields = ['nombre']


class FilialUpdateForm(forms.ModelForm):

    class Meta:
        model = filial
        fields = ['nombre']