from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from administracion.filtros.departamento import DepartamentoFilterForm
from administracion.forms.departamento import DepartamentoForm
from administracion.mixin.crud_mixin import CRUDListMixin
from administracion.models.departamentos import Departamento


class DepartamentoListView(CRUDListMixin, ListView):
    model = Departamento
    template_name = 'administracion/index.html'
    paginate_by = 10

    list_display = ['id', 'nombre', 'codigo', 'active']
    search_fields = ['nombre', 'codigo']
    filter_form_class = DepartamentoFilterForm
    form_class = DepartamentoForm
    title = "Mantenedor de Departamentos"
    list_url_name = "departamento_list"

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = reverse_lazy('buscar_departamento')
        return context


def buscar_departamento(request):
    view = DepartamentoListView()
    view.request = request
    queryset = view.get_queryset()
    
    table_columns = [
        {'name': 'id', 'label': 'ID', 'is_boolean': False},
        {'name': 'nombre', 'label': 'Nombre', 'is_boolean': False},
        {'name': 'codigo', 'label': 'Código', 'is_boolean': False},
        {'name': 'active', 'label': 'Estado', 'is_boolean': True},
    ]

    return render(
        request,
        'administracion/components/_table_result.html',
        {
            "object_list": queryset[:20],
            "table_columns": table_columns,
            "list_url": reverse_lazy('departamento_list'),
        },
    )
