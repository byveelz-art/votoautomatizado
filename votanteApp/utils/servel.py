import requests
from django.conf import settings

def consultar_servel(rut, nombre, fecha_nacimiento):
    """
    Consulta la API de Khipu (SERVEL) para obtener datos electorales del votante.
    """

    # El RUT debe ir sin guión ni DV según documentación
    rut_sin_dv = rut.replace(".", "").split("-")[0]

    url = "https://services.khipu.com/services/servel.cl/electoral-data-verification/v1"

    headers = {
        "x-api-key": settings.KHIPU_API_KEY
    }

    payload = {
        "run": rut_sin_dv,
        "fullname": nombre,
        "birthday": str(fecha_nacimiento)
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        if response.status_code == 200:
            return data  # Datos completos del padrón electoral

        return None
    except:
        return None
