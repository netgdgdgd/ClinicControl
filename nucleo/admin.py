from .models import Clinica, Paciente, Medico, Especialidad, Padecimiento, LaboratorioClinico
from django.contrib import admin

admin.site.register(Clinica)
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Especialidad)
admin.site.register(Padecimiento)
admin.site.register(LaboratorioClinico)
