# votanteApp/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sesionApp import views

@login_required
def panel_votante(request):
    return render(request, 'panel_votante.html', {
        'usuario': request.user,
    })

@login_required
def votante_home(request):
    return render(request, 'home.html')