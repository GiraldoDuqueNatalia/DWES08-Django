from django.contrib import admin
from .models import Sala, Evento, FechaEvento, Reserva

admin.site.register(Sala)
admin.site.register(Evento)
admin.site.register(FechaEvento)
admin.site.register(Reserva)
