from django import forms

from administracion.models.calidad_juridica import CalidadJuridica


class CalidadJuridicaForm(forms.ModelForm):
    class Meta:
        model = CalidadJuridica
        fields = ['nombre', 'codigo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
        }
