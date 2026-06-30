from .models import AgendaMedico, Cita, Receta, RecetaMedicamento, SolicitudEstudio
from django.contrib import admin

admin.site.register(RecetaMedicamento)
admin.site.register(SolicitudEstudio)
admin.site.register(AgendaMedico)
admin.site.register(Receta)
admin.site.register(Cita)
