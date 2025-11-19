from django.db import models
from datetime import timedelta
from django.utils import timezone


class Sala(models.Model):
    nombre_sala = models.CharField(max_length=100)
    capacidad_max = models.PositiveIntegerField()
    disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_sala
    
    @property
    def disponible_ahora(self):
        ahora = timezone.now()
        return not self.reservas.filter(fecha_hora_termino__gt=ahora).exists()

class Reserva(models.Model):
    rut = models.CharField(max_length=12)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_termino = models.DateTimeField()
    sala_reservada = models.ForeignKey(
        Sala,
        on_delete=models.CASCADE,
        related_name="reservas"
    )

    def save(self, *args, **kwargs):
        es_nueva = self.pk is None

        if es_nueva:
            if not self.fecha_hora_inicio:
                self.fecha_hora_inicio = timezone.now()
            if not self.fecha_hora_termino:
                self.fecha_hora_termino = self.fecha_hora_inicio + timedelta(hours=2)

        super().save(*args, **kwargs)
        
        if es_nueva:
            sala = self.sala_reservada
            if sala.disponibilidad:
                sala.disponibilidad = False
                sala.save()
    def delete(self, *args, **kwargs):
        sala = self.sala_reservada
        
        super().delete(*args, **kwargs)

        hay_reservas_activas = Reserva.objects.filter(
            sala_reservada=sala,
            fecha_hora_termino__gt=timezone.now()
        ).exists()

        if not hay_reservas_activas:
            sala.disponibilidad = True
            sala.save()
            
    def __str__(self):
        return f"Reserva {self.rut} {self.sala_reservada.nombre_sala}"
