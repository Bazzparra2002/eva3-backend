from django.db import models
from datetime import timedelta
from django.utils import timezone

class Sala(models.Model):
    nombre_sala = models.CharField(max_length=100)
    capacidad_max = models.PositiveIntegerField()
    disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_sala


class Reserva(models.Model):
    rut = models.CharField(max_length=12)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_termino = models.DateTimeField()
    sala_reservada = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="reservas")

    def save(self, *args, **kwargs):
        if not self.pk:
            
            self.fecha_hora_inicio = timezone.now()
                    
            #calcula la duración
            self.fecha_hora_termino = self.fecha_hora_inicio + timedelta(hours=2)

            #cambia el estado de sala a ocupada
            self.sala_reservada.disponibilidad = False
            self.sala_reservada.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva {self.rut} {self.sala_reservada.nombre_sala}"
