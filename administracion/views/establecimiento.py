from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from administracion.filtros.establecimiento import EstablecimientoFilterForm
from administracion.forms.establecimiento import EstablecimientoForm
from administracion.mixin.crud_mixin import CRUDListMixin
from administracion.models import Establecimiento


class EstablecimientoListView(CRUDListMixin, ListView):
    model = Establecimiento
    template_name = 'administracion/index.html'
    paginate_by = 10

    # Configuraciones CRUDListMixin
    list_display = ['id', 'nombre', 'codigo', 'active']
    search_fields = ['nombre', 'codigo']
    filter_form_class = EstablecimientoFilterForm
    form_class = EstablecimientoForm
    title = "Mantenedor de Establecimientos"
    list_url_name = "establecimiento_list"

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = reverse_lazy('buscar_establecimiento')
        return context


def buscar_establecimiento(request):
    view = EstablecimientoListView()
    view.request = request
    queryset = view.get_queryset()

    # Necesitamos pasar table_columns al template de búsqueda
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
            "list_url": reverse_lazy('establecimiento_list'),
        },
    )
