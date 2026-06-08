from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from administracion.filtros.banco import BancoFilterForm
from administracion.forms.banco import BancoForm
from administracion.mixin.crud_mixin import CRUDListMixin
from administracion.models.banco import Banco


class BancoListView(CRUDListMixin, ListView):
    model = Banco
    template_name = 'administracion/index.html'
    paginate_by = 10

    list_display = ['id', 'nombre', 'codigo', 'active']
    search_fields = ['nombre', 'codigo']
    filter_form_class = BancoFilterForm
    form_class = BancoForm
    title = "Mantenedor de Bancos"
    list_url_name = "banco_list"

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = reverse_lazy('buscar_banco')
        return context


def buscar_banco(request):
    q = request.GET.get("q", "").strip()
    # Reutilizamos la lógica del mixin para consistencia
    view = BancoListView()
    view.request = request
    queryset = view.get_queryset()
    
    # El mixin ya maneja el filtrado por 'q' y por campos del form en get_queryset
    # si se llama adecuadamente, pero aquí lo hacemos manual por compatibilidad HTMX simple
    
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
            "list_url": reverse_lazy('banco_list'),
        },
    )
