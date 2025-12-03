from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q, Count
from adminApp.models import Votante, Eleccion, SesionVotacion, CandidatoOpcion, Voto , Auditoria, Terminal, UsuarioSistema
from django.utils import timezone
from django.contrib import messages
from adminApp.forms import CandidatoOpcionForm, UsuarioSistemaForm
from rest_framework import viewsets
from adminApp.serializers import CandidatoOpcionSerializer
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.


# View para el dashboard principal
# Muestra estadísticas resumidas
@login_required(login_url='/sesion/login/')
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Datos resumidos para la vista principal
    total_votantes = Votante.objects.count()
    total_elecciones = Eleccion.objects.count()
    total_candidatos = CandidatoOpcion.objects.count()
    total_votos = Voto.objects.count()
    sesiones_activas = SesionVotacion.objects.filter(estado_sesion='iniciada').count()

    context = {
        'total_votantes': total_votantes,
        'total_elecciones': total_elecciones,
        'total_candidatos': total_candidatos,
        'total_votos': total_votos,
        'sesiones_activas': sesiones_activas,
    }
    return render(request, 'dashboard.html', context)

# View para listar candidatos
@login_required(login_url='/sesion/login/')
def lista_candidatos(request):
    query = request.GET.get('q')
    if query:
        candidatos = CandidatoOpcion.objects.filter(
            Q(nombre_candidato__icontains=query) |
            Q(partido__icontains=query) |
            Q(cargo__icontains=query)
        )
    else:
        candidatos = CandidatoOpcion.objects.all()
    return render(request, 'lista.html', {'candidatos': candidatos})

# View para crear un nuevo candidato
@login_required(login_url='/sesion/login/')
def crear_candidato(request):
    if request.method == 'POST':
        form = CandidatoOpcionForm(request.POST)
        if form.is_valid():
            from django.db import transaction
            try:
                with transaction.atomic():
                    candidato = form.save()
                    registrar_auditoria('candidato_opcion', candidato.candidato_id, 'INSERT', request.user.username)
                messages.success(request, f'✅ Candidato "{candidato.nombre_candidato}" agregado correctamente.')
                return redirect('lista_candidatos')
            except Exception as e:
                messages.error(request, f'❌ Error al agregar candidato: {str(e)}')
    else:
        form = CandidatoOpcionForm()
    return render(request, 'form.html', {'form': form, 'titulo': 'Agregar Candidato'})

# View para editar un candidato existente
@login_required(login_url='/sesion/login/')
def editar_candidato(request, candidato_id):
    candidato = get_object_or_404(CandidatoOpcion, candidato_id=candidato_id)
    if request.method == 'POST':
        form = CandidatoOpcionForm(request.POST, instance=candidato)
        if form.is_valid():
            form.save()
            registrar_auditoria('candidato_opcion', candidato.candidato_id, 'UPDATE', request.user.username)
            messages.info(request, f'✏️ Candidato "{candidato.nombre_candidato}" actualizado.')
            return redirect('lista_candidatos')
    else:
        form = CandidatoOpcionForm(instance=candidato)
    return render(request, 'form.html', {'form': form, 'titulo': 'Editar Candidato'})

# View para eliminar un candidato
@login_required(login_url='/sesion/login/')
def eliminar_candidato(request, candidato_id):
    candidato = get_object_or_404(CandidatoOpcion, candidato_id=candidato_id)
    if request.method == 'POST':
        nombre = candidato.nombre_candidato
        id_cand = candidato.candidato_id
        candidato.delete()
        registrar_auditoria('candidato_opcion', id_cand, 'DELETE', request.user.username)
        messages.error(request, f'🗑️ Candidato "{nombre}" eliminado.')
        return redirect('lista_candidatos')
    return render(request, 'eliminar.html', {'candidato': candidato})

# View para ver detalles de un candidato
@login_required(login_url='/sesion/login/')
def detalle_candidato(request, candidato_id):
    candidato = get_object_or_404(CandidatoOpcion, candidato_id=candidato_id)
    registrar_auditoria('candidato_opcion', candidato.candidato_id, 'SELECT', request.user.username)
    messages.info(request, f'ℹ️ Viste los detalles del candidato "{candidato.nombre_candidato}".')
    return render(request, 'detalle.html', {'candidato': candidato})

# Función para registrar auditoría
def registrar_auditoria(entidad, id_registro, tipo_evento, usuario, terminal_id=None):
    Auditoria.objects.create(
        fecha_hora_evento=timezone.now(),
        entidad_afectada=entidad,
        id_registro_afectado=id_registro,
        tipo_evento=tipo_evento,
        usuario_sistema=usuario,
        terminal_id=terminal_id
    )

# API ViewSet para CandidatoOpcion
class CandidatoOpcionViewSet(viewsets.ModelViewSet):
    queryset = CandidatoOpcion.objects.all()
    serializer_class = CandidatoOpcionSerializer
    def perform_create(self, serializer):
        candidato = serializer.save()
        registrar_auditoria('candidato_opcion', candidato.candidato_id, 'INSERT', self.request.user.username)
    def perform_update(self, serializer):
        candidato = serializer.save()
        registrar_auditoria('candidato_opcion', candidato.candidato_id, 'UPDATE', self.request.user.username)
    def perform_destroy(self, instance):
        id_cand = instance.candidato_id
        instance.delete()
        registrar_auditoria('candidato_opcion', id_cand, 'DELETE', self.request.user.username)

def candidato_opcion_api():
    return CandidatoOpcionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })

@login_required(login_url='/sesion/login/')
def lista_usuarios(request):
    usuarios = UsuarioSistema.objects.select_related('id_votante').all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

# ✅ CREAR USUARIO
@login_required(login_url='/sesion/login/')
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioSistemaForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            registrar_auditoria('usuario_sistema', usuario.id_usuario, 'INSERT', request.user.username)
            messages.success(request, "✅ Usuario creado correctamente.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioSistemaForm()

    return render(request, 'form_usuario.html', {
        'form': form,
        'titulo': 'Crear Usuario'
    })

# ✅ EDITAR USUARIO
@login_required(login_url='/sesion/login/')
def editar_usuario(request, id_usuario):
    usuario = get_object_or_404(UsuarioSistema, id_usuario=id_usuario)

    if request.method == 'POST':
        form = UsuarioSistemaForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            registrar_auditoria('usuario_sistema', usuario.id_usuario, 'UPDATE', request.user.username)
            messages.info(request, "✏️ Usuario actualizado.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioSistemaForm(instance=usuario)

    return render(request, 'form_usuario.html', {
        'form': form,
        'titulo': 'Editar Usuario'
    })

# ✅ ELIMINAR USUARIO
@login_required(login_url='/sesion/login/')
def eliminar_usuario(request, id_usuario):
    usuario = get_object_or_404(UsuarioSistema, id_usuario=id_usuario)

    if request.method == 'POST':
        usuario.delete()
        registrar_auditoria('usuario_sistema', id_usuario, 'DELETE', request.user.username)
        messages.error(request, "🗑️ Usuario eliminado.")
        return redirect('lista_usuarios')

    return render(request, 'eliminar_usuario.html', {'usuario': usuario})