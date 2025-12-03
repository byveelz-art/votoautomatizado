from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db import connection
from adminApp.models import UsuarioSistema, Votante


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            usuario_sis = UsuarioSistema.objects.get(username=username)
        except UsuarioSistema.DoesNotExist:
            return render(request, "login.html", {
                "error": "Usuario no existe"
            })

        if usuario_sis.password_hash != password:
            return render(request, "login.html", {
                "error": "Contraseña incorrecta"
            })

        if usuario_sis.rol == "Admin":
            return redirect("/admin/")
        else:
            return redirect("/votante/")

    return render(request, "login.html")

def logout_view(request):
    username = request.user.username

    # Registrar en auditoría antes de logout
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO auditoria (fecha_hora_evento, entidad_afectada, tipo_evento, usuario_sistema)
            VALUES (%s, %s, %s, %s)
        """, [
            timezone.now(),
            "sesion",
            "LOGOUT",
            username
        ])

    logout(request)
    return redirect('login/')