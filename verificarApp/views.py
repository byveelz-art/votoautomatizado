# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from adminApp.models import Voto
import hashlib

def verificar_voto(request):
    if request.method == "POST":
        comprobante = request.POST.get("comprobante")
        hash_ingresado = request.POST.get("hash")

        try:
            voto = Voto.objects.get(comprobante_emision=comprobante)

            # Recalcular hash desde los datos reales
            base_string = f"{voto.id_sesion.id_sesion}-{voto.id_candidato.nombre_candidato}-{voto.fecha_hora_emision}"
            hash_real = hashlib.sha256(base_string.encode()).hexdigest()

            if hash_real == hash_ingresado:
                messages.success(request, "✅ VOTO VÁLIDO Y NO ALTERADO")
                return render(request, "verificar_voto.html", {
                    "valido": True,
                    "voto": voto
                })
            else:
                messages.error(request, "❌ EL VOTO FUE ALTERADO")
                return render(request, "verificar_voto.html", {
                    "valido": False,
                    "voto": voto
                })

        except Voto.DoesNotExist:
            messages.error(request, "⚠️ NO EXISTE NINGÚN VOTO CON ESE COMPROBANTE")

    return render(request, "verificar_voto.html")
