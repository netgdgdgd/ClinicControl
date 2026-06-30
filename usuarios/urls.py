from django.urls import path
from .views import (
    DetalleUsuarioView,
    registro_medico_web,
    registro_paciente_web,
)

urlpatterns = [
    # Formularios públicos de registro
    path('registro/paciente/formulario/', registro_paciente_web, name='registro-paciente-web'),
    path('registro/medico/formulario/', registro_medico_web, name='registro-medico-web'),

    # Endpoint de Perfil (Privado)
    path('perfil/<int:pk>/', DetalleUsuarioView.as_view(), name='detalle-usuario'),
]
