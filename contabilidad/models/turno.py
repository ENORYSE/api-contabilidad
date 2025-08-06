from django.db import models
from datetime import date

class Turno(models.Model):
    nombre = models.CharField(max_length=100)
    empleado = models.ForeignKey('Empleado', related_name='turnos', on_delete=models.CASCADE)
    jornada = models.ForeignKey('Jornada', related_name='turnos', on_delete=models.CASCADE)
    horarios = models.ManyToManyField('Horario', related_name='turnos')
    fecha_inicio = models.DateField(default=date.today)
    fecha_fin = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.nombre} - {self.empleado.nombre} ({self.jornada.departamento.titulo})"