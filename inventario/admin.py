from .models import FabricanteMedicamento, Farmacia, Medicamento, Inventario
from django.contrib import admin

admin.site.register(FabricanteMedicamento)
admin.site.register(Medicamento)
admin.site.register(Inventario)
admin.site.register(Farmacia)
