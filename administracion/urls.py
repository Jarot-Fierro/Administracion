from django.contrib.auth import views as auth_views
from django.urls import path

from administracion.views import usuarios, comunas

urlpatterns = [
    path('', usuarios.IndexView.as_view(), name='index'),
    path('usuarios/', usuarios.UsuarioListView.as_view(), name='usuarios_list'),
    path('busqueda-usuarios/', usuarios.buscar_usuarios, name='buscar_usuarios'),

    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # COMUNAS
    path('comuna/', comunas.ComunaListView.as_view(), name='comuna_list'),
    path('busqueda-comuna/', comunas.buscar_comuna, name='buscar_comuna'),
]
