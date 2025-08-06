from django.contrib import admin
from .models import Departamento, Horario, Jornada, Turno, Empleado, Sesion

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion_corta')

    def descripcion_corta(self, obj):
        longitud_maxima = 150
        return obj.descripcion[:longitud_maxima] + '...' if len(obj.descripcion) > longitud_maxima else obj.descripcion
    
    descripcion_corta.short_description = 'Descripción'

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'correo_electronico', 'estado', 'nombre_usuario')
    list_filter = ('estado',)
    search_fields = ('nombre', 'apellido', 'dni', 'correo_electronico', 'nombre_usuario')
    
    def correo_electronico(self, obj):
        return obj.correo_electronico
    correo_electronico.short_description = 'Correo electrónico'

    def nombre_usuario(self, obj):
        return obj.nombre_usuario
    nombre_usuario.short_description = 'Nombre de usuario'

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('dia', 'hora_inicio', 'hora_fin')
    
    list_filter = ('dia', 'hora_inicio', 'hora_fin')
    
    ordering = ('orden',)

class JornadaAdmin(admin.ModelAdmin):
    list_display = ('departamento', 'horas_mensuales', 'pago_por_hora', 'fecha_cobro')
    list_filter = ('departamento',)
    search_fields = ('departamento__titulo', 'horas_mensuales')
    
    # Agrupar en "grupos" los campos relacionados
    fieldsets = (
        (None, {
            'fields': ('departamento', 'horas_mensuales')
        }),
        ('Pagos', {
            'fields': ('pago_por_hora',)
        }),
        ('Fecha de cobro', {
            'fields': ('fecha_cobro',)
        }),
    )


admin.site.register(Jornada, JornadaAdmin)

admin.site.register(Turno)
admin.site.register(Sesion)