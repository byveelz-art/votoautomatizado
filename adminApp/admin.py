from django.contrib import admin
from adminApp.models import CandidatoOpcion, Eleccion, Votante, SesionVotacion, Terminal, Voto, Auditoria, UsuarioSistema

# Register your models here.

class CandidatoOpcionAdmin(admin.ModelAdmin):
    list_display = ('nombre_candidato', 'partido', 'cargo')
    search_fields = ('nombre_candidato', 'partido', 'cargo')

admin.site.register(CandidatoOpcion, CandidatoOpcionAdmin)
admin.site.register(Eleccion)
admin.site.register(Votante)
admin.site.register(SesionVotacion)
admin.site.register(Terminal)
admin.site.register(Voto)
admin.site.register(Auditoria)
admin.site.register(UsuarioSistema)
admin.site.site_header = "Administración de Voto Automatizado"
admin.site.site_title = "Voto Automatizado Admin"
admin.site.index_title = "Panel de Administración"
