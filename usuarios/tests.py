from django.test import TestCase

from usuarios.forms import RegistroPacienteForm, RegistroMedicoForm


class RegistroPacienteFormTests(TestCase):
    def test_rechaza_password_debil(self):
        form = RegistroPacienteForm(
            data={
                'email': 'paciente@example.com',
                'password': '123456',
                'password_confirm': '123456',
                'nombres': 'Juan',
                'apellidos': 'Pérez',
                'fecha_nacim': '1990-01-10',
                'curp': 'PEPJ900110HDFRZN09',
                'calle': 'Av. Principal',
                'num_ext': '10',
                'colonia': 'Centro',
                'alcaldia': 'Coyoacán',
                'estado_ciudad': 'CDMX',
                'cp': '04000',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_rechaza_passwords_distintas(self):
        form = RegistroPacienteForm(
            data={
                'email': 'paciente@example.com',
                'password': 'Clinica2024!',
                'password_confirm': 'Clinica2025!',
                'nombres': 'Juan',
                'apellidos': 'Pérez',
                'fecha_nacim': '1990-01-10',
                'curp': 'PEPJ900110HDFRZN09',
                'calle': 'Av. Principal',
                'num_ext': '10',
                'colonia': 'Centro',
                'alcaldia': 'Coyoacán',
                'estado_ciudad': 'CDMX',
                'cp': '04000',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('password_confirm', form.errors)

    def test_acepta_password_valido(self):
        form = RegistroPacienteForm(
            data={
                'email': 'paciente@example.com',
                'password': 'Clinica2024!',
                'password_confirm': 'Clinica2024!',
                'nombres': 'Juan',
                'apellidos': 'Pérez',
                'fecha_nacim': '1990-01-10',
                'curp': 'PEPJ900110HDFRZN09',
                'calle': 'Av. Principal',
                'num_ext': '10',
                'colonia': 'Centro',
                'alcaldia': 'Coyoacán',
                'estado_ciudad': 'CDMX',
                'cp': '04000',
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_guarda_password_hash_y_lo_verifica(self):
        form = RegistroPacienteForm(
            data={
                'email': 'paciente-hash@example.com',
                'password': '123contra',
                'password_confirm': '123contra',
                'nombres': 'Juan',
                'apellidos': 'Pérez',
                'fecha_nacim': '1990-01-10',
                'curp': 'PEPJ900110HDFRZN09',
                'calle': 'Av. Principal',
                'num_ext': '10',
                'colonia': 'Centro',
                'alcaldia': 'Coyoacán',
                'estado_ciudad': 'CDMX',
                'cp': '04000',
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertTrue(user.check_password('123contra'))
        self.assertNotEqual(user.password, '123contra')
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))


class RegistroMedicoFormTests(TestCase):
    def test_rechaza_password_debil(self):
        form = RegistroMedicoForm(
            data={
                'email': 'medico@example.com',
                'password': '123456',
                'password_confirm': '123456',
                'nombres': 'Ana',
                'apellidos': 'García',
                'num_telefono': '5551234567',
                'cedula_profesional': 'MED-001',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_acepta_password_valido(self):
        form = RegistroMedicoForm(
            data={
                'email': 'medico@example.com',
                'password': 'Clinica2024!',
                'password_confirm': 'Clinica2024!',
                'nombres': 'Ana',
                'apellidos': 'García',
                'num_telefono': '5551234567',
                'cedula_profesional': 'MED-001',
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_guarda_password_hash_y_lo_verifica(self):
        form = RegistroMedicoForm(
            data={
                'email': 'medico-hash@example.com',
                'password': '123contra',
                'password_confirm': '123contra',
                'nombres': 'Ana',
                'apellidos': 'García',
                'num_telefono': '5551234567',
                'cedula_profesional': 'MED-001',
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertTrue(user.check_password('123contra'))
        self.assertNotEqual(user.password, '123contra')
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))
