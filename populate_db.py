from django.contrib.auth.hashers import make_password
from adminApp.models import UsuarioSistema
from decouple import config
import os

UsuarioSistema.objects.get_or_create(
    username=os.getenv("DJANGO_SUPERUSER_USERNAME"),
    defaults={
        "password_hash": make_password(os.getenv("DJANGO_SUPERUSER_PASSWORD")),
        "rol": os.getenv("DJANGO_SUPERUSER_ROLE"),
        "id_votante": None
    }
)

print("✅ Usuario admin garantizado")
print("   - Usuario:", config("DJANGO_SUPERUSER_USERNAME"))
print("   - Contraseña:", config("DJANGO_SUPERUSER_PASSWORD"))
print("   - Rol:", config("DJANGO_SUPERUSER_ROLE"))