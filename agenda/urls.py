from django.urls import path
from . import views

urlpatterns = [
    path('', views.agenda_general, name='agenda_general'),
    path('<slug:slug>/', views.evento_detalle, name='evento_detalle'),
]
