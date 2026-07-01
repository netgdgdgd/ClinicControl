from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status, generics, permissions
from nucleo.models import Medico, Paciente, LaboratorioClinico, PacientePadecimiento
from .serializers import AgendarCitaSerializer, CitaSerializer
from django.views import View
from datetime import time
from .models import Cita, AgendaMedico, Receta, RecetaMedicamento, SolicitudEstudio
from .forms import AgendaMedicoForm, RecetaForm, RecetaMedicamentoForm, PacientePadecimientoForm, SolicitudEstudioForm

class AgendarCitaPageView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_paciente:
            medicos = Medico.objects.all()
            return render(request, 'citas/agendar.html', {'medicos': medicos})
        elif request.user.is_medico:
            pacientes = Paciente.objects.all()
            return render(request, 'citas/agendar.html', {'pacientes': pacientes})

class AgendaMedicaView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        citas = Cita.objects.none()
        agendas = AgendaMedico.objects.none()
        form = None
        
        if getattr(user, 'is_medico', False):
            medico = getattr(user, 'perfil_medico', None)
            if medico is not None:
                citas = Cita.objects.filter(agenda__medico=medico)
                agendas = AgendaMedico.objects.filter(medico=medico)
                form = AgendaMedicoForm()
        elif getattr(user, 'is_paciente', False):
            paciente = getattr(user, 'perfil_paciente', None)
            if paciente is not None:
                citas = Cita.objects.filter(paciente=paciente)
        
        context = {
            'citas': citas,
            'agendas': agendas,
            'form': form,
        }
        return render(request, 'citas/agenda.html', context)
    
    def post(self, request):
        """
        Método POST para que el médico registre bloques de disponibilidad en su agenda.
        """
        user = request.user
        
        # Verificar que el usuario es médico
        if not getattr(user, 'is_medico', False):
            return render(request, 'citas/agenda.html', {
                'error': 'Solo los médicos pueden registrar disponibilidad.',
                'citas': Cita.objects.none(),
                'agendas': AgendaMedico.objects.none(),
                'form': AgendaMedicoForm(),
            })
        
        medico = getattr(user, 'perfil_medico', None)
        if medico is None:
            return render(request, 'citas/agenda.html', {
                'error': 'No se encontró el perfil de médico asociado.',
                'citas': Cita.objects.none(),
                'agendas': AgendaMedico.objects.none(),
                'form': AgendaMedicoForm(),
            })

        # Procesar el formulario
        form = AgendaMedicoForm(request.POST)
        if form.is_valid():
            # Crear la instancia pero no guardar aún
            agenda = form.save(commit=False)
            # Asignar el médico logueado
            agenda.medico = medico
            # Guardar en la base de datos
            agenda.save()
            
            # Redirigir o recargar la página con mensaje de éxito
            citas = Cita.objects.filter(agenda__medico=medico)
            agendas = AgendaMedico.objects.filter(medico=medico)
            return render(request, 'citas/agenda.html', {
                'citas': citas,
                'agendas': agendas,
                'form': AgendaMedicoForm(),
                'success': 'Bloque de disponibilidad registrado exitosamente.',
            })
        
        # Si el formulario no es válido, mostrar errores
        citas = Cita.objects.filter(agenda__medico=medico)
        agendas = AgendaMedico.objects.filter(medico=medico)
        return render(request, 'citas/agenda.html', {
            'citas': citas,
            'agendas': agendas,
            'form': form,
            'error': 'Error al registrar el bloque de disponibilidad. Revisa los datos.',
        })

