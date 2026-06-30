from usuarios.models import MultiClaseAuditoriaBase
from django.conf import settings
from django.db import models

class Clinica(MultiClaseAuditoriaBase):
    """
    Entidades de infraestructura médica donde consultan los doctores.
    """
    nombre = models.CharField(max_length=150)
    calle = models.CharField(max_length=100)
    num_ext = models.CharField(max_length=20)
    num_int = models.CharField(max_length=20, null=True, blank=True)
    colonia = models.CharField(max_length=100)
    alcaldia = models.CharField(max_length=100)
    estado_ciudad = models.CharField(max_length=100)
    cp = models.CharField(max_length=10)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()

    class Meta:
        db_table = 'CLINICAS'
        verbose_name = 'Clínica'
        verbose_name_plural = 'Clínicas'

    def __str__(self):
        return self.nombre


class Paciente(MultiClaseAuditoriaBase):
    """
    Perfil clínico y datos personales del Paciente.
    Vinculado 1:1 con las credenciales de la app Usuarios.
    """
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_paciente'
    )
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    num_telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacim = models.DateField()
    curp = models.CharField(max_length=18, unique=True)
    calle = models.CharField(max_length=100)
    num_ext = models.CharField(max_length=20)
    num_int = models.CharField(max_length=20, null=True, blank=True)
    colonia = models.CharField(max_length=100)
    alcaldia = models.CharField(max_length=100)
    estado_ciudad = models.CharField(max_length=100)
    cp = models.CharField(max_length=10)
    nss = models.CharField(max_length=20, unique=True, null=True, blank=True)
    tipo_sangre = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        db_table = 'PACIENTES'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Medico(MultiClaseAuditoriaBase):
    """
    Perfil profesional del Médico.
    Vinculado 1:1 con las credenciales de la app Usuarios.
    """
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_medico'
    )
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    num_telefono = models.CharField(max_length=20, null=True, blank=True)
    cedula_profesional = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'MEDICOS'
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'

    def __str__(self):
        return f"Dr(a). {self.nombres} {self.apellidos}"

# ==========================================
# CATÁLOGOS DEL NÚCLEO
# ==========================================

class Especialidad(MultiClaseAuditoriaBase):
    nombre_especialidad = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'ESPECIALIDADES'
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'

    def __str__(self):
        return self.nombre_especialidad


class Padecimiento(MultiClaseAuditoriaBase):
    nombre_padecimiento = models.CharField(max_length=150, unique=True)

    class Meta:
        db_table = 'PADECIMIENTOS'
        verbose_name = 'Padecimiento'
        verbose_name_plural = 'Padecimientos'

    def __str__(self):
        return self.nombre_padecimiento


class LaboratorioClinico(MultiClaseAuditoriaBase):
    nombre = models.CharField(max_length=150)
    calle = models.CharField(max_length=100)
    num_ext = models.CharField(max_length=20)
    colonia = models.CharField(max_length=100)
    alcaldia = models.CharField(max_length=100)
    estado_ciudad = models.CharField(max_length=100)
    cp = models.CharField(max_length=10)

    class Meta:
        db_table = 'LABORATORIOS_CLINICOS'
        verbose_name = 'Laboratorio Clínico'
        verbose_name_plural = 'Laboratorios Clínicos'

    def __str__(self):
        return self.nombre

# ==========================================
# TABLAS INTERMEDIAS (M:N) - SIN AUDITORÍA
# ==========================================

class MedicoEspecialidad(models.Model):
    """Resuelve la relación Muchos a Muchos entre Médico y Especialidad"""
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='especialidades')
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='medicos')

    class Meta:
        db_table = 'MEDICO_ESPECIALIDAD'
        # Emula la llave primaria compuesta a nivel base de datos
        unique_together = (('medico', 'especialidad'),)
        verbose_name = 'Especialidad de Médico'
        verbose_name_plural = 'Especialidades de Médicos'


class PacientePadecimiento(models.Model):
    """Resuelve la relación Muchos a Muchos entre Paciente y Padecimiento"""
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='padecimientos')
    padecimiento = models.ForeignKey(Padecimiento, on_delete=models.CASCADE, related_name='pacientes')

    class Meta:
        db_table = 'PACIENTE_PADECIMIENTO'
        unique_together = (('paciente', 'padecimiento'),)
        verbose_name = 'Padecimiento de Paciente'
        verbose_name_plural = 'Padecimientos de Pacientes'
