from django import forms
from .models import rol
from cobrox.models import filial
from django.contrib.auth.models import User


class RolAddForm(forms.ModelForm):

    class Meta:
        model = rol
        fields = ['nombre','codigo']


class RolUpdateForm(forms.ModelForm):

    class Meta:
        model = rol
        fields = ['nombre','codigo']


class UserAddForm(forms.ModelForm):
    rol = forms.ModelChoiceField(
        queryset=rol.objects.all()
    )

    filial = forms.ModelChoiceField(
        queryset=filial.objects.all()
    )

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


class UserUpdateForm(forms.ModelForm):
    rol = forms.ModelChoiceField(
        queryset=rol.objects.all()
    )

    filial = forms.ModelChoiceField(
        queryset=filial.objects.all()
    )

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','is_active','is_staff']


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("Los dos passwords no coinciden."),
        }
    new_password1 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    new_password2 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Repita el Password'}))

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2