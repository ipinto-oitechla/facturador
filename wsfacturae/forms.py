from django import forms
from django_select2.forms import ModelSelect2Widget
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Establecimiento, PuntoVenta, ReceptorN, param_version_dte, wsentorno,wsurl,\
    mastercat,detallemastercat, catactividadeco,subactividadeco,actividadeco,\
    departamento,municipio,tributo, Productos,EmisorN,Descuento, SMTP
from django.db.models import Q

class InsertarDteForm(forms.Form):
    fecha = forms.CharField(required=True)
    receptor = forms.ModelChoiceField(
        queryset=ReceptorN.objects.all(),
        required=False
    )
    establecimiento = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    puntoventa = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))

class AgregarMetodoPagoForm(forms.Form):
    forma_pago = forms.ModelChoiceField(queryset=detallemastercat.objects.filter(mastercat=mastercat.objects.get(id=14)).order_by("descripcion"), label="Forma de pago", required=False)
    monto = forms.DecimalField(decimal_places=2, min_value=0.01, required=True)
    
class ParametrosForm(forms.ModelForm):
    model = param_version_dte
    class Meta:
        fields = '__all__'


class EmisorNUpdateForm(forms.ModelForm):
    catactividadeco = forms.ModelChoiceField(
        queryset=catactividadeco.objects.filter(nm_estado=1).order_by("descripcion"), label="Categoría Económica")
    subactividadeco = forms.ModelChoiceField(
        queryset=subactividadeco.objects.filter(nm_estado=1).order_by("descripcion"), label="Subcategoría Económica")

    class Meta:
        model = EmisorN
        fields = ['nit',
                  'nrc',
                  'nombre',
                  'actividadeco',
                  'nombrecomercial',
                  'email',
                  'logo',
                  'natural'

                  ]
        widgets = {
            'nit': forms.TextInput(attrs={'placeholder': '____-______-___-_', 'data-mask': '9999-999999-999-9'}),
            'telefono': forms.TextInput(attrs={'placeholder': '____-____', 'data-mask': '9999-9999'}),
            'celular': forms.TextInput(attrs={'placeholder': '____-____', 'data-mask': '9999-9999'}),
        }
        labels = {
            'nit': 'NIT:',
            'nrc': 'NRC:',
            'nombre': 'Nombre:',
            'actividadeco': 'Actividad Económica:',
            'nombrecomercial': 'Nombre Comercial:',
            'email': 'Email:',
            'logo':'Logo de la empresa:',
            'natural':'¿Es persona natural?'

        }
    def __init__(self, *args, **kwargs):
        query_catactividadeco = kwargs.pop('query_catactividadeco')
        query_subactividadeco = kwargs.pop('query_subactividadeco')
        query_actividadeco = kwargs.pop('query_actividadeco')
        super().__init__(*args, **kwargs)
        self.fields['subactividadeco'].queryset = query_subactividadeco
        self.fields['actividadeco'].queryset = query_actividadeco
        self.fields['catactividadeco'].queryset = query_catactividadeco


class AgregarProductoForm(forms.Form):
    producto = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    cantidad = forms.IntegerField(required=True,min_value=1)

class ProductoSearchForm(forms.Form):
    nombre = forms.CharField(required=True)

