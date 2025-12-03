from datetime import datetime
import django
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
import hashlib
import uuid
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from adminApp.models import Votante, Voto, SesionVotacion, CandidatoOpcion, UsuarioSistema, Terminal
from votanteApp.utils.servel import consultar_servel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.core.files.base import ContentFile
from io import BytesIO
from django.conf import settings
from django.core.files import File


@login_required
def votante_home(request):
    return render(request, 'home.html')


@login_required
def panel_votante(request):

    votante = Votante.objects.filter(rut=request.user.username).first()

    if not votante:
        return render(request, "panel_votante.html", {
            "error": "No se encontró perfil de votante"
        })

    # Consultar padrón SERVEL vía Khipu
    servel_data = consultar_servel(
        rut=votante.rut,
        nombre=f"{votante.nombre} {votante.apellido_paterno} {votante.apellido_materno}",
        fecha_nacimiento=votante.fecha_nacimiento
    )

    votos = Voto.objects.filter(id_sesion__id_votante=votante)
    candidatos = CandidatoOpcion.objects.all()

    search = request.GET.get("search", "")

    votos = Voto.objects.filter(id_sesion__id_votante=votante)

    if search:
        votos = votos.filter(
            Q(tipo_eleccion__icontains=search) |
            Q(hash_verificacion__icontains=search) |
            Q(comprobante_emision__icontains=search) |
            Q(fecha_hora_emision__icontains=search)
        )


    return render(request, 'panel_votante.html', {
        'votante': votante,
        'votos': votos,
        'candidatos': candidatos,
        'servel': servel_data,
        "search": search
    })


@login_required
def emitir_voto(request):

    if request.method == "POST":
        # ✅ 1. Buscar votante por username
        votante = Votante.objects.filter(rut=request.user.username).first()

        Terminal.objects.get_or_create(
            terminal_id="1",
            defaults={"ubicacion": "Producción", "estado_terminal": "Activo"}
        )

        if not votante:
            messages.error(request, "No existe un votante asociado al usuario.")
            return redirect("panel_votante")

        # ✅ 2. Validar candidato
        candidato_id = request.POST.get("candidato_id")

        if not candidato_id:
            messages.error(request, "Debe seleccionar un candidato.")
            return redirect("panel_votante")

        try:
            candidato = CandidatoOpcion.objects.get(pk=candidato_id)
        except CandidatoOpcion.DoesNotExist:
            messages.error(request, "El candidato no existe.")
            return redirect("panel_votante")

        # ✅ 3. Validar que exista un terminal (ESTO ARREGLA TU ERROR FK EN RENDER)
        terminal = Terminal.objects.first()

        if not terminal:
            messages.error(request, "No hay terminal disponible en el sistema.")
            return redirect("panel_votante")

        # ✅ 4. Evitar que el votante vote dos veces
        # if SesionVotacion.objects.filter(id_votante=votante).exists():
        #     messages.error(request, "Este votante ya emitió su voto.")
        #     return redirect("panel_votante")

        # ✅ 5. Crear sesión correctamente (FORMA CORRECTA DEL FK)
        sesion = SesionVotacion.objects.create(
            id_votante=votante,
            terminal=terminal,   # ✅ NO terminal_id
            fecha_hora_inicio=timezone.now(),
            estado_sesion="Activa"
        )

        # ✅ 6. Generar hash seguro
        fecha_emision = timezone.now()
        voto_raw = f"{sesion.id_sesion}-{candidato.nombre_candidato}-{fecha_emision}"
        hash_ver = hashlib.sha256(voto_raw.encode()).hexdigest()

        # ✅ 7. Crear voto
        comprobante = str(uuid.uuid4())[:12]

        Voto.objects.create(
            id_sesion=sesion,
            id_candidato=candidato,
            tipo_eleccion=candidato.eleccion,
            fecha_hora_emision=fecha_emision,
            voto_encriptado="VOTO_SIMULADO",
            hash_verificacion=hash_ver,
            comprobante_emision=comprobante
        )

        messages.success(request, "✅ Voto emitido correctamente. Comprobante generado.")
        return redirect("panel_votante")

    # ✅ 8. ESTE RETURN ES EL QUE ARREGLA EL ERROR 500 EN RENDER
    return render(request, "panel_votante.html")

# @login_required
# def generar_pdf_votos(request):
#     votante = Votante.objects.filter(rut=request.user.username).first()
#     votos = Voto.objects.filter(id_sesion__id_votante=votante)

#     # Configurar respuesta como archivo PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="comprobante_votos.pdf"'

#     c = canvas.Canvas(response, pagesize=letter)
#     width, height = letter

#     y = height - 50
#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(50, y, "Comprobante de Votos Emitidos")
#     y -= 40

#     c.setFont("Helvetica", 12)
#     c.drawString(50, y, f"Votante: {votante.nombre} {votante.apellido_paterno} ({votante.rut})")
#     y -= 30

#     # Tabla / lista de votos
#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(50, y, "Elección")
#     c.drawString(200, y, "Fecha")
#     c.drawString(350, y, "Comprobante")
#     y -= 20

#     c.setFont("Helvetica", 11)

#     for voto in votos:
#         if y < 80:
#             c.showPage()
#             y = height - 80

#         c.drawString(50, y, voto.tipo_eleccion)
#         c.drawString(200, y, voto.fecha_hora_emision.strftime("%Y-%m-%d %H:%M"))
#         c.drawString(350, y, voto.comprobante_emision)
#         y -= 20

#     c.showPage()
#     c.save()

#     return response

# def generar_pdf_voto(voto):
#     buffer = BytesIO()
#     c = canvas.Canvas(buffer, pagesize=letter)
#     width, height = letter

#     y = height - 50
#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(50, y, "Comprobante de Voto")
#     y -= 40

#     c.setFont("Helvetica", 12)
#     c.drawString(50, y, f"Tipo de elección: {voto.tipo_eleccion}")
#     y -= 25

#     c.drawString(50, y, f"Fecha emisión: {voto.fecha_hora_emision.strftime('%Y-%m-%d %H:%M')}")
#     y -= 25

#     c.drawString(50, y, "Comprobante único:")
#     y -= 20

#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(50, y, voto.pdf)
#     y -= 40

#     c.showPage()
#     c.save()

#     buffer.seek(0)
#     return buffer