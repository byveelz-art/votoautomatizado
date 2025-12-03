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
from adminApp.models import Votante, Voto, SesionVotacion, CandidatoOpcion, UsuarioSistema
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
        votante = Votante.objects.filter(rut=request.user.username).first()

        if not votante:
            messages.error(request, "No existe un votante asociado al usuario")
            return redirect("panel_votante")

        candidato_id = request.POST.get("candidato_id")
        candidato = CandidatoOpcion.objects.get(pk=candidato_id)

        # Crear sesión de votación
        sesion = SesionVotacion.objects.create(
            id_votante=votante,
            terminal_id=1,
            fecha_hora_inicio=timezone.now(),
            estado_sesion="activa"
        )

        # Crear hash de verificación
        voto_raw = f"{votante.id_votante}-{candidato.nombre_candidato}-{timezone.now()}"
        hash_ver = hashlib.sha256(voto_raw.encode()).hexdigest()

        # Crear voto
        comprobante = str(uuid.uuid4())[:12]
        voto = Voto.objects.create(
            id_sesion=sesion,
            id_candidato=candidato,
            tipo_eleccion=candidato.eleccion,
            fecha_hora_emision=timezone.now(),
            voto_encriptado="VOTO_SIMULADO",
            hash_verificacion=hash_ver,
            comprobante_emision=comprobante
        )

        # -------------------------------
        #   GENERAR PDF DEL COMPROBANTE
        # -------------------------------
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        import os

        carpeta = os.path.join(settings.MEDIA_ROOT, "votos_pdf")
        os.makedirs(carpeta, exist_ok=True)

        nombre_pdf = f"comprobante_{voto.id_voto}.pdf"
        ruta_pdf = os.path.join(carpeta, nombre_pdf)

        # Generar el PDF
        c = canvas.Canvas(ruta_pdf, pagesize=letter)
        c.setFont("Helvetica", 12)

        c.drawString(50, 750, "COMPROBANTE DE VOTO")
        c.drawString(50, 720, f"Votante: {votante.nombre} {votante.apellido_paterno} {votante.apellido_materno}")
        c.drawString(50, 700, f"RUT: {votante.rut}")
        c.drawString(50, 680, f"Elección: {candidato.eleccion}")
        c.drawString(50, 660, f"Candidato: {candidato.nombre_candidato}")
        c.drawString(50, 640, f"Fecha: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(50, 620, f"Hash: {hash_ver[:25]}...")
        c.drawString(50, 600, f"Comprobante: {comprobante}")

        c.showPage()
        c.save()

        # Guardarlo en el FileField real de Django
        with open(ruta_pdf, "rb") as pdf:
            voto.pdf_file.save(nombre_pdf, File(pdf), save=True)

        messages.success(request, "Voto emitido correctamente. Comprobante disponible.")
        return redirect("panel_votante")

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