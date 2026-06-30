from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.db import transaction

from nucleo.models import Paciente, Medico

User = get_user_model()


class RegistroPacienteForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    nombres = forms.CharField(label='Nombres', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellidos = forms.CharField(label='Apellidos', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fecha_nacim = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    curp = forms.CharField(label='CURP', max_length=18, widget=forms.TextInput(attrs={'class': 'form-control'}))
    calle = forms.CharField(label='Calle', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    num_ext = forms.CharField(label='Número exterior', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    num_int = forms.CharField(label='Número interior', max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    colonia = forms.CharField(label='Colonia', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    alcaldia = forms.CharField(label='Alcaldía', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    estado_ciudad = forms.CharField(label='Estado / Ciudad', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cp = forms.CharField(label='Código postal', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo electrónico.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            password_validation.validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Las contraseñas no coinciden.')

        return cleaned_data

    def save(self):
        data = self.cleaned_data
        nombres = data['nombres'].strip()
        apellidos = data['apellidos'].strip()

        primer_nombre = nombres.split()[0].lower()
        primer_apellido = apellidos.split()[0].lower()
        username = f'{primer_nombre}_{primer_apellido}'
        suffix = 2
        while User.objects.filter(username=username).exists():
            username = f'{primer_nombre}_{primer_apellido}{suffix}'
            suffix += 1

        with transaction.atomic():
            user = User.create_with_password(
                username=username,
                email=data['email'],
                password=data['password'],
                is_paciente=True,
            )
            Paciente.objects.create(
                usuario=user,
                nombres=nombres,
                apellidos=apellidos,
                fecha_nacim=data['fecha_nacim'],
                curp=data['curp'],
                calle=data['calle'],
                num_ext=data['num_ext'],
                num_int=data['num_int'] or None,
                colonia=data['colonia'],
                alcaldia=data['alcaldia'],
                estado_ciudad=data['estado_ciudad'],
                cp=data['cp'],
            )
        return user


class RegistroMedicoForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    nombres = forms.CharField(label='Nombres', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellidos = forms.CharField(label='Apellidos', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    num_telefono = forms.CharField(label='Teléfono', max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cedula_profesional = forms.CharField(label='Cédula profesional', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo electrónico.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            password_validation.validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Las contraseñas no coinciden.')

        return cleaned_data

    def save(self):
        data = self.cleaned_data
        nombres = data['nombres'].strip()
        apellidos = data['apellidos'].strip()

        primer_nombre = nombres.split()[0].lower()
        primer_apellido = apellidos.split()[0].lower()
        username = f'{primer_nombre}_{primer_apellido}'
        suffix = 2
        while User.objects.filter(username=username).exists():
            username = f'{primer_nombre}_{primer_apellido}{suffix}'
            suffix += 1

        with transaction.atomic():
            user = User.create_with_password(
                username=username,
                email=data['email'],
                password=data['password'],
                is_medico=True,
            )
            Medico.objects.create(
                usuario=user,
                nombres=nombres,
                apellidos=apellidos,
                num_telefono=data['num_telefono'] or None,
                cedula_profesional=data['cedula_profesional'],
            )
        return user
