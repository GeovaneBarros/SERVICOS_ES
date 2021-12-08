"""SERVICOS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from core.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sobre/', SobreTemplateView.as_view(), name='sobre_template_view'),
    path('usuario/criar/', UsuarioCreateView.as_view(), name='usuario_create_view'),
    path('prestador/criar/', PrestadorCreateView.as_view(), name='prestador_create_view'),
    path('prestador/listar/', PrestadorListView.as_view(), name='prestador_list_view'),
    path('prestador/<int:pk>/detalhe/', PrestadorDetailView.as_view(), name='prestador_detail_view'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_view'),
    path('login/', LoginView.as_view(), name='login_view')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   