class ReceptorUpdateForm(forms.ModelForm):
    catactividadeco = forms.ModelChoiceField(required=False,
        queryset=catactividadeco.objects.filter(nm_estado=1).order_by("descripcion"), label="Categoría Económica")
    subactividadeco = forms.ModelChoiceField(required=False,
        queryset=subactividadeco.objects.filter(nm_estado=1).order_by("descripcion"), label="Subcategoría Económica")
    departamento = forms.ModelChoiceField(required=False,
        queryset=departamento.objects.filter(nm_estado=1).order_by("descripcion"), label="Departamento")

    class Meta:
        model = ReceptorN
        fields = ['tipodocumento',
                  'nodocumento',
                  'nrc',
                  'nombre',
                  'nombreComercial',
                  'actividadeco',
                  'municipio',
                  'complementodir',
                  'telefono',
                  'celular',
                  'email',
                  'gran_contr'
                  ]
        widgets = {
            'telefono': forms.TextInput(attrs={'placeholder': '____-____', 'data-mask': '9999-9999'}),
            'celular': forms.TextInput(attrs={'placeholder': '____-____', 'data-mask': '9999-9999'}),
        }
        labels = {
            'tipodocumento': 'Tipo de Documento:',
            'nodocumento': 'No de Documento:',
            'nrc': 'NRC:',
            'nombre': 'Nombre:',
            'nombreComercial': 'Nombre comercial:',
            'actividadeco': 'Actividad Económica:',
            'complementodir': 'Dirección:',
            'telefono': 'Teléfono:',
            'celular': 'Celular:',
            'email': 'Email:',
            'gran_contr':'¿Es gran contribuyente?'
        }

    def __init__(self, *args, **kwargs):
        query_catactividadeco = kwargs.pop('query_catactividadeco')
        query_municipio = kwargs.pop('query_municipio')
        query_subactividadeco = kwargs.pop('query_subactividadeco')
        query_actividadeco = kwargs.pop('query_actividadeco')
        query_tipodocumento = kwargs.pop('query_tipodocumento')
        super().__init__(*args, **kwargs)
        self.fields['municipio'].queryset = query_municipio
        self.fields['subactividadeco'].queryset = query_subactividadeco
        self.fields['actividadeco'].queryset = query_actividadeco
        self.fields['catactividadeco'].queryset = query_catactividadeco
        self.fields['tipodocumento'].queryset = query_tipodocumento

class ReceptorSearchForm(forms.Form):
    descripcion = forms.CharField (required=False)

    def filter_queryset(self, request, queryset):
        if self.cleaned_data['descripcion']:
            return queryset.filter(Q(nombre__unaccent__icontains=self.cleaned_data['descripcion']) | Q(actividadeco__descripcion__unaccent__icontains=self.cleaned_data['descripcion']) | Q(actividadeco__subactividadeco__descripcion__unaccent__icontains=self.cleaned_data['descripcion']))
        return queryset

class ReceptorAddForm(forms.ModelForm):

    catactividadeco = forms.ModelChoiceField(required=False,
        queryset=catactividadeco.objects.filter(nm_estado=1).order_by("descripcion"), label="Categoría Económica")
    subactividadeco = forms.ModelChoiceField(required=False,
        queryset=subactividadeco.objects.filter(nm_estado=1).order_by("descripcion"), label="Subcategoría Económica")
    departamento = forms.ModelChoiceField(required=False,
        queryset=departamento.objects.filter(nm_estado=1).order_by("descripcion"), label="Departamento")
    nombre = forms.CharField(required=True, label="Nombre")
    nombreComercial = forms.CharField(required=True, label="Nombre comercial")

    class Meta:
        model = ReceptorN
        fields =[   'tipodocumento',
                    'nodocumento',
                    'nrc',
                    'nombre',
                    'nombreComercial',
                    'actividadeco',
                    'municipio',
                    'complementodir',
                    'telefono',
                    'celular',
                    'email',
                    'gran_contr'
                ]
        widgets = {
            'telefono': forms.TextInput(attrs={'placeholder': '____-____', 'data-mask': '9999-9999'}),
            'celular': forms.TextInput(attrs={'placeholder': '____-____', 'data-mask': '9999-9999'}),
        }
        labels = {
            'tipodocumento': 'Tipo de Documento:',
            'nodocumento': 'No de Documento:',
            'nrc': 'NRC:',
            'nombre': 'Nombre:',
            'nombreComercial': 'Nombre comercial:',
            'actividadeco': 'Actividad Económica:',
            'complementodir': 'Dirección:',
            'telefono': 'Teléfono:',
            'celular': 'Celular:',
            'email': 'Email:',
            'gran_contr':'¿Es gran contribuyente?'
        }

    def __init__(self, *args, **kwargs):
        super(ReceptorAddForm, self).__init__(*args, **kwargs)
        self.fields['municipio'].queryset = municipio.objects.none()
        self.fields['subactividadeco'].queryset = subactividadeco.objects.none()
        self.fields['tipodocumento'].queryset = detallemastercat.objects.filter(mastercat__codigo='CAT-022').filter(nm_estado=1).order_by("descripcion")
        self.fields['actividadeco'].queryset = actividadeco.objects.none()

        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['municipio'].queryset = municipio.objects.filter(
                    departamento__id=departamento_id).filter(nm_estado=1).order_by('descripcion')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Talla queryset
        elif self.instance.pk:
            self.fields['municipio'].queryset = self.instance.departamento.municipio_set.order_by(
                'descripcion')

        if 'catactividadeco' in self.data:
            try:
                catactividadeco_id = int(self.data.get('catactividadeco'))
                self.fields['subactividadeco'].queryset = subactividadeco.objects.filter(
                    catactividadeco__id=catactividadeco_id).filter(nm_estado=1).order_by('descripcion')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Talla queryset
        elif self.instance.pk:
            self.fields['subactividadeco'].queryset = self.instance.catactividadeco.subactividadeco_set.order_by(
                'descripcion')

        if 'subactividadeco' in self.data:
            try:
                subactividadeco_id = int(self.data.get('subactividadeco'))
                self.fields['actividadeco'].queryset = actividadeco.objects.filter(
                    subactividadeco__id=subactividadeco_id).filter(nm_estado=1).order_by('descripcion')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Talla queryset
        elif self.instance.pk:
            self.fields['actividadeco'].queryset = self.instance.subactividadeco.actividadeco_set.order_by(
                'descripcion')

