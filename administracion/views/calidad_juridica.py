from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from administracion.filtros.calidad_juridica import CalidadJuridicaFilterForm
from administracion.forms.calidad_juridica import CalidadJuridicaForm
from administracion.mixin.crud_mixin import CRUDListMixin
from administracion.models.calidad_juridica import CalidadJuridica


class CalidadJuridicaListView(CRUDListMixin, ListView):
    model = CalidadJuridica
    template_name = 'administracion/index.html'
    paginate_by = 10

    list_display = ['id', 'nombre', 'codigo', 'active']
    search_fields = ['nombre', 'codigo']
    filter_form_class = CalidadJuridicaFilterForm
    form_class = CalidadJuridicaForm
    title = "Mantenedor de Calidades Jurídicas"
    list_url_name = "calidad_juridica_list"

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = reverse_lazy('buscar_calidad_juridica')
        return context


def buscar_calidad_juridica(request):
    view = CalidadJuridicaListView()
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
            "list_url": reverse_lazy('calidad_juridica_list'),
        },
    )
