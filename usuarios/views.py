from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from rest_framework import status, generics, permissions
from django.contrib import messages
from .serializers import RegistroPacienteSerializer, RegistroMedicoSerializer, UsuarioReadSerializer
from .models import CustomUser
from .forms import RegistroPacienteForm, RegistroMedicoForm

def inicio_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def registro_paciente_web(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroPacienteForm(request.POST)
        if form.is_valid():
            # Guardamos y autenticamos automáticamente
            created_user = form.save()
            raw_password = form.cleaned_data.get('password')
            auth_user = authenticate(request, username=created_user.username, password=raw_password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, f'Paciente registrado y logueado correctamente. Tu nombre de usuario es: {created_user.username}')
                return redirect('dashboard')
            messages.success(request, f'Paciente registrado correctamente. Tu nombre de usuario es: {created_user.username}. Por favor inicia sesión.')
            return redirect('registro-paciente-web')
    else:
        form = RegistroPacienteForm()

    return render(request, 'usuarios/registro_paciente.html', {'form': form})

def registro_medico_web(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroMedicoForm(request.POST)
        if form.is_valid():
            created_user = form.save()
            raw_password = form.cleaned_data.get('password')
            auth_user = authenticate(request, username=created_user.username, password=raw_password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, f'Médico registrado y logueado correctamente. Tu nombre de usuario es: {created_user.username}')
                return redirect('dashboard')
            messages.success(request, f'Médico registrado correctamente. Tu nombre de usuario es: {created_user.username}. Por favor inicia sesión.')
            return redirect('registro-medico-web')
    else:
        form = RegistroMedicoForm()

    return render(request, 'usuarios/registro_medico.html', {'form': form})

class RegistroPacienteView(APIView):
    """
    Endpoint para el autoregistro de Pacientes en la plataforma.
    Genera automáticamente las credenciales de Usuario asociadas con el formato 'nombre1_apellido1'.
    Acceso público para permitir el registro de nuevos pacientes.
    """
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post', 'options']
    
    @extend_schema(
        request=RegistroPacienteSerializer,
        responses={201: RegistroPacienteSerializer},
        description="Recibe los datos personales del paciente, genera el username automáticamente y crea el registro transaccional uniendo las tablas USUARIOS y PACIENTES."
    )
    def post(self, request):
        serializer = RegistroPacienteSerializer(data=request.data)

        if serializer.is_valid():
            # El método .save() dispara la función create() que configuramos en el Serializer
            serializer.save()

            return Response(
                {"mensaje": "Paciente registrado exitosamente de forma transaccional."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistroMedicoView(APIView):
    """
    Endpoint para dar de alta al personal Médico en el sistema.
    Genera credenciales y enlaza la cédula profesional de forma segura.
    Acceso público para permitir el registro de nuevos médicos.
    """
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post', 'options']
    
    @extend_schema(
        request=RegistroMedicoSerializer,
        responses={201: RegistroMedicoSerializer},
        description="Recibe los datos profesionales, genera el username y crea el registro transaccional uniendo las tablas USUARIOS y MEDICOS."
    )
    def post(self, request):
        serializer = RegistroMedicoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"mensaje": "Médico registrado exitosamente en el sistema."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetalleUsuarioView(generics.RetrieveAPIView):
    """
    Endpoint para obtener los datos básicos del usuario logueado.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UsuarioReadSerializer

    # Seguridad: Solo usuarios que hayan iniciado sesión pueden ver los perfiles.
    permission_classes = [permissions.IsAuthenticated]
