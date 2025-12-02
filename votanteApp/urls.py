from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('panel/', views.panel_votante, name='panel_votante'),
    path('home/', views.votante_home, name='votante_home'),
    path('emitir-voto/', views.emitir_voto, name='emitir_voto'),
    path("pdf-votos/", views.generar_pdf_votos, name="generar_pdf_votos"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

