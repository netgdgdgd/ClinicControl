from rest_framework import serializers
from nucleo.models import Paciente, Medico
from django.db import transaction
from .models import CustomUser

class RegistroPacienteSerializer(serializers.ModelSerializer):
    # Declaramos los campos del perfil del paciente
    nombres = serializers.CharField(max_length=150, write_only=True)
    apellidos = serializers.CharField(max_length=150, write_only=True)
    fecha_nacim = serializers.DateField(write_only=True)
    curp = serializers.CharField(max_length=18, write_only=True)
    calle = serializers.CharField(max_length=100, write_only=True)
    num_ext = serializers.CharField(max_length=20, write_only=True)
    num_int = serializers.CharField(max_length=20, required=False, allow_null=True, write_only=True)

    colonia = serializers.CharField(max_length=100, write_only=True) 

    alcaldia = serializers.CharField(max_length=100, write_only=True)
    estado_ciudad = serializers.CharField(max_length=100, write_only=True)
    cp = serializers.CharField(max_length=10, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'password', 'nombres', 'apellidos', 'fecha_nacim', 
            'curp', 'calle', 'num_ext', 'num_int', 'colonia', 'alcaldia', 
            'estado_ciudad', 'cp'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # 1. Extraemos los campos exclusivos del perfil del Paciente
        nombres = validated_data.pop('nombres')
        apellidos = validated_data.pop('apellidos')
        fecha_nacim = validated_data.pop('fecha_nacim')
        curp = validated_data.pop('curp')
        calle = validated_data.pop('calle')
        num_ext = validated_data.pop('num_ext')
        num_int = validated_data.get('num_int', None)
        colonia = validated_data.pop('colonia')
        alcaldia = validated_data.pop('alcaldia')
        estado_ciudad = validated_data.pop('estado_ciudad')
        cp = validated_data.pop('cp')

        # 2. Lógica de negocio: Generar el username automático (nombre1_apellido1)
        # Tomamos la primera palabra de nombres y la primera de apellidos en minúsculas
        primer_nombre = nombres.strip().split()[0].lower()
        primer_apellido = apellidos.strip().split()[0].lower()
        username_automatico = f"{primer_nombre}_{primer_apellido}"

        # Evitar duplicados simples agregando un validador o sufijo si es necesario, 
        # pero mantenemos la regla base solicitada.
        
        # 3. Bloque transaccional atómico (Principio ACID)
        # Si la creación del paciente falla, se deshace la creación del usuario automáticamente
        with transaction.atomic():
            user = CustomUser.create_with_password(
                username=username_automatico,
                email=validated_data['email'],
                password=validated_data['password'],
                is_paciente=True,
            )
            
            # Vinculamos el perfil del paciente con el usuario recién creado
            Paciente.objects.create(
                usuario=user,
                nombres=nombres,
                apellidos=apellidos,
                fecha_nacim=fecha_nacim,
                curp=curp,
                calle=calle,
                num_ext=num_ext,
                num_int=num_int,
                colonia=colonia,
                alcaldia=alcaldia,
                estado_ciudad=estado_ciudad,
                cp=cp
            )
            
        return user

class RegistroMedicoSerializer(serializers.ModelSerializer):
    nombres = serializers.CharField(max_length=150, write_only=True)
    apellidos = serializers.CharField(max_length=150, write_only=True)
    num_telefono = serializers.CharField(max_length=20, required=False, allow_null=True, write_only=True)
    cedula_profesional = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = CustomUser
        # Validado: Todos los declarados arriba están aquí abajo.
        fields = ['email', 'password', 'nombres', 'apellidos', 'num_telefono', 'cedula_profesional']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # 1. Extraemos los campos del perfil profesional
        nombres = validated_data.pop('nombres')
        apellidos = validated_data.pop('apellidos')
        num_telefono = validated_data.get('num_telefono', None)
        cedula_profesional = validated_data.pop('cedula_profesional')

        # 2. Generamos el username bajo el estándar de la clínica
        primer_nombre = nombres.strip().split()[0].lower()
        primer_apellido = apellidos.strip().split()[0].lower()
        username_automatico = f"{primer_nombre}_{primer_apellido}"

        # 3. Transacción ACID para asegurar consistencia
        with transaction.atomic():
            # Creamos el usuario base marcando la bandera is_medico
            user = CustomUser.create_with_password(
                username=username_automatico,
                email=validated_data['email'],
                password=validated_data['password'],
                is_medico=True,
            )
            
            # Vinculamos el perfil del médico
            Medico.objects.create(
                usuario=user,
                nombres=nombres,
                apellidos=apellidos,
                num_telefono=num_telefono,
                cedula_profesional=cedula_profesional
            )
            
        return user

class UsuarioReadSerializer(serializers.ModelSerializer):
    """
    Serializer de solo lectura para el perfil de usuario.
    Evita exponer hashes de contraseñas.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_medico', 'is_paciente']
