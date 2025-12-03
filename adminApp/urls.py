from django.urls import path, include
from adminApp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'candidatos', views.CandidatoOpcionViewSet, basename='candidatoopcion')

urlpatterns = [
    path('dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('candidatos/', views.lista_candidatos, name='lista_candidatos'),
    path('candidatos/<int:candidato_id>/', views.detalle_candidato, name='detalle_candidato'),
    path('candidatos/crear/', views.crear_candidato, name='crear_candidato'),
    path('candidatos/editar/<int:candidato_id>/', views.editar_candidato, name='editar_candidato'),
    path('candidatos/eliminar/<int:candidato_id>/', views.eliminar_candidato, name='eliminar_candidato'),
    path('api/candidatos/', views.candidato_opcion_api, name='candidato_opcion_api'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id_usuario>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id_usuario>/', views.eliminar_usuario, name='eliminar_usuario'),
]