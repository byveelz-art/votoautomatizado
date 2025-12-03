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

        if request.user.is_superuser:
            return redirect('/admin/')

        # 1️⃣ Buscar usuario en usuario_sistema
        try:
            usuario_sis = UsuarioSistema.objects.get(username=username)
        except UsuarioSistema.DoesNotExist:
            messages.error(request, "Usuario no existe en el sistema.")
            return render(request, "login.html")

        # 2️⃣ Validar contraseña (TEXTUAL por ahora)
        # Idealmente reemplazar por hashing real: bcrypt / sha256
        if usuario_sis.password_hash != password:
            messages.error(request, "Contraseña incorrecta.")
            return render(request, "login.html")

        # 3️⃣ Asegurar existencia del usuario Django
        user, created = User.objects.get_or_create(username=username)

        if created:
            user.set_password(password)
            user.save()

        # 4️⃣ Hacer login de usuario Django (sesión)
        login(request, user)

        # 5️⃣ Crear votante automáticamente si no existe
        if usuario_sis.id_votante is None:
            # Crear votante
            votante = Votante.objects.create(
                rut=username,
                nombre=username,
                apellido_paterno="",
                apellido_materno="",
                fecha_nacimiento="2000-01-01",
                direccion="Sin dirección",
                cod_qr=f"QR-{username}",
                activo=1
            )

            usuario_sis.id_votante = votante
            usuario_sis.save()

        # 6️⃣ Registrar en auditoría
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO auditoria (fecha_hora_evento, entidad_afectada, tipo_evento, usuario_sistema)
                VALUES (%s, %s, %s, %s)
            """, [
                timezone.now(),
                "sesion",
                "LOGIN",
                username
            ])

        # 7️⃣ Redirección según rol
        if usuario_sis.rol == "Admin":
            return redirect("/administracion/dashboard")
        else:
            return redirect("/votante/home")

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