class ConsultaDteSearchForm(forms.Form):
   tipoDTE_choices = detallemastercat.objects.filter(mastercat=mastercat.objects.get(id=2)).order_by("descripcion")
   tipoDTE = forms.ModelChoiceField(required=False, queryset=tipoDTE_choices)
   emisor = forms.CharField(required=False)
   factura = forms.CharField(required=False)
   fecha_ini = forms.CharField(required=False)
   fecha_fin = forms.CharField(required=False)

   
   def filter_queryset(self, request, queryset):
        dte_selected = self.cleaned_data['tipoDTE']
        fechaini_selected = self.cleaned_data['fecha_ini']
        emisor_selected = self.cleaned_data['emisor']
        factura_selected = self.cleaned_data['factura']
        dte_selected = self.cleaned_data['tipoDTE']
        qs = queryset
        if dte_selected:
                qs = qs.filter(Q(fk_Identificacion__tipoDte=dte_selected))
        if emisor_selected:
            qs = qs.filter(Q(fk_receptor__nombre__unaccent__icontains=emisor_selected))

        if fechaini_selected:
            fecha_ini = self.cleaned_data['fecha_ini']
            fecha_fin = self.cleaned_data['fecha_fin']
            if fecha_ini:
                aware_ini = make_aware(datetime.strptime(fecha_ini, '%Y-%m-%d'))
            else:
                aware_ini = None

            if fecha_fin:
                aware_fin = make_aware(datetime.strptime(fecha_fin, '%Y-%m-%d'))
            else:
                aware_fin = None
            qs = qs.filter(fecha__range = (aware_ini,aware_fin))
        if  factura_selected:
            qs = qs.filter(Q(codFacturaEmpresa__unaccent__icontains=factura_selected))
        return qs
        

class WsEntornoAddForm(forms.ModelForm):

    class Meta:
        model = wsentorno
        fields = ['codigo','nombre','url']

