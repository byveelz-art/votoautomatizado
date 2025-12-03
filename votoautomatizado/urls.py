"""
URL configuration for votoautomatizado project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from adminApp import urls as admin_urls
from sesionApp import urls as sesion_urls
from votanteApp import urls as votante_urls
from verificarApp.views import verificar_voto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('administracion/', include(admin_urls)),
    path('', include(sesion_urls)),
    path('votante/', include(votante_urls)),
    path("verificar-voto/", verificar_voto, name="verificar_voto"),
]