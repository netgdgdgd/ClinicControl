from usuarios.models import MultiClaseAuditoriaBase
from django.db import models

class FabricanteMedicamento(MultiClaseAuditoriaBase):
    nombre = models.CharField(max_length=150)
    num_telefono_contacto = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'FABRICANTES_MEDICAMENTOS'
        verbose_name = 'Fabricante de Medicamento'
        verbose_name_plural = 'Fabricantes de Medicamentos'

    def __str__(self):
        return self.nombre

class Farmacia(MultiClaseAuditoriaBase):
    nombre = models.CharField(max_length=150)
    calle = models.CharField(max_length=100)
    num_ext = models.CharField(max_length=20)
    colonia = models.CharField(max_length=100)
    alcaldia = models.CharField(max_length=100)
    estado_ciudad = models.CharField(max_length=100)
    cp = models.CharField(max_length=10)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    num_telefono = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'FARMACIAS'
        verbose_name = 'Farmacia'
        verbose_name_plural = 'Farmacias'

    @property
    def direccion(self):
        """
        Devuelve la dirección completa de la farmacia en un solo string.
        """
        return f"{self.calle} {self.num_ext}, {self.colonia}, {self.alcaldia}, {self.estado_ciudad}, C.P. {self.cp}"

    def __str__(self):
        return f"Farmacia {self.nombre} ({self.colonia})"


class Medicamento(MultiClaseAuditoriaBase):
    fabricante = models.ForeignKey(FabricanteMedicamento, on_delete=models.RESTRICT, related_name='medicamentos')
    nombre_generico = models.CharField(max_length=150)
    nombre_comercial = models.CharField(max_length=150, null=True, blank=True)
    contenido_neto = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'MEDICAMENTOS'
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'

    def __str__(self):
        nombre = self.nombre_comercial if self.nombre_comercial else self.nombre_generico
        return f"{nombre} - {self.contenido_neto}"


class Inventario(models.Model):
    """
    Tabla intermedia transaccional (M:N) que registra existencias físicas.
    No requiere campos de auditoría estándar por ser de alto volumen de escritura.
    """
    farmacia = models.ForeignKey(Farmacia, on_delete=models.CASCADE, related_name='inventarios')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='inventarios')
    
    # Validamos que el stock jamás sea negativo directo en el modelo
    stock_actual = models.PositiveIntegerField(default=0)
    # Decimal de 10 dígitos y 2 decimales para la moneda
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'INVENTARIOS'
        # Llave primaria compuesta lógica
        unique_together = (('farmacia', 'medicamento'),)
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self):
        return f"{self.medicamento} en {self.farmacia}: {self.stock_actual} pzas"
