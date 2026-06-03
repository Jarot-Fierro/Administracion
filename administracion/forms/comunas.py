from django import forms

from administracion.models import Comuna


class ComunaForm(forms.ModelForm):
    class Meta:
        model = Comuna
        fields = ['nombre', 'codigo']

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre de la comuna'
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