class AddProductoForm(forms.ModelForm):
    preciouni = forms.DecimalField(decimal_places=2)
    exentoIva = forms.ChoiceField(label="¿Es exento de IVA?", choices=[('S', 'Sí'),('N', 'No'),])
    class Meta:
        model = Productos
        fields = ['codigo', 'descripcion', 'preciouni', 'tipoitem','unimedida','exentoIva','tributo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        opciones_tipo_item = detallemastercat.objects.filter(mastercat=mastercat.objects.get(id=11)).order_by("descripcion")
        opciones_tipo_tributo = tributo.objects.order_by("descripcion")
        opciones_unidad_medida = detallemastercat.objects.filter(mastercat=mastercat.objects.get(id=12)).order_by("descripcion")    
        
        self.fields['unimedida'] = forms.ModelChoiceField(
            queryset=opciones_unidad_medida,
            label="Categoría de Unidad de Medida"
        )
        self.fields['tipoitem'] = forms.ModelChoiceField(
            queryset=opciones_tipo_item,
            label="Tipo de item"
        )
        self.fields['tributo'] = forms.ModelChoiceField(
            queryset=opciones_tipo_tributo,
            label="Tipo de Tributo"
        )

class EstablecimientoAddForm(forms.ModelForm):
    opciones_tipo_estab = detallemastercat.objects.filter(mastercat=mastercat.objects.get(id=9)).order_by("descripcion")
    departamento = forms.ModelChoiceField(required=False,
        queryset=departamento.objects.filter(nm_estado=1).order_by("descripcion"), label="Departamento")
    tipoEstable = forms.ModelChoiceField(required=False, queryset=opciones_tipo_estab)

    class Meta:
        model = Establecimiento
        fields = ['direccionMun','tipoEstable','complementodir','telefono','celular','codestablemh','codestablec']
        widgets = {
            'telefono': forms.TextInput(attrs={'placeholder': '____-____', 'data-mask': '9999-9999'}),
            'celular': forms.TextInput(attrs={'placeholder': '____-____', 'data-mask': '9999-9999'}),
        }
    def __init__(self, *args, **kwargs):
        super(EstablecimientoAddForm, self).__init__(*args, **kwargs)
        self.fields['direccionMun'].queryset = municipio.objects.none()
        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['direccionMun'].queryset = municipio.objects.filter(
                    departamento__id=departamento_id).filter(nm_estado=1).order_by('descripcion')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Talla queryset
        elif self.instance.pk:
            self.fields['direccionMun'].queryset = self.instance.departamento.municipio_set.order_by(
                'descripcion')
            
class EstablecimientoUpdateForm(forms.ModelForm):
    opciones_tipo_estab = detallemastercat.objects.filter(mastercat=mastercat.objects.get(id=9)).order_by("descripcion")
    departamento = forms.ModelChoiceField(required=False,
        queryset=departamento.objects.filter(nm_estado=1).order_by("descripcion"), label="Departamento")
    tipoEstable = forms.ModelChoiceField(required=False, queryset=opciones_tipo_estab)
    class Meta:
        model = Establecimiento
        fields = ['direccionMun','tipoEstable','complementodir','telefono','celular','codestablemh','codestablec']
        widgets = {
            'telefono': forms.TextInput(attrs={'placeholder': '____-____', 'data-mask': '9999-9999'}),
            'celular': forms.TextInput(attrs={'placeholder': '____-____', 'data-mask': '9999-9999'}),
        }

    def __init__(self, *args, **kwargs):

        query_municipio = kwargs.pop('query_municipio')
        super().__init__(*args, **kwargs)
        self.fields['direccionMun'].queryset = query_municipio

class PuntoVentaAddForm(forms.ModelForm):
    def clean_codpuntoventamh(self):
        codpuntoventamh = self.cleaned_data.get('codpuntoventamh')
        if codpuntoventamh is None:
            return ""  # Si el campo está vacío, asigna una cadena vacía
        return codpuntoventamh

    class Meta:
        model = PuntoVenta
        fields = ['establecimiento_fk', 'codpuntoventamh', 'codpuntoventa']
        labels = {}
        widgets = {'establecimiento_fk': forms.HiddenInput()}

class WsEntornoUpdateForm(forms.ModelForm):

    class Meta:
        model = wsentorno
        fields = ['codigo','nombre','url']


class WsUrlAddForm(forms.ModelForm):

    class Meta:
        model = wsurl
        fields = ['wsentorno','codigo','nombre','url']


class WsUrlUpdateForm(forms.ModelForm):

    class Meta:
        model = wsurl
        fields = ['wsentorno','codigo','nombre','url']


class MastercatAddForm(forms.ModelForm):

    class Meta:
        model = mastercat
        fields = ['codigo','descripcion','nm_estado']
        labels = {
                    'codigo': 'Código:',
                    'descripcion': 'Descripción:',
                }
        widgets = {'nm_estado': forms.HiddenInput()}


class MastercatUpdateForm(forms.ModelForm):

    class Meta:
        model = mastercat
        fields = ['codigo','descripcion','nm_estado']
        labels = {
            'codigo': 'Código:',
            'descripcion': 'Descripción:',
        }


class DetalleMastercatAddForm(forms.ModelForm):
    class Meta:
        model = detallemastercat
        fields = ['codigo', 'descripcion', 'nm_estado','mastercat']
        labels = {
            'codigo': 'Código:',
            'descripcion': 'Descripción:',
        }
        widgets = {'nm_estado': forms.HiddenInput(),
                   'mastercat': forms.HiddenInput()}

    def clean(self):
        form = super(DetalleMastercatAddForm, self).clean()

        existen = detallemastercat.objects.filter(mastercat=form['mastercat']).filter(codigo=form['codigo']).count()
        if existen > 0:
            raise forms.ValidationError(
                "Ya existe el código "+ form['codigo'] +" en el catálogo seleccionado")

        return form


class DetalleMastercatUpdateForm(forms.ModelForm):
    class Meta:
        model = detallemastercat
        fields = ['codigo', 'descripcion', 'nm_estado','mastercat']
        labels = {
            'codigo': 'Código:',
            'descripcion': 'Descripción:',
            'nm_estado':'Estado'
        }
        widgets = {
                   'mastercat': forms.HiddenInput(),
                   'codigo':forms.TextInput(attrs={'class':'form-control','readonly':True})}


class CategoriaAEAddForm(forms.ModelForm):

    class Meta:
        model = catactividadeco
        fields = ['descripcion','nm_estado']
        labels = {
                    'descripcion': 'Descripción:',
                }
        widgets = {'nm_estado': forms.HiddenInput()}


class CategoriaAEUpdForm(forms.ModelForm):

    class Meta:
        model = catactividadeco
        fields = ['descripcion','nm_estado']
        labels = {
                    'descripcion': 'Descripción:',
                }


class SubCategoriaAEAddForm(forms.ModelForm):

    class Meta:
        model = subactividadeco
        fields = ['descripcion','catactividadeco','nm_estado']
        labels = {
                    'descripcion': 'Descripción:',
                    'catactividadeco':'Categoría:'
                }
        widgets = {'nm_estado': forms.HiddenInput(),
                   'catactividadeco': forms.HiddenInput()}


class SubCategoriaAEUpdForm(forms.ModelForm):

    class Meta:
        model = subactividadeco
        fields = ['descripcion','catactividadeco','nm_estado']
        labels = {
                    'descripcion': 'Descripción:',
                    'catactividadeco': 'Categoría:'
                }
        widgets = {'catactividadeco': forms.HiddenInput()}


class ActividadecoAddForm(forms.ModelForm):
    catactividadeco = forms.ModelChoiceField(queryset=catactividadeco.objects.filter(nm_estado=1).order_by("descripcion"),label="Categoría")

    class Meta:
        model = actividadeco
        fields = ['codigo','descripcion','subactividadeco','nm_estado']
        labels = {
                    'descripcion': 'Descripción:',
                    'codigo': 'Código:',
                    'subactividadeco': 'Sub categoría:',

                }
        widgets = {'nm_estado': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(ActividadecoAddForm, self).__init__(*args, **kwargs)
        self.fields['subactividadeco'].queryset = subactividadeco.objects.none()

        if 'catactividadeco' in self.data:
            try:
                catactividadeco_id = int(self.data.get('catactividadeco'))
                self.fields['subactividadeco'].queryset = subactividadeco.objects.filter(catactividadeco__id=catactividadeco_id).filter(nm_estado=1).order_by('descripcion')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Talla queryset
        elif self.instance.pk:
            self.fields['subactividadeco'].queryset = self.instance.catactividadeco.subactividadeco_set.order_by('descripcion')


class ActividadecoUpdForm(forms.ModelForm):
    catactividadeco = forms.ModelChoiceField(
        queryset=catactividadeco.objects.filter(nm_estado=1).order_by("descripcion"), label="Categoría")

    class Meta:
        model = actividadeco
        fields = ['subactividadeco', 'codigo', 'descripcion', 'nm_estado']
        labels = {
            'descripcion': 'Descripción:',
            'codigo': 'Código:',
            'nm_estado' :'Estado',
            'subactividadeco': 'Sub categoría:'
        }

    def __init__(self, *args, **kwargs):
        query_subactividadeco = kwargs.pop('query_subactividadeco')
        super().__init__(*args, **kwargs)
        self.fields['subactividadeco'].queryset = query_subactividadeco


class ActividadecoSearchForm(forms.Form):
    descripcion = forms.CharField (required=False)

    def filter_queryset(self, request, queryset):
        if self.cleaned_data['descripcion']:
            return queryset.filter(Q(codigo__unaccent__icontains=self.cleaned_data['descripcion']) | Q(descripcion__unaccent__icontains=self.cleaned_data['descripcion']) | Q(subactividadeco__descripcion__unaccent__icontains=self.cleaned_data['descripcion']) | Q(subactividadeco__catactividadeco__descripcion__unaccent__icontains=self.cleaned_data['descripcion']))
        return queryset


class DepartamentoAddForm(forms.ModelForm):

    class Meta:
        model = departamento
        fields = ['codigo','descripcion','nm_estado']
        labels = {
                    'codigo': 'Código:',
                    'descripcion': 'Descripción:',
                }
        widgets = {'nm_estado': forms.HiddenInput()}


class DepartamentoUpdateForm(forms.ModelForm):

    class Meta:
        model = departamento
        fields = ['codigo','descripcion','nm_estado']
        labels = {
            'codigo': 'Código:',
            'descripcion': 'Descripción:',
        }


class MunicipioAddForm(forms.ModelForm):
    class Meta:
        model = municipio
        fields = ['codigo', 'descripcion', 'nm_estado','departamento']
        labels = {
            'codigo': 'Código:',
            'descripcion': 'Descripción:',
        }
        widgets = {'nm_estado': forms.HiddenInput(),
                   'departamento': forms.HiddenInput()}

    def clean(self):
        form = super(MunicipioAddForm, self).clean()

        existen = municipio.objects.filter(departamento=form['departamento']).filter(codigo=form['codigo']).count()
        if existen > 0:
            raise forms.ValidationError(
                "Ya existe el código "+ form['codigo'] +" en el deprtamento seleccionado")

        return form


class MunicipioUpdateForm(forms.ModelForm):
    class Meta:
        model = municipio
        fields = ['codigo', 'descripcion', 'nm_estado','departamento']
        labels = {
            'codigo': 'Código:',
            'descripcion': 'Descripción:',
            'nm_estado':'Estado'
        }
        widgets = {
                   'departamento': forms.HiddenInput(),
                   'codigo':forms.TextInput(attrs={'class':'form-control','readonly':True})}


class TributoAddForm(forms.ModelForm):
    class Meta:
        model = tributo
        fields = ['seccion', 'codigo', 'descripcion', 'tipo', 'valor', 'nm_estado']
        labels = {
            'seccion': 'Sección:',
            'codigo': 'Código:',
            'descripcion': 'Descripción:',
            'tipo': 'Tipo:',
            'valor': 'Valor:',
        }
        widgets = {'nm_estado': forms.HiddenInput()}


class TributoUpdateForm(forms.ModelForm):
    class Meta:
        model = tributo
        fields = ['seccion', 'codigo', 'descripcion', 'tipo', 'valor', 'nm_estado']
        labels = {
            'seccion': 'Sección:',
            'codigo': 'Código:',
            'descripcion': 'Descripción:',
            'tipo': 'Tipo:',
            'valor': 'Valor:',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'readonly': True})}
        

