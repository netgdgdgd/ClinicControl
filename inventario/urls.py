from django.urls import path
from .views import InventarioHomeView, MedicamentoListView, RegistrarRecetaView, CatalogoFarmaciasView

urlpatterns = [
    #path('', InventarioHomeView.as_view(), name='inventario-home'),
    path('catalogo/', CatalogoFarmaciasView.as_view(), name='catalogo-farmacias'),
    path('medicamentos/', MedicamentoListView.as_view(), name='medicamento-list'),
    path('recetas/crear/', RegistrarRecetaView.as_view(), name='receta-crear'),
]
