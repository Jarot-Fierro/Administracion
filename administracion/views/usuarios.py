from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView

from administracion.filtros.usuarios import UsuarioFilterForm
from administracion.forms.usuarios import UsuarioForm
from administracion.mixin.crud_mixin import CRUDListMixin

Usuario = get_user_model()


class IndexView(TemplateView):
    template_name = 'administracion/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios_count'] = Usuario.objects.count()
        context['title'] = "Dashboard de Administración"
        return context


class UsuarioListView(CRUDListMixin, ListView):
    model = Usuario
    template_name = 'administracion/index.html'
    paginate_by = 10

    list_display = ['id', 'username', 'email', 'rol', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    filter_form_class = UsuarioFilterForm
    form_class = UsuarioForm
    title = "Mantenedor de Usuarios"
    list_url_name = "usuarios_list"

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = reverse_lazy('buscar_usuarios')
        return context


def buscar_usuarios(request):
    view = UsuarioListView()
    view.request = request
    queryset = view.get_queryset()

    table_columns = [
        {'name': 'id', 'label': 'ID', 'is_boolean': False},
        {'name': 'username', 'label': 'Username', 'is_boolean': False},
        {'name': 'email', 'label': 'Email', 'is_boolean': False},
        {'name': 'rol', 'label': 'Rol', 'is_boolean': False},
        {'name': 'is_active', 'label': 'Estado', 'is_boolean': True},
    ]

    return render(
        request,
        'administracion/components/_table_result.html',
        {
            "object_list": queryset[:20],
            "table_columns": table_columns,
            "list_url": reverse_lazy('usuarios_list'),
        },
    )
