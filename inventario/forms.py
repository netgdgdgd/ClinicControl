from django import forms


class BuscarMedicamentoForm(forms.Form):
    """
    Formulario para buscar medicamentos por nombre comercial o genérico.
    """
    busqueda = forms.CharField(
        label='Buscar Medicamento',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Busca por nombre comercial o nombre genérico...',
            'id': 'busqueda-medicamentos',
        })
    )
