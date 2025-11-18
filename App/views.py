from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Sala, Reserva
from .forms import ReservaForm


def inicio(request):
    #marca las salas como disponibles si su reserva termina
    ahora = timezone.now()
    reservas_expiradas = Reserva.objects.filter(fecha_hora_termino__lt=ahora)

    for reserva in reservas_expiradas:
        reserva.sala_reservada.disponibilidad = True
        reserva.sala_reservada.save()

    salas = Sala.objects.all()
    return render(request, "inicio.html", {"salas": salas})


def detalle_sala(request, sala_id):   
    sala = get_object_or_404(Sala, id=sala_id)

    #sala disponible va permitir reservar
    if sala.disponibilidad:
        if request.method == "POST":
            form = ReservaForm(request.POST)
            if form.is_valid():
                reserva = form.save(commit=False)
                reserva.sala_reservada = sala
                reserva.save()
                return redirect("inicio")
        else:
            form = ReservaForm()

        return render(request, "detalle.html", {"sala": sala, "form": form})

    #si sala esta ocupada muestra que la reserva esta en transcurso
    else:
        reserva_activa = Reserva.objects.filter(
            sala_reservada=sala,
            fecha_hora_termino__gt=timezone.now()
        ).first()

        return render(
            request,
            "detalle.html",
            {"sala": sala, "form": None, "reserva_activa": reserva_activa},
        )
