from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from administracion.filtros.funcionarios import FuncionarioFilterForm
from administracion.forms.funcionarios import FuncionarioForm
from administracion.mixin.crud_mixin import CRUDListMixin
from administracion.models.funcionarios import Funcionario


class FuncionarioListView(CRUDListMixin, ListView):
    model = Funcionario
    template_name = 'administracion/index.html'
    paginate_by = 10

    list_display = ['id', 'rut', 'nombres', 'apellido_paterno', 'active']
    search_fields = ['rut', 'nombres', 'apellido_paterno', 'apellido_materno']
    filter_form_class = FuncionarioFilterForm
    form_class = FuncionarioForm
    title = "Mantenedor de Funcionarios"
    list_url_name = "funcionario_list"

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = reverse_lazy('buscar_funcionario')
        return context


def buscar_funcionario(request):
    view = FuncionarioListView()
    view.request = request
    queryset = view.get_queryset()
    
    table_columns = [
        {'name': 'id', 'label': 'ID', 'is_boolean': False},
        {'name': 'rut', 'label': 'RUT', 'is_boolean': False},
        {'name': 'nombres', 'label': 'Nombres', 'is_boolean': False},
        {'name': 'apellido_paterno', 'label': 'Apellido P.', 'is_boolean': False},
        {'name': 'active', 'label': 'Estado', 'is_boolean': True},
    ]

    return render(
        request,
        'administracion/components/_table_result.html',
        {
            "object_list": queryset[:20],
            "table_columns": table_columns,
            "list_url": reverse_lazy('funcionario_list'),
        },
    )
