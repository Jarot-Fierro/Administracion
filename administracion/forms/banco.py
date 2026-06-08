from django import forms

from administracion.models.banco import Banco


class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ['nombre', 'codigo', 'website']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }
