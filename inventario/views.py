from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import generics, permissions, serializers
from .serializers import MedicamentoSerializer, RecetaSerializer
from .models import Medicamento
from citas.models import Receta

# Inventario (Catálogo de medicamentos)
class InventarioHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/agregar_medicamento.html'

class MedicamentoListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer

# Recetas (Vinculadas a citas)
class RegistrarRecetaView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecetaSerializer
    queryset = Receta.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_medico:
            raise serializers.ValidationError("Solo los médicos pueden emitir recetas.")
        serializer.save()
