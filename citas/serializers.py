from rest_framework import serializers
from django.utils import timezone
from chat.models import SalaChat
from django.db import transaction
from .models import Cita

class AgendarCitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = ['id', 'paciente', 'agenda', 'fecha_hora_timestamp', 'motivo', 'estado']
        read_only_fields = ['estado'] # El estado siempre inicia como 'Agendada'

    def create(self, validated_data):
        # Transacción ACID: O se crea la cita Y el chat, o no se crea nada.
        with transaction.atomic():
            # 1. Creamos la cita médica
            cita = Cita.objects.create(**validated_data)

            # 2. Automatización: Creamos la Sala de Chat inmediatamente
            SalaChat.objects.create(
                cita=cita,
                activa=True
            )
        return cita

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = ['id', 'paciente', 'medico', 'fecha_hora', 'motivo', 'estado']
        # El paciente será el usuario logueado automáticamente (lo manejamos en la view)
        read_only_fields = ['paciente', 'estado'] 

    def validate_fecha_hora(self, value):
        # Aquí podrías agregar lógica para no permitir citas en el pasado
        if value < timezone.now():
            raise serializers.ValidationError("No puedes agendar una cita en el pasado.")
        return value
