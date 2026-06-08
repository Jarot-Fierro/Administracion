from django import forms


class UsuarioFilterForm(forms.Form):
    id = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'ID...'
            }
        )
    )
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Username...'
            }
        )
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Email...'
            }
        )
    )
    is_active = forms.TypedChoiceField(
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
