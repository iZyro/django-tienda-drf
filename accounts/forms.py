from .models import *
from django import forms
from django.forms.widgets import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario', 
        required=True,
        
        error_messages={
            'invalid': 'Ingresa un valor válido.'
        }, 
        widget=TextInput(attrs={
            'required': 'true', 
            'class': 'form-control'
            }))
    password = forms.CharField(label='Contraseña', required=True, widget=PasswordInput(attrs={'required': 'true', 'class': 'form-control'}))


class RegisterForm(forms.ModelForm):
    name = forms.CharField(
        label='Nombres',
        widget=TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        label='Apellidos',
        widget=TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(
        label='Nombre de usuario',
        widget=TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(
        label='Email',
        required=True,
        widget=EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserData
        fields = ['name', 'last_name', 'username', 'email', 'password'] + ['password2',]

        
class ForgotPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label = "Nueva contraseña",
        required = True,
        widget=PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(
        label = "Confirmar nueva contraseña",
        widget=PasswordInput(attrs={'class': 'form-control'}))
    
    error_messages={
        'password_mismatch': 'Las contraseñas no coinciden.'
    }
    