class DescuentoAddForm(forms.ModelForm):
    tipo_descuento = forms.ChoiceField(label="Tipo de descuento", choices=[
        (None, '---------'),
        ('MONTO_ITEM', 'Monto item'),
        ('PORCENTUAL_ITEM', 'Porcentual item'),
        ('MONTO_FACTURA', 'Monto factura'),
        ('PORCENTUAL_FACTURA', 'Porcentual factura')
    ])
    cantidad = forms.DecimalField(decimal_places=2)
    valor_descuento = forms.DecimalField(decimal_places=2)
    tipo_producto = forms.ChoiceField(
        required=False,
        choices=[
            (None, '---------'),
            ('S', 'Exento'),
            ('N', 'Gravado')
        ])
    
    class Meta:
        model = Descuento
        fields = ['tipo_descuento', 'producto', 'tipo_producto', 'cantidad', 'valor_descuento', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.widgets.DateInput(attrs={
                'type': 'date',
                'class':'form-control',
            }),
            'fecha_fin': forms.widgets.DateInput(attrs={
                'type': 'date',
                'class':'form-control',
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['producto'] = forms.ModelChoiceField(
            queryset=Productos.objects.order_by("descripcion"),
            label="Producto",
            required=False,
        )
        

class SMTPUpdateForm(forms.ModelForm):
    class Meta:
        model = SMTP
        fields = ['host', 'port', 'use_tls', 'username', 'password']
        
        labels = {
            'host': 'Host:',
            'port': 'Puerto:',
            'use_tls': 'TLS:',
            'username': 'Nombre de Usuario:',
            'password': 'Contraseña:',
        }
    
