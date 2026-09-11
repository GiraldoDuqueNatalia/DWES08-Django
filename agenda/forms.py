from django import forms
from django.db import models  
from .models import Reserva, FechaEvento

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['email', 'cantidad_entradas', 'fecha_evento']
        widgets = {
            'fecha_evento': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cantidad_entradas': forms.NumberInput(attrs={'class': 'form-control', 'max': 6}),
        }
        labels = {
            'email': 'Correo electrónico',
            'cantidad_entradas': 'Cantidad de entradas',
            'fecha_evento': 'Selecciona una sesión',
        }

    def __init__(self, *args, **kwargs):
        evento_actual = kwargs.pop('evento', None)  
        usuario = kwargs.pop('usuario', None)  
        super().__init__(*args, **kwargs)

        if evento_actual:
            self.fields['fecha_evento'].queryset = FechaEvento.objects.filter(evento=evento_actual)
            self.fields['fecha_evento'].label_from_instance = lambda obj: (
                f"{obj.fecha.strftime('%d/%m/%Y %H:%M')} - {obj.evento.sala.capacidad - (Reserva.objects.filter(fecha_evento=obj).aggregate(total=models.Sum('cantidad_entradas'))['total'] or 0)} plazas disponibles"
            )

        #  Si el usuario está autenticado, ocultamos el campo de email y lo llenamos automáticamente
        if usuario and usuario.is_authenticated:
            self.fields['email'].required = False 
            self.fields['email'].widget = forms.HiddenInput() 
            self.fields['email'].initial = usuario.email  
