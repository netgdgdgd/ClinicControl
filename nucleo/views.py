from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from inventario.models import Farmacia
from django.shortcuts import render
from .models import Clinica, LaboratorioClinico

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

class ClinicasListView(LoginRequiredMixin, ListView):
    """
    Vista para listar todas las clínicas disponibles con detalles
    de nombre, horario de atención y ubicación.
    """
    model = Clinica
    template_name = 'nucleo/clinicas_list.html'
    context_object_name = 'clinicas'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Clínicas Disponibles'
        context['icono'] = 'fa-hospital'
        return context


class FarmaciasListView(LoginRequiredMixin, ListView):
    """
    Vista para listar todas las farmacias disponibles con detalles
    de nombre, horario de atención y ubicación.
    """
    model = Farmacia
    template_name = 'nucleo/farmacias_list.html'
    context_object_name = 'farmacias'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Farmacias Disponibles'
        context['icono'] = 'fa-pills'
        return context


class LaboratoriosListView(LoginRequiredMixin, ListView):
    """
    Vista para listar todos los laboratorios disponibles con detalles
    de nombre, horario de atención y ubicación.
    """
    model = LaboratorioClinico
    template_name = 'nucleo/laboratorios_list.html'
    context_object_name = 'laboratorios'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Laboratorios Clínicos'
        context['icono'] = 'fa-flask'
        return context
