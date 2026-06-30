from rest_framework import serializers
from .models import Medicamento
from citas.models import Receta

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ['id', 'nombre_generico', 'nombre_comercial', 'contenido_neto']

class RecetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receta
        fields = ['id', 'cita', 'fecha_emision', 'indicaciones_generales']
        read_only_fields = ['fecha_emision']
