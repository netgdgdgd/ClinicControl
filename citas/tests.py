from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from citas.models import AgendaMedico, Cita
from nucleo.models import Clinica, Medico, Paciente
from usuarios.models import CustomUser


class AgendaMedicaViewTests(TestCase):
    def test_doctor_sees_only_his_citas(self):
        doctor_user = CustomUser.objects.create_user(
            username='doctor1',
            email='doctor1@example.com',
            password='secret123',
            is_medico=True,
        )
        doctor_profile = Medico.objects.create(
            usuario=doctor_user,
            nombres='Ana',
            apellidos='López',
            cedula_profesional='MED001',
        )

        patient_user = CustomUser.objects.create_user(
            username='paciente1',
            email='paciente1@example.com',
            password='secret123',
            is_paciente=True,
        )
        patient_profile = Paciente.objects.create(
            usuario=patient_user,
            nombres='Luis',
            apellidos='Pérez',
            fecha_nacim=timezone.now().date(),
            curp='ABC123456789012',
            calle='Calle 1',
            num_ext='1',
            colonia='Centro',
            alcaldia='Álvaro Obregón',
            estado_ciudad='CDMX',
            cp='01000',
        )

        clinica = Clinica.objects.create(
            nombre='Clínica Test',
            calle='Calle 2',
            num_ext='2',
            num_int='3',
            colonia='Centro',
            alcaldia='Álvaro Obregón',
            estado_ciudad='CDMX',
            cp='01000',
            hora_apertura='08:00:00',
            hora_cierre='20:00:00',
        )
        agenda = AgendaMedico.objects.create(
            medico=doctor_profile,
            clinica=clinica,
            dia_semana=1,
            hora_inicio='08:00:00',
            hora_fin='09:00:00',
        )
        cita = Cita.objects.create(
            paciente=patient_profile,
            agenda=agenda,
            fecha_hora_timestamp=timezone.now() + timedelta(days=1),
            motivo='Consulta general',
            estado='Agendada',
        )

        self.client.force_login(doctor_user)
        response = self.client.get(reverse('agenda-medica'))

        self.assertEqual(response.status_code, 200)
        self.assertIn(cita, response.context['citas'])
