from django import forms


class ComunaFilterForm(forms.Form):
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

    codigo = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Código...'
            }
        )
    )

    active = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Estado...'),
            ('true', 'Activos'),
            ('false', 'Inactivos'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-sm'
            }
        )
    )
