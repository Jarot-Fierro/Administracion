from django import forms


class CalidadJuridicaFilterForm(forms.Form):
    id = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'ID...'
            }
        )
    )
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Nombre...'
            }
        )
    )
    codigo = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Código...'
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
