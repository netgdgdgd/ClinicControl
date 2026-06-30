from usuarios.models import MultiClaseAuditoriaBase
from django.conf import settings
from django.db import models

class SalaChat(MultiClaseAuditoriaBase):
    """
    Sala de conversación única generada a partir de una Cita agendada.
    """
    cita = models.OneToOneField(
        'citas.Cita', 
        on_delete=models.CASCADE, 
        related_name='sala_chat'
    )
    activa = models.BooleanField(
        default=True,
        help_text="Permite deshabilitar el chat cuando la cita concluye."
    )

    class Meta:
        db_table = 'SALAS_CHAT'
        verbose_name = 'Sala de Chat'
        verbose_name_plural = 'Salas de Chat'

    def __str__(self):
        return f"Chat de la Cita #{self.cita.id} - Activa: {self.activa}"


class Mensaje(models.Model):
    """
    Registro individual de mensajes en tiempo real.
    Diseñado para ser ligero en I/O.
    """
    sala = models.ForeignKey(
        SalaChat, 
        on_delete=models.CASCADE, 
        related_name='mensajes'
    )
    remitente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mensajes_enviados'
    )
    contenido = models.TextField()
    leido = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'MENSAJES'
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        # El ordenamiento por defecto garantiza que el frontend siempre 
        # reciba los mensajes en orden cronológico correcto.
        ordering = ['fecha_envio']

    def __str__(self):
        return f"Mensaje de {self.remitente} en {self.sala}"
