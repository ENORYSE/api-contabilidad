from django.contrib import admin
from .models import Empleado, Departamento, Proveedor, Contrato

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "usuario", "correo", "telefono", "documento", "estado")
    search_fields = ("nombre", "apellido", "usuario", "correo", "documento")
    list_filter = ("estado",)
    ordering = ("apellido", "nombre")

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cuit", "correo", "telefono", "direccion")
    search_fields = ("nombre", "cuit", "correo", "telefono", "direccion")
    ordering = ("nombre", )

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ("empleado__nombre", "empleado__apellido", "pago_hora", "fecha_contratacion", "fecha_vencimiento", "fecha_baja", "horas_totales")
    search_fields = ("empleado__nombre", "empleado__apellido", "pago_hora", "horas_totales")
    list_display = ("fecha_contratacion", "fecha_vencimiento", "fecha_baja")
    ordering = ("empleado__nombre", "empleado__apellido")