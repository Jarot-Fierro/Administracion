from django import forms

from administracion.models.funcionarios import Funcionario


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = [
            'rut', 'nombres', 'apellido_paterno', 'apellido_materno',
            'email', 'telefono', 'calidad_juridica', 'departamento',
            'comuna_residencia', 'banco', 'numero_cuenta', 'tipo_cuenta',
            'cargo', 'grado', 'horas_contrato'
        ]
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'calidad_juridica': forms.Select(attrs={'class': 'form-select'}),
            'departamento': forms.Select(attrs={'class': 'form-select'}),
            'comuna_residencia': forms.Select(attrs={'class': 'form-select'}),
            'banco': forms.Select(attrs={'class': 'form-select'}),
            'numero_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'grado': forms.TextInput(attrs={'class': 'form-control'}),
            'horas_contrato': forms.NumberInput(attrs={'class': 'form-control'}),
        }
