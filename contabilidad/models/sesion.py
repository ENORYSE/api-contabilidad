from django.db import models

class Sesion(models.Model):
    turno = models.ForeignKey('Turno', related_name='sesiones', on_delete=models.CASCADE)
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    estado = models.CharField(
        max_length=20, 
        choices=[('Iniciada', 'Iniciada'), ('Terminada', 'Terminada'), ('Pendiente', 'Pendiente'), ('Cancelada', 'Cancelada')],
        default='Pendiente'
    )
    motivo_discrepancia = models.TextField(null=True, blank=True)
    reemplazo = models.ForeignKey('Empleado', related_name='sesiones_reemplazo', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Sesión de {self.turno.empleado.nombre} - {self.estado} ({self.hora_inicio} - {self.hora_fin})"