from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from .serializers import AgendarCitaSerializer, CitaSerializer
from .models import Cita
from nucleo.models import Medico

class AgendarCitaPageView(LoginRequiredMixin, View):
    def get(self, request):
        medicos = Medico.objects.all()
        return render(request, 'citas/agendar.html', {'medicos': medicos})

class AgendaMedicaView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        citas = Cita.objects.none()
        if getattr(user, 'is_medico', False):
            medico = getattr(user, 'perfil_medico', None)
            if medico is not None:
                citas = Cita.objects.filter(agenda__medico=medico)
        elif getattr(user, 'is_paciente', False):
            paciente = getattr(user, 'perfil_paciente', None)
            if paciente is not None:
                citas = Cita.objects.filter(paciente=paciente)
        return render(request, 'citas/agenda.html', {'citas': citas})


class AgendarCitaView(APIView):
    """
    Endpoint principal para la creación de citas médicas.
    Al generarse exitosamente, el sistema despliega automáticamente una 
    Sala de Chat asociada para la comunicación Paciente-Médico vía ActiveMQ.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CitaSerializer

    def perform_create(self, serializer):
        # Asignamos al paciente logueado automáticamente
        paciente = getattr(self.request.user, 'perfil_paciente', None)
        serializer.save(paciente=paciente)

    @extend_schema(
        request=AgendarCitaSerializer,
        responses={201: AgendarCitaSerializer},
        description="Registra una nueva cita médica y genera automáticamente su sala de mensajería (WebSockets/STOMP)."
    )
    def post(self, request):
        serializer = AgendarCitaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"mensaje": "Cita agendada exitosamente. Sala de chat inicializada."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarCitasView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CitaSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_medico', False):
            medico = getattr(user, 'perfil_medico', None)
            if medico is not None:
                return Cita.objects.filter(agenda__medico=medico)
        if getattr(user, 'is_paciente', False):
            paciente = getattr(user, 'perfil_paciente', None)
            if paciente is not None:
                return Cita.objects.filter(paciente=paciente)
        return Cita.objects.none()
