from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("sala/<int:sala_id>/", views.detalle_sala, name="detalle_sala"),
]
