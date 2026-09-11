"""
URL configuration for proyectoDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from agenda import views 
from django.views.generic import RedirectView 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
   #  path('paginaExemple/', views.home, name="home"),
    path('portada/', views.portada, name="portada"),
    path('', RedirectView.as_view(url='/agenda/')),  # para que si escribimos en el navegador con o sin se abra agenda_general.html  
    path('agenda/', include('agenda.urls')),  # para mantener las URLs de la app agenda
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
