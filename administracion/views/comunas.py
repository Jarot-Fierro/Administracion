from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from administracion.filtros.comunas import ComunaFilterForm
from administracion.forms.comunas import ComunaForm
from administracion.mixin.crud_mixin import CRUDListMixin
from administracion.models import Comuna


class ComunaListView(CRUDListMixin, ListView):
    model = Comuna
    template_name = 'administracion/index.html'
    paginate_by = 10

    # Configuraciones CRUDListMixin
    list_display = ['id', 'nombre', 'codigo', 'active']
    search_fields = ['nombre', 'codigo']
    filter_form_class = ComunaFilterForm
    form_class = ComunaForm
    title = "Mantenedor de Comunas"
    list_url_name = "comuna_list"

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = reverse_lazy('buscar_comuna')
        return context


def buscar_comuna(request):
    # Reutilizamos el mixin para la búsqueda HTMX si fuera necesario, 
    # pero por ahora mantenemos la compatibilidad con el endpoint existente 
    # adaptándolo al nuevo sistema de filtrado si se desea.
    nombre = request.GET.get('nombre', '').strip()
    codigo = request.GET.get('codigo', '').strip()
    q = request.GET.get("q", "").strip()

    comuna = Comuna.objects.all()

    if nombre:
        comuna = comuna.filter(nombre__icontains=nombre)
    if codigo:
        comuna = comuna.filter(codigo__icontains=codigo)
    if q:
        query = Q()
        for field in ['nombre', 'codigo']:
            query |= Q(**{f"{field}__icontains": q})
        comuna = comuna.filter(query)

    comuna = comuna.order_by("-id")[:20]

    # Necesitamos pasar table_columns al template de búsqueda
    table_columns = [
        {'name': 'id', 'label': 'ID'},
        {'name': 'nombre', 'label': 'Nombre'},
        {'name': 'codigo', 'label': 'Código'},
        {'name': 'active', 'label': 'Activo'},
    ]

    return render(
        request,
        'administracion/components/_table_result.html',
        {
            "object_list": comuna,
            "table_columns": table_columns,
        },
    )
