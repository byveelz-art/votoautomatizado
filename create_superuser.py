import os
from django.contrib.auth import get_user_model

User = get_user_model()

def run():
    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email='',
            password=password
        )
        print("✅ Superusuario creado automáticamente en Render")
    else:
        print("ℹ️ El superusuario ya existe")

    print("   - Usuario:", username)
    print("   - Contraseña:", password)
    print("   - Rol: Admin")

run()