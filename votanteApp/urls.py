from django.urls import path
from . import views

urlpatterns = [
    path('panel/', views.panel_votante, name='panel_votante'),
    path('home/', views.votante_home, name='votante_home'),
]