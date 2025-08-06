from django.db import models

class Empleado(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=20, unique=True)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=8, choices=ESTADO_CHOICES, default='activo')
    nombre_usuario = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.nombre_usuario})"
    