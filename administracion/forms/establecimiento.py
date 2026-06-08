from django import forms

from administracion.models import Establecimiento


class EstablecimientoForm(forms.ModelForm):
    class Meta:
        model = Establecimiento
        fields = ['nombre', 'codigo']

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del establecimiento'
                }
            ),
            'codigo': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el código'
                }
            ),
        }

        labels = {
            'nombre': 'Nombre',
            'codigo': 'Código',
        }
