from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento, FechaEvento, Reserva
from .forms import ReservaForm
from django.db import models

from django.contrib import messages 

from allauth.socialaccount.models import SocialToken
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import timedelta

from django.utils.safestring import mark_safe
import os



# Vista para la página de portada (solo de prueba)
def portada(request):
    return render(request, 'agenda/portada.html')

# Vista general de la agenda, la página principal de los eventos del teatro 
def agenda_general(request):
    eventos = Evento.objects.all()
    return render(request, 'agenda/agenda_general.html', {'eventos': eventos})

# Vista de detalle del evento con funcionalidad de reservas
def evento_detalle(request, slug):
    evento = get_object_or_404(Evento, slug=slug)
    form = ReservaForm(request.POST or None, evento=evento, usuario=request.user)
  # Pasamos el evento al formulario

    if request.method == 'POST':  # Si el usuario envía el formulario
        if form.is_valid():  # Si el formulario es válido
            reserva = form.save(commit=False)  # No guarda aún en la base de datos
            reserva.evento = evento  # Asocia la reserva al evento actual

            # Verifica si hay capacidad disponible
            entradas_reservadas = Reserva.objects.filter(fecha_evento=reserva.fecha_evento).aggregate(
                total=models.Sum('cantidad_entradas'))['total'] or 0
            capacidad_restante = reserva.fecha_evento.evento.sala.capacidad - entradas_reservadas

            # Verifica si las entradas solicitadas no exceden la capacidad restante
            if reserva.cantidad_entradas <= capacidad_restante:
                reserva.save()
                
              

            # si esta autenticado agregar a su calendario
            if request.user.is_authenticated:
                try:
                    token = SocialToken.objects.get(account__user=request.user, account__provider='google')
                    creds = Credentials(
                        token=token.token,
                        refresh_token=token.token_secret,
                        token_uri="https://oauth2.googleapis.com/token",
                        # Configurar las credenciales OAuth de Google mediante variables de entorno
                        # GOOGLE_CLIENT_ID
                        # GOOGLE_CLIENT_SECRET
                        client_id=os.getenv("GOOGLE_CLIENT_ID"),
                        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
                        
                        
                        scopes=['https://www.googleapis.com/auth/calendar.events']
                    )

                    service = build('calendar', 'v3', credentials=creds)
                    event = {
                        'summary': reserva.evento.titulo,
                        'description': f"Reserva de {reserva.cantidad_entradas} entrada(s) per a {reserva.evento.titulo}",
                        'start': {'dateTime': reserva.fecha_evento.fecha.isoformat(), 'timeZone': 'Europe/Madrid'},
                        'end': {'dateTime': (reserva.fecha_evento.fecha + timedelta(hours=2)).isoformat(), 'timeZone': 'Europe/Madrid'},
                    }
                    event_result = service.events().insert(calendarId='primary', body=event).execute()
                    event_link = event_result.get('htmlLink')

                    

                    messages.success( request, mark_safe(f"""¡Reserva efectuada correctamente! Has reservado {reserva.cantidad_entradas} entradas para la sesión {reserva.fecha_evento.fecha.strftime('%d/%m/%Y %H:%M')} del {reserva.evento.titulo}.  
                            <br><br> 
                            <a href='{event_link}' target='_blank' 
                                style='display: inline-block; padding: 10px 15px; background-color: #007bff; color: white; border-radius: 5px; text-decoration: none; font-weight: bold;'>
                                Ir a Google Calendar
                            </a>
                        """)
                    )

                   

                except SocialToken.DoesNotExist:
                    messages.warning(request, "Reserva hecha pero no se logra agregar a su calendario de google.")

            else:
                messages.success(
                    request,
                    f"¡Reserva efectuada correctamente! se ha reservado {reserva.cantidad_entradas} entrades para la sesion  {reserva.fecha_evento.fecha.strftime('%d/%m/%Y %H:%M')} del {reserva.evento.titulo}. Revisa los detalles en tu emal {reserva.email}."
                )

            return redirect('evento_detalle', slug=slug)
        else:
            messages.error(request, "No se puede hacer la reserva, no quedan tantas entradas para esta sesión.")

    return render(request, 'agenda/evento_detalle.html', {'evento': evento, 'form': form})




