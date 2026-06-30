from usuarios.models import MultiClaseAuditoriaBase
from django.db import models

class AgendaMedico(MultiClaseAuditoriaBase):
    """
    Bloques de disponibilidad del médico en una clínica específica.
    """
    DIAS_SEMANA = (
        (0, 'Domingo'),
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miércoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
    )
    medico = models.ForeignKey('nucleo.Medico', on_delete=models.CASCADE, related_name='agendas')
    clinica = models.ForeignKey('nucleo.Clinica', on_delete=models.CASCADE, related_name='agendas')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        db_table = 'AGENDA_MEDICOS'
        verbose_name = 'Agenda Médica'
        verbose_name_plural = 'Agendas Médicas'

    def __str__(self):
        return f"Agenda {self.medico} - Día {self.dia_semana}"


class Cita(MultiClaseAuditoriaBase):
    """
    Registro del encuentro médico. 
    (La lógica de negocio asume que dura 1 hora a partir del fecha_hora_timestamp)
    """
    ESTADOS = (
        ('Agendada', 'Agendada'),
        ('Cancelada', 'Cancelada'),
        ('Atendida', 'Atendida'),
    )
    paciente = models.ForeignKey('nucleo.Paciente', on_delete=models.CASCADE, related_name='citas')
    agenda = models.ForeignKey(AgendaMedico, on_delete=models.RESTRICT, related_name='citas')
    fecha_hora_timestamp = models.DateTimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Agendada')

    class Meta:
        db_table = 'CITAS'
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

    def __str__(self):
        return f"Cita: {self.paciente} - {self.fecha_hora_timestamp}"


class Receta(MultiClaseAuditoriaBase):
    """
    Documento médico legal derivado de una Cita.
    """
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE, related_name='receta')
    fecha_emision = models.DateField()
    indicaciones_generales = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'RECETAS'
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'

    def __str__(self):
        return f"Receta de Cita #{self.cita.id}"


class RecetaMedicamento(models.Model):
    """
    Tabla intermedia M:N (Detalle de la Receta).
    Hereda de models.Model (SIN auditoría para no sobrecargar la BD).
    """
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='detalles_medicamentos')
    # Apuntamos a la app de inventario (que crearemos en el siguiente paso)
    medicamento = models.ForeignKey('inventario.Medicamento', on_delete=models.RESTRICT)
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    duracion_dias = models.PositiveIntegerField()

    class Meta:
        db_table = 'RECETA_MEDICAMENTO'
        verbose_name = 'Detalle de Receta'
        verbose_name_plural = 'Detalles de Recetas'
        # Llave primaria compuesta
        unique_together = (('receta', 'medicamento'),)

    def __str__(self):
        return f"{self.medicamento} - {self.dosis}"


class SolicitudEstudio(MultiClaseAuditoriaBase):
    """
    Orden de estudios clínicos derivada de la cita.
    """
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='estudios')
    # Apuntamos al laboratorio (asumiendo que vivirá en la app núcleo o inventario, aquí uso núcleo)
    laboratorio_clinico = models.ForeignKey('nucleo.LaboratorioClinico', on_delete=models.RESTRICT)
    tipo_estudio = models.CharField(max_length=150)
    indicaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'SOLICITUDES_ESTUDIO'
        verbose_name = 'Solicitud de Estudio'
        verbose_name_plural = 'Solicitudes de Estudio'

    def __str__(self):
        return f"Estudio: {self.tipo_estudio} (Cita #{self.cita.id})"
