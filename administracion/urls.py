from django.contrib.auth import views as auth_views
from django.urls import path

from administracion.views import usuarios, comuna, establecimiento, banco, calidad_juridica, departamento, funcionarios

urlpatterns = [
    path('', usuarios.IndexView.as_view(), name='index'),
    path('usuarios/', usuarios.UsuarioListView.as_view(), name='usuarios_list'),
    path('busqueda-usuarios/', usuarios.buscar_usuarios, name='buscar_usuarios'),

    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # COMUNAS
    path('comuna/', comuna.ComunaListView.as_view(), name='comuna_list'),
    path('busqueda-comuna/', comuna.buscar_comuna, name='buscar_comuna'),

    # ESTABLECIMIENTOS
    path('establecimiento/', establecimiento.EstablecimientoListView.as_view(), name='establecimiento_list'),
    path('busqueda-establecimiento/', establecimiento.buscar_establecimiento, name='buscar_establecimiento'),

    # BANCOS
    path('banco/', banco.BancoListView.as_view(), name='banco_list'),
    path('busqueda-banco/', banco.buscar_banco, name='buscar_banco'),

    # CALIDADES JURIDICAS
    path('calidad-juridica/', calidad_juridica.CalidadJuridicaListView.as_view(), name='calidad_juridica_list'),
    path('busqueda-calidad-juridica/', calidad_juridica.buscar_calidad_juridica, name='buscar_calidad_juridica'),

    # DEPARTAMENTOS
    path('departamento/', departamento.DepartamentoListView.as_view(), name='departamento_list'),
    path('busqueda-departamento/', departamento.buscar_departamento, name='buscar_departamento'),

    # FUNCIONARIOS
    path('funcionario/', funcionarios.FuncionarioListView.as_view(), name='funcionario_list'),
    path('busqueda-funcionario/', funcionarios.buscar_funcionario, name='buscar_funcionario'),
]