class AgendarCitaView(APIView):
    """
    Endpoint principal para la creación de citas médicas.
    Al generarse exitosamente, el sistema despliega automáticamente una 
    Sala de Chat asociada para la comunicación Paciente-Médico vía ActiveMQ.
    
    Solo permite POST desde médicos autenticados.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CitaSerializer
    http_method_names = ['post', 'options']

    def perform_create(self, serializer):
        # Asignamos al paciente logueado 
        paciente = getattr(self.request.user, 'perfil_paciente', None)
        serializer.save(paciente=paciente)

    @extend_schema(
        request=AgendarCitaSerializer,
        responses={201: AgendarCitaSerializer},
        description="Registra una nueva cita médica y genera automáticamente su sala de mensajería (WebSockets/STOMP)."
    )
    def post(self, request):
        if not request.user.is_medico:
            return render(request, 'citas/partials/resultado_form.html', {'exito': False})

        data = request.data.copy()
        data['fecha_hora_timestamp'] = data.get('fecha_hora')  # Aseguramos que el campo fecha_hora_timestamp esté presente
        # Asignamos al usuario logueado automáticamente
        data['paciente'] = request.data.get('paciente')  # El médico debe especificar el paciente
        agenda_medico = AgendaMedico.objects.filter(medico=getattr(request.user, 'perfil_medico', None)).all()
        for agenda in agenda_medico:
            if agenda.hora_inicio <= time.fromisoformat(data.get('fecha_hora').split('T')[1]) < agenda.hora_fin:
                data['agenda'] = agenda.id
                break

        serializer = AgendarCitaSerializer(data=data)
        # print(serializer.initial_data)  # Para depuración
        # if not serializer.is_valid():
        #     print(serializer.errors)  # Para depuración
        #     #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #     return render(request, 'citas/partials/resultado_form.html', {'errores': serializer.errors})

        if serializer.is_valid():
            serializer.save()
            #return Response(
            #    {"mensaje": "Cita agendada exitosamente. Sala de chat inicializada."},
            #    status=status.HTTP_201_CREATED
            #)
            return render(request, 'citas/partials/resultado_form.html', {'exito': True})
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'citas/partials/resultado_form.html', {'errores': serializer.errors})


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


class DetalleCitaView(LoginRequiredMixin, View):
    """
    Vista para mostrar los detalles de una cita y permitir que el médico:
    - Crear una receta
    - Agregar medicamentos a la receta
    - Asignar padecimientos al paciente
    - Generar solicitudes de estudio
    """
    
    def get(self, request, cita_id):
        cita = get_object_or_404(Cita, id=cita_id)
        user = request.user
        print(f"Usuario logueado: {user}, es médico: {getattr(user, 'is_medico', False)}, es paciente: {getattr(user, 'is_paciente', False)}")  # Depuración
        
        # Verificar que solo el médico de la cita o el paciente pueden verla
        if getattr(user, 'is_medico', False):
            medico = getattr(user, 'perfil_medico', None)
            if cita.agenda.medico != medico:
                return render(request, 'citas/error.html', {
                    'error': 'No tienes permiso para acceder a esta cita.'
                })
        elif getattr(user, 'is_paciente', False):
            paciente = getattr(user, 'perfil_paciente', None)
            if cita.paciente != paciente:
                return render(request, 'citas/error.html', {
                    'error': 'No tienes permiso para acceder a esta cita.'
                })
        else:
            return render(request, 'citas/error.html', {
                'error': 'No tienes permiso para acceder a esta cita.'
            })
        
        # Obtener datos relacionados
        receta = getattr(cita, 'receta', None)
        medicamentos_receta = RecetaMedicamento.objects.filter(receta=receta) if receta else None
        padecimientos_paciente = PacientePadecimiento.objects.filter(paciente=cita.paciente).all()
        for padecimiento in padecimientos_paciente:
            print(f"Padecimiento del paciente: {padecimiento.padecimiento.nombre_padecimiento}")  # Depuración
        solicitudes_estudio = SolicitudEstudio.objects.filter(cita=cita.id).all()
        for estudio in solicitudes_estudio:
            print(f"Solicitud de estudio del paciente: {estudio.tipo_estudio}")  # Depuración
        
        # Preparar formularios solo si el usuario es médico
        context = {
            'cita': cita,
            'receta': receta,
            'medicamentos_receta': medicamentos_receta,
            'padecimientos_paciente': padecimientos_paciente,
            'solicitudes_estudio': solicitudes_estudio,
            'es_medico': getattr(user, 'is_medico', False),
        }
        
        if getattr(user, 'is_medico', False):
            if not receta:
                context['receta_form'] = RecetaForm()
            context['medicamento_form'] = RecetaMedicamentoForm()
            context['padecimiento_form'] = PacientePadecimientoForm()
            context['solicitud_estudio_form'] = SolicitudEstudioForm()
        
        return render(request, 'citas/detalle_cita.html', context)
    
    def post(self, request, cita_id):
        """
        Maneja múltiples tipos de POST según el formulario enviado.
        """
        cita = get_object_or_404(Cita, id=cita_id)
        user = request.user
        
        # Verificar que el usuario es médico
        if not getattr(user, 'is_medico', False):
            return render(request, 'citas/error.html', {
                'error': 'Solo los médicos pueden realizar esta acción.'
            })
        
        medico = getattr(user, 'perfil_medico', None)
        if cita.agenda.medico != medico:
            return render(request, 'citas/error.html', {
                'error': 'No tienes permiso para acceder a esta cita.'
            })
        
        # Determinar cuál formulario se envió según el botón presionado
        if 'crear_receta' in request.POST:
            return self._crear_receta(request, cita)
        elif 'agregar_medicamento' in request.POST:
            return self._agregar_medicamento(request, cita)
        elif 'asignar_padecimiento' in request.POST:
            return self._asignar_padecimiento(request, cita)
        elif 'crear_solicitud_estudio' in request.POST:
            return self._crear_solicitud_estudio(request, cita)
        
        # Si no se reconoce el formulario, redireccionar
        return redirect('detalle-cita', cita_id=cita.id)
    
    def _crear_receta(self, request, cita):
        """Crea una nueva receta para la cita."""
        if hasattr(cita, 'receta'):
            return self._redirect_with_error(request, cita, 'Esta cita ya tiene una receta registrada.')
        
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.cita = cita
            receta.save()
            return self._redirect_with_success(request, cita, 'Receta creada exitosamente.')
        
        return self._redirect_with_error(request, cita, 'Error al crear la receta.')
    
    def _agregar_medicamento(self, request, cita):
        """Agrega un medicamento a la receta."""
        if not hasattr(cita, 'receta'):
            return self._redirect_with_error(request, cita, 'Debe crear una receta primero.')
        
        form = RecetaMedicamentoForm(request.POST)
        if form.is_valid():
            medicamento_receta = form.save(commit=False)
            medicamento_receta.receta = cita.receta
            medicamento_receta.save()
            return self._redirect_with_success(request, cita, 'Medicamento agregado a la receta.')
        
        return self._redirect_with_error(request, cita, 'Error al agregar el medicamento.')
    
    def _asignar_padecimiento(self, request, cita):
        """Asigna un padecimiento al paciente."""
        form = PacientePadecimientoForm(request.POST)
        if form.is_valid():
            padecimiento = form.cleaned_data['padecimiento']
            # Verificar que el padecimiento no esté ya asignado
            if PacientePadecimiento.objects.filter(padecimiento=padecimiento.id, paciente=cita.paciente).exists():
                return self._redirect_with_error(request, cita, 'Este padecimiento ya está asignado al paciente.')
            
            padecimiento_paciente = form.save(commit=False)
            padecimiento_paciente.paciente = cita.paciente
            padecimiento_paciente.save()
            return self._redirect_with_success(request, cita, 'Padecimiento asignado exitosamente.')
        
        return self._redirect_with_error(request, cita, 'Error al asignar el padecimiento.')
    
    def _crear_solicitud_estudio(self, request, cita):
        """Crea una solicitud de estudio para la cita."""
        form = SolicitudEstudioForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.cita = cita
            solicitud.save()
            return self._redirect_with_success(request, cita, 'Solicitud de estudio creada exitosamente.')
        
        return self._redirect_with_error(request, cita, 'Error al crear la solicitud de estudio.')
    
    def _redirect_with_success(self, request, cita, message):
        """Redirige con mensaje de éxito."""
        request.session['success'] = message
        return redirect('detalle-cita', cita_id=cita.id)
    
    def _redirect_with_error(self, request, cita, message):
        """Redirige con mensaje de error."""
        request.session['error'] = message
        return redirect('detalle-cita', cita_id=cita.id)
