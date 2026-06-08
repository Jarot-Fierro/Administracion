from django import forms


class FuncionarioFilterForm(forms.Form):
    id = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'ID...'
            }
        )
    )
    rut = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'RUT...'
            }
        )
    )
    nombres = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Nombres...'
            }
        )
    )
    apellido_paterno = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Apellido P...'
            }
        )
    )
    active = forms.TypedChoiceField(
        required=False,
        choices=[
            ('', 'Estado...'),
            ('True', 'Activo'),
            ('False', 'Inactivo'),
        ],
        coerce=lambda x: x == 'True' if x in ['True', 'False'] else None,
        empty_value=None,
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-sm'
            }
        )
    )
