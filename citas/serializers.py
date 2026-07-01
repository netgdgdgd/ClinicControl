from rest_framework import serializers
from django.utils import timezone
from chat.models import SalaChat
from django.db import transaction
from datetime import datetime
from .models import Cita, AgendaMedico

class AgendarCitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = ['id', 'paciente', 'agenda', 'fecha_hora_timestamp', 'motivo', 'estado']
        read_only_fields = ['estado'] # El estado siempre inicia como 'Agendada'

    def validate(self, data):
        """
        Valida que la fecha y hora de la cita coincidan con la disponibilidad
        del médico en la clínica (día de semana y horario).
        """
        agenda = data.get('agenda')
        fecha_hora = data.get('fecha_hora_timestamp')
        
        if agenda and fecha_hora:
            # Obtener el día de la semana (0=Domingo, 6=Sábado)
            dia_semana = fecha_hora.weekday()
            # Python: 0=Lunes, 6=Domingo; Django: 0=Domingo, 6=Sábado
            # Convertir: Python -> Django
            dia_semana_django = (dia_semana + 1) % 7
            
            # Verificar que el día de semana coincida
            if agenda.dia_semana != dia_semana_django:
                dias_semana_nombres = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
                raise serializers.ValidationError(
                    f"El médico no tiene disponibilidad en {dias_semana_nombres[dia_semana_django]}. "
                    f"Su disponibilidad es el {dias_semana_nombres[agenda.dia_semana]}."
                )
            
            # Verificar que la hora de inicio esté dentro del rango
            hora_cita = fecha_hora.time()
            if not (agenda.hora_inicio <= hora_cita < agenda.hora_fin):
                raise serializers.ValidationError(
                    f"La hora de la cita ({hora_cita.strftime('%H:%M')}) debe estar dentro del horario "
                    f"de disponibilidad ({agenda.hora_inicio.strftime('%H:%M')} - {agenda.hora_fin.strftime('%H:%M')})."
                )
        
        return data

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
        fields = ['id', 'paciente', 'agenda', 'fecha_hora_timestamp', 'motivo', 'estado']
        # El paciente será el usuario logueado automáticamente (lo manejamos en la view)
        read_only_fields = ['paciente', 'estado'] 

    def validate_fecha_hora(self, value):
        # Aquí podrías agregar lógica para no permitir citas en el pasado
        if value < timezone.now():
            raise serializers.ValidationError("No puedes agendar una cita en el pasado.")
        return value
