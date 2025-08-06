from django.db import models

class Jornada(models.Model):
    departamento = models.ForeignKey('Departamento', related_name='jornadas', on_delete=models.CASCADE)
    horas_mensuales = models.PositiveIntegerField()
    pago_por_hora = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_cobro = models.DateField()

    def __str__(self):
        return f"Jornada para {self.departamento.titulo} ({self.horas_mensuales} horas)"
    
    class Meta:
        verbose_name = 'Jornada Laboral'
        verbose_name_plural = 'Jornadas Laborales'