from django.contrib.auth.hashers import make_password
from adminApp.models import UsuarioSistema
from decouple import config

UsuarioSistema.objects.get_or_create(
    username=config("DJANGO_SUPERUSER_USERNAME"),
    defaults={
        "password_hash": make_password(config("DJANGO_SUPERUSER_PASSWORD")),
        "rol": config("DJANGO_SUPERUSER_ROLE"),
        "id_votante": None
    }
)

print("✅ Usuario admin garantizado")
