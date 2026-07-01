from django.urls import path
from .views import (
    ClinicasListView,
    FarmaciasListView,
    LaboratoriosListView,
)

app_name = 'nucleo'

urlpatterns = [
    path('clinicas/', ClinicasListView.as_view(), name='clinicas-list'),
    path('farmacias/', FarmaciasListView.as_view(), name='farmacias-list'),
    path('laboratorios/', LaboratoriosListView.as_view(), name='laboratorios-list'),
]
