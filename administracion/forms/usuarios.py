from django import forms
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'rol']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el apellido'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el correo electrónico'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'rol': 'Rol',
        }
