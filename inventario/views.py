from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics, permissions, serializers
from .serializers import MedicamentoSerializer, RecetaSerializer
from citas.models import Receta
from .models import Medicamento, Farmacia, Inventario
from .forms import BuscarMedicamentoForm

# Inventario (Catálogo de medicamentos)
class InventarioHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/catalogo_farmacias.html'

class CatalogoFarmaciasView(LoginRequiredMixin, View):
    """
    Vista que muestra un catálogo de medicamentos agrupados por farmacia.
    Permite búsqueda de medicamentos por nombre comercial o genérico.
    Accesible para médicos y pacientes.
    """
    def get(self, request):
        form = BuscarMedicamentoForm(request.GET or None)
        busqueda = request.GET.get('busqueda', '').strip()

        farmacias = Farmacia.objects.all()
        farmacias_con_medicamentos = {}
        for farmacia in farmacias:
            inventarios = Inventario.objects.filter(farmacia=farmacia).select_related('medicamento')
            if busqueda:
                inventarios = inventarios.filter(
                    Q(medicamento__nombre_comercial__icontains=busqueda) |
                    Q(medicamento__nombre_generico__icontains=busqueda)
                )
            if inventarios.exists():
                farmacias_con_medicamentos[farmacia] = inventarios

        context = {
            'form': form,
            'farmacias_con_medicamentos': farmacias_con_medicamentos,
            'busqueda': busqueda,
            'total_medicamentos': sum(len(invs) for invs in farmacias_con_medicamentos.values()),
        }

        # Si HTMX hace la petición, solo devolvemos lista de resultados
        if request.headers.get('HX-Request'):
            return render(request, 'inventario/partials/resultados_catalogo.html', context)

        # Si es una carga normal del navegador, devolvemos la página completa
        return render(request, 'inventario/catalogo_farmacias.html', context)

class MedicamentoListView(generics.ListAPIView):
    """
    Vista pública para listar todos los medicamentos disponibles.
    Solo permite acceso de lectura sin autenticación.
    """
    permission_classes = [permissions.AllowAny]
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    http_method_names = ['get', 'head', 'options']

# Recetas (Vinculadas a citas)
class RegistrarRecetaView(generics.CreateAPIView):
    """
    Endpoint para crear recetas médicas.
    Solo permite POST desde médicos autenticados.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecetaSerializer
    queryset = Receta.objects.all()
    http_method_names = ['post', 'options']

    def perform_create(self, serializer):
        if not self.request.user.is_medico:
            raise serializers.ValidationError("Solo los médicos pueden emitir recetas.")
        serializer.save()
