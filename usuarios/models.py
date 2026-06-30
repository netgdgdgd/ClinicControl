from django.contrib.auth.models import AbstractUser
from django.db import models

class MultiClaseAuditoriaBase(models.Model):
    """
    Clase Abstracta para cumplir con SOLID (Single Responsibility).
    Centraliza el comportamiento de auditoría solicitado por el profesor.
    """
    estado_activo = models.BooleanField(
        default=True, 
        help_text="Indicador para el borrado lógico (Soft Delete)"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, 
        help_text="Fecha y hora de alta automatizada"
    )
    fecha_modif = models.DateTimeField(
        auto_now=True, 
        help_text="Fecha y hora de última modificación automatizada"
    )

    # Relaciones de auditoría apuntando al modelo de usuario personalizado.
    # El '%(class)s' dinámico evita colisiones de nombres en el ORM (related_name).
    usuario_creacion = models.ForeignKey(
        'usuarios.CustomUser', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_creados'
    )
    usuario_modif = models.ForeignKey(
        'usuarios.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_modificados'
    )

    class Meta:
        abstract = True  # Especifica que no creará una tabla física por sí sola


class CustomUser(AbstractUser, MultiClaseAuditoriaBase):
    """
    Modelo de Usuario Personalizado para la autenticación global.
    Hereda de AbstractUser para mantener la compatibilidad nativa con 'last_login'.
    """
    email = models.EmailField(
        unique=True, 
        error_messages={
            'unique': "Ya existe un usuario registrado con este correo electrónico.",
        }
    )
    is_medico = models.BooleanField(
        default=False,
        help_text="Define si el usuario tiene acceso al panel médico"
    )
    is_paciente = models.BooleanField(
        default=False,
        help_text="Define si el usuario tiene acceso al portal de pacientes"
    )

    # Configuración para que Django valide usando el email en lugar de exigirusername si se requiere a futuro,
    # aunque por ahora mantendremos el flujo estándar.
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'USUARIOS'  # Forzamos el nombre exacto de tu DDL para MariaDB
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    @classmethod
    def create_with_password(cls, *, username, email, password, **extra_fields):
        user = cls.objects.create_user(username=username, email=email, password=None, **extra_fields)
        user.set_password(password)
        user.save(update_fields=['password'])
        return user

    def __str__(self):
        return self.username
