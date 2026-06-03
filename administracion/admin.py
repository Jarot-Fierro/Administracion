from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter
from reversion.admin import VersionAdmin
from simple_history.admin import SimpleHistoryAdmin

from administracion.models import (
    Banco, CalidadJuridica, Comuna, Departamento,
    Establecimiento, Funcionario, Usuario
)


class BaseAdmin(ImportExportModelAdmin, SimpleHistoryAdmin, VersionAdmin):
    """
    Clase base para todos los registros del admin.
    Hereda funcionalidades de Import/Export, Simple History y Revision (solo delete).
    """
    pass


# Recursos para Import/Export
class BancoResource(resources.ModelResource):
    class Meta:
        model = Banco


class CalidadJuridicaResource(resources.ModelResource):
    class Meta:
        model = CalidadJuridica


class ComunaResource(resources.ModelResource):
    class Meta:
        model = Comuna


class DepartamentoResource(resources.ModelResource):
    class Meta:
        model = Departamento


class EstablecimientoResource(resources.ModelResource):
    class Meta:
        model = Establecimiento


class FuncionarioResource(resources.ModelResource):
    class Meta:
        model = Funcionario


class UsuarioResource(resources.ModelResource):
    class Meta:
        model = Usuario


@admin.register(Banco)
class BancoAdmin(BaseAdmin):
    resource_class = BancoResource
    search_fields = ('nombre', 'codigo')
    list_display = ('nombre', 'codigo', 'website')
    list_filter = (
        ('created_at', DateRangeFilter),
    )


@admin.register(CalidadJuridica)
class CalidadJuridicaAdmin(BaseAdmin):
    resource_class = CalidadJuridicaResource
    search_fields = ('nombre', 'codigo')
    list_display = ('nombre', 'codigo')
    list_filter = (
        ('created_at', DateRangeFilter),
    )


@admin.register(Comuna)
class ComunaAdmin(BaseAdmin):
    resource_class = ComunaResource
    search_fields = ('nombre', 'codigo')
    list_display = ('nombre', 'codigo')
    list_filter = (
        ('created_at', DateRangeFilter),
    )


@admin.register(Departamento)
class DepartamentoAdmin(BaseAdmin):
    resource_class = DepartamentoResource
    search_fields = ('nombre', 'codigo')
    list_display = ('nombre', 'codigo', 'email_contacto')
    list_filter = (
        ('created_at', DateRangeFilter),
    )


@admin.register(Establecimiento)
class EstablecimientoAdmin(BaseAdmin):
    resource_class = EstablecimientoResource
    search_fields = ('nombre', 'codigo')
    list_display = ('nombre', 'codigo', 'region')
    list_filter = (
        ('created_at', DateRangeFilter),
    )


@admin.register(Funcionario)
class FuncionarioAdmin(BaseAdmin):
    resource_class = FuncionarioResource
    search_fields = ('rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'email')
    list_display = ('rut', 'nombres', 'apellido_paterno', 'email', 'departamento')
    autocomplete_fields = ('calidad_juridica', 'departamento', 'comuna_residencia', 'banco')
    list_filter = (
        ('created_at', DateRangeFilter),
        'departamento',
        'calidad_juridica',
    )


@admin.register(Usuario)
class UsuarioAdmin(BaseAdmin):
    resource_class = UsuarioResource
    search_fields = ('username', 'email', 'funcionario__nombres', 'funcionario__apellido_paterno')
    list_display = ('username', 'email', 'rol', 'is_staff')
    autocomplete_fields = ('funcionario',)

    list_filter = (
        ('date_joined', DateRangeFilter),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),

        ('Información personal', {
            'fields': ('first_name', 'last_name', 'email')
        }),

        ('Información institucional', {
            'fields': ('rol', 'funcionario', 'establecimiento',)
        }),

        ('Permisos', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),

        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )
