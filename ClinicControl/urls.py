from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path

# Importar las vistas
from usuarios.views import (
    DetalleUsuarioView,
    RegistroPacienteView,
    RegistroMedicoView,
    inicio_view,
)
from citas.views import AgendarCitaView
from nucleo.views import dashboard_view

urlpatterns = [
    # Panel de Administración
    path('admin/', admin.site.urls),

    path('', inicio_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # ----------------------------------------------------
    # ENDPOINTS DE LA APLICACIÓN (APIs)
    # ----------------------------------------------------
    # Módulo de Usuarios
    path('api/usuarios/registro-paciente/', RegistroPacienteView.as_view(), name='registro-paciente'),
    path('api/usuarios/registro-medico/', RegistroMedicoView.as_view(), name='registro-medico'),

    # Módulo de Citas y Operación
    path('api/citas/agendar/', AgendarCitaView.as_view(), name='agendar-cita'),

    # ----------------------------------------------------
    # SWAGGER & OPENAPI 3 (Documentación Automática)
    # ----------------------------------------------------
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/login/', obtain_auth_token, name='api-login'),

    path('inventario/', include('inventario.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('citas/', include('citas.urls')),
    path('chat/', include('chat.urls')),
]
