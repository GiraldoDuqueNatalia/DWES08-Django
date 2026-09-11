# Create your models here.
from django.db import models

# Tabla para las salas
class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

# Tabla para los eventos
class Evento(models.Model):
    TIPO_EVENTO = [
        ('Teatro', 'Teatro'),
        ('Cine', 'Cine'),
        ('Exposición','Exposición'),
    ]
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_EVENTO)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.titulo

# Tabla para la fecha de los eventos 
class FechaEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha = models.DateTimeField()

    def __str__(self):
        return f"{self.evento.titulo} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        ordering = ['-fecha']



class Reserva(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_evento = models.ForeignKey(FechaEvento, on_delete=models.CASCADE)
    email = models.EmailField()
    cantidad_entradas = models.PositiveIntegerField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.email} - {self.evento.titulo} ({self.cantidad_entradas} entradas)"

    class Meta:
        ordering = ['-creado_en']  # Orden descendente por fecha de creación
