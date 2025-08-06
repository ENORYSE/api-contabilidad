from django.db import models

class Horario(models.Model):
    DIA_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miércoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sábado', 'Sábado'),
    ]

    DIA_ORDEN = {
        'lunes': 1,
        'martes': 2,
        'miércoles': 3,
        'jueves': 4,
        'viernes': 5,
        'sábado': 6,
        'domingo': 7,
    }

    dia = models.CharField(max_length=20, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    orden = models.IntegerField(editable=False)

    def save(self, *args, **kwargs):
        self.orden = self.DIA_ORDEN[self.dia]
        super(Horario, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.dia} ({self.hora_inicio} - {self.hora_fin})"