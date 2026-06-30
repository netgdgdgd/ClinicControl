from django.urls import path
from .views import AgendarCitaPageView, AgendaMedicaView, AgendarCitaView, ListarCitasView

urlpatterns = [
    path('agendar/', AgendarCitaPageView.as_view(), name='agendar-cita-page'),
    path('agenda/', AgendaMedicaView.as_view(), name='agenda-medica'),
    path('listar/', ListarCitasView.as_view(), name='listar-citas'),
]
