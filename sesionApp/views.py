from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
from django.db import connection

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 1️⃣ Guardar o actualizar votante en la tabla votante
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO votante (rut, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, direccion, cod_qr, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
                    ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)
                """, [
                    user.username,             # rut = username (puedes ajustarlo)
                    user.first_name,           # nombre
                    user.last_name,            # apellido_paterno
                    '',                        # apellido_materno
                    '2000-01-01',              # fecha_nacimiento (dummy)
                    'Sin dirección',           # direccion
                    f'QR-{user.username}',     # cod_qr (puede ser generado real)
                ])

            # 2️⃣ Registrar el inicio de sesión en auditoría
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO auditoria (fecha_hora_evento, entidad_afectada, tipo_evento, usuario_sistema)
                    VALUES (%s, %s, %s, %s)
                """, [
                    timezone.now(),
                    'sesion',
                    'INSERT',
                    user.username
                ])

            # 3️⃣ Redirección según el rol
            if user.is_superuser:
                return redirect('/administracion/dashboard')
            else:
                return redirect('/votante/home')

        else:
            messages.error(request, 'Credenciales incorrectas.')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')