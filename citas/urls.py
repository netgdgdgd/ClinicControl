from django.urls import path
from .views import AgendarCitaPageView, AgendaMedicaView, AgendarCitaView, ListarCitasView, DetalleCitaView

urlpatterns = [
    path('agendar/', AgendarCitaPageView.as_view(), name='agendar-cita-page'),
    path('agenda/', AgendaMedicaView.as_view(), name='agenda-medica'),
    path('listar/', ListarCitasView.as_view(), name='listar-citas'),
    path('<int:cita_id>/', DetalleCitaView.as_view(), name='detalle-cita'),
]
