from django.contrib import admin
from .models import Sala, Reserva


@admin.register(Sala)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_sala', 'capacidad_max', 'disponibilidad')
    list_filter = ("disponibilidad",)

@admin.register(Reserva)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('rut', 'fecha_hora_inicio','fecha_hora_termino', 'sala_reservada' )
    list_filter = ("sala_reservada", )