from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Sala, Reserva
from .forms import ReservaForm

def inicio(request):
    salas = Sala.objects.all()
    
    for sala in salas:
        estado_real = sala.disponible_ahora
        if sala.disponibilidad != estado_real:
            sala.disponibilidad = estado_real
            sala.save(update_fields=['disponibilidad'])
            
    return render(request, "inicio.html", {"salas": salas})

def detalle_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    ahora = timezone.now()

    reserva_activa = Reserva.objects.filter(
        sala_reservada=sala,
        fecha_hora_termino__gt=ahora
    ).first()

    if sala.disponible_ahora:
        if request.method == "POST":
            form = ReservaForm(request.POST)
            if form.is_valid():
                reserva = form.save(commit=False)
                reserva.sala_reservada = sala
                reserva.save()
                return redirect("detalle_sala", sala_id=sala.id)
        else:
            form = ReservaForm()
            
        return render(request, "detalle.html", {
            "sala": sala,
            "form": form,
            "reserva_activa": None
        })

    return render(request, "detalle.html", {
        "sala": sala,
        "form": None,
        "reserva_activa": reserva_activa
    })