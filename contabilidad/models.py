from django.db import models

# -----------------------------
# Choices
# -----------------------------
class Dia(models.IntegerChoices):
    LUNES = 1, "Lunes"
    MARTES = 2, "Martes"
    MIERCOLES = 3, "Miércoles"
    JUEVES = 4, "Jueves"
    VIERNES = 5, "Viernes"
    SABADO = 6, "Sábado"
    DOMINGO = 7, "Domingo"


class TipoFactura(models.TextChoices):
    COMPRA = "COMPRA", "Compra"
    VENTA = "VENTA", "Venta"
    DONACION = "DONACION", "Donación"
    AJUSTE_POSITIVO = "AJUSTE_POS", "Ajuste positivo (sobrante)"
    AJUSTE_NEGATIVO = "AJUSTE_NEG", "Ajuste negativo (faltante)"


class EstadoFactura(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"
    FINALIZADO = "FINALIZADO", "Finalizado"
    CANCELADO = "CANCELADO", "Cancelado"


class MetodoPago(models.TextChoices):
    EFECTIVO = "EFECTIVO", "Efectivo"
    TRANSFERENCIA = "TRANSFERENCIA", "Transferencia"
    OTRO = "OTRO", "Otro"


class EstadoPago(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"
    PAGADO = "PAGADO", "Pagado"
    ANULADO = "ANULADO", "Anulado"


class MetodoPagoEmpleado(models.TextChoices):
    EFECTIVO = "EFECTIVO", "Efectivo"
    TRANSFERENCIA = "TRANSFERENCIA", "Transferencia"
    OTRO = "OTRO", "Otro"


class EstadoEmpleado(models.TextChoices):
    ACTIVO = "ACT", "Activo"
    INACTIVO = "INA", "Inactivo"
    

# -----------------------------
# Modelos principales
# -----------------------------
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    documento = models.CharField(max_length=20, unique=True)
    estado = models.CharField(
        max_length=3,
        choices=EstadoEmpleado.choices,
        default=EstadoEmpleado.ACTIVO
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Contrato(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    fecha_contratacion = models.DateField()
    fecha_vencimiento = models.DateField(blank=True, null=True)
    fecha_baja = models.DateField(blank=True, null=True)
    pago_hora = models.DecimalField(max_digits=10, decimal_places=2)
    horas_totales = models.PositiveIntegerField()

    def __str__(self):
        return f"Contrato {self.empleado} - {self.departamento}"


class Turno(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    dia = models.IntegerField(choices=Dia.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.contrato.empleado} - {self.get_dia_display()} {self.hora_inicio}-{self.hora_fin}"


class Asistencia(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.SET_NULL, null=True, blank=True)
    hora_entrada = models.DateTimeField()
    hora_salida = models.DateTimeField(blank=True, null=True)
    tiempo_total = models.DurationField(blank=True, null=True)
    motivo_entrada = models.CharField(max_length=100, blank=True, null=True)
    motivo_salida = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.hora_entrada and self.hora_salida:
            self.tiempo_total = self.hora_salida - self.hora_entrada
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Asistencia {self.empleado} - {self.hora_entrada.date()}"


class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    cuit = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)


class Factura(models.Model):
    tipo = models.CharField(max_length=10, choices=TipoFactura.choices)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    numero = models.CharField(max_length=50, unique=True)
    empleado = models.ForeignKey("Empleado", on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=10, choices=EstadoFactura.choices)
    metodo_pago = models.CharField(max_length=15, choices=MetodoPago.choices)

    def __str__(self):
        return f"Factura {self.numero} ({self.tipo}) - {self.total}"


class FacturaLinea(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="lineas")
    nombre = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def __str__(self):
        return f"{self.nombre} ({self.cantidad} x {self.precio_unitario})"
    

class PagoEmpleado(models.Model):
    contrato = models.ForeignKey("Contrato", on_delete=models.CASCADE)
    periodo_mes = models.PositiveSmallIntegerField()
    periodo_anio = models.PositiveSmallIntegerField()
    fecha_pago = models.DateField()
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago = models.CharField(max_length=15, choices=MetodoPagoEmpleado.choices)
    estado = models.CharField(max_length=10, choices=EstadoPago.choices, default=EstadoPago.PENDIENTE)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pago {self.contrato.empleado} - {self.periodo_mes}/{self.periodo_anio} - {self.estado}"