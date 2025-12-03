from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('panel/', views.panel_votante, name='panel_votante'),
    path('home/', views.votante_home, name='votante_home'),
    path('emitir-voto/', views.emitir_voto, name='emitir_voto'),
] 

