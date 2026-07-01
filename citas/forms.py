from .models import AgendaMedico, Receta, RecetaMedicamento, SolicitudEstudio
from nucleo.models import PacientePadecimiento
from django import forms
from django.utils import timezone


class AgendaMedicoForm(forms.ModelForm):
    """
    Formulario para que el médico registre bloques de disponibilidad en su agenda.
    """
    class Meta:
        model = AgendaMedico
        fields = ['dia_semana', 'hora_inicio', 'hora_fin', 'clinica']
        widgets = {
            'dia_semana': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'hora_inicio': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'required': True,
            }),
            'hora_fin': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'required': True,
            }),
            'clinica': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
        }
        labels = {
            'dia_semana': 'Día de la Semana',
            'hora_inicio': 'Hora de Inicio',
            'hora_fin': 'Hora de Finalización',
            'clinica': 'Clínica',
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        if hora_inicio and hora_fin:
            if hora_inicio >= hora_fin:
                raise forms.ValidationError(
                    "La hora de inicio debe ser anterior a la hora de finalización."
                )

        return cleaned_data


class RecetaForm(forms.ModelForm):
    """
    Formulario para que el médico cree una receta asociada a una cita.
    """
    class Meta:
        model = Receta
        fields = ['fecha_emision', 'indicaciones_generales']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True,
            }),
            'indicaciones_generales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Indicaciones generales para el paciente...',
            }),
        }
        labels = {
            'fecha_emision': 'Fecha de Emisión',
            'indicaciones_generales': 'Indicaciones Generales',
        }

    def clean_fecha_emision(self):
        fecha = self.cleaned_data.get('fecha_emision')
        if fecha and fecha > timezone.now().date():
            raise forms.ValidationError("La fecha no puede ser en el futuro.")
        return fecha


class RecetaMedicamentoForm(forms.ModelForm):
    """
    Formulario para agregar medicamentos a una receta.
    """
    class Meta:
        model = RecetaMedicamento
        fields = ['medicamento', 'dosis', 'frecuencia', 'duracion_dias']
        widgets = {
            'medicamento': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg',
                'required': True,
            }),
            'frecuencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cada 8 horas',
                'required': True,
            }),
            'duracion_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '1',
                'required': True,
            }),
        }
        labels = {
            'medicamento': 'Medicamento',
            'dosis': 'Dosis',
            'frecuencia': 'Frecuencia',
            'duracion_dias': 'Duración (días)',
        }


class PacientePadecimientoForm(forms.ModelForm):
    """
    Formulario para asignar padecimientos al paciente.
    """
    class Meta:
        model = PacientePadecimiento
        fields = ['padecimiento']
        widgets = {
            'padecimiento': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
        }
        labels = {
            'padecimiento': 'Padecimiento',
        }


class SolicitudEstudioForm(forms.ModelForm):
    """
    Formulario para generar una solicitud de estudios clínicos.
    """
    class Meta:
        model = SolicitudEstudio
        fields = ['laboratorio_clinico', 'tipo_estudio', 'indicaciones']
        widgets = {
            'laboratorio_clinico': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'tipo_estudio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Análisis de sangre, Radiografía, etc.',
                'required': True,
            }),
            'indicaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Indicaciones especiales para el laboratorio...',
            }),
        }
        labels = {
            'laboratorio_clinico': 'Laboratorio Clínico',
            'tipo_estudio': 'Tipo de Estudio',
            'indicaciones': 'Indicaciones',
        }
