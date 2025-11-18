from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["rut"]  #Solo pide el rut para reservar
        widgets = {
            "rut": forms.TextInput(attrs={"class": "form-control"}),
        }