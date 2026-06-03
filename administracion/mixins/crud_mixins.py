from django import forms
from django.db.models import Q


class CRUDListMixin:
    """
    Mixin para automatizar listados con filtrado dinámico,
    paginación y contexto para templates estandarizados.
    """
    list_display = []  # Campos a mostrar en la tabla: ['nombre', 'codigo']
    filter_form_class = None
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        queryset = super().get_queryset()

        # 1. Filtrado tradicional vía FilterForm (tfoot)
        if self.filter_form_class:
            form = self.filter_form_class(self.request.GET)
            if form.is_valid():
                for field, value in form.cleaned_data.items():
                    if value:
                        if isinstance(form.fields[field], forms.CharField):
                            queryset = queryset.filter(**{f"{field}__icontains": value})
                        else:
                            queryset = queryset.filter(**{field: value})

        # 2. Búsqueda rápida (HTMX q)
        q = self.request.GET.get('q', '').strip()
        if q and self.list_display:
            query = Q()
            for field in self.list_display:
                # Intentamos filtrar solo por campos de texto para evitar errores de tipo
                try:
                    field_obj = self.model._meta.get_field(field)
                    if isinstance(field_obj, (models.CharField, models.TextField, models.EmailField)):
                        query |= Q(**{f"{field}__icontains": q})
                except:
                    # Si no es un campo directo o falla, probamos icontains genérico
                    query |= Q(**{f"{field}__icontains": q})
            queryset = queryset.filter(query)

        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Definiciones para la tabla
        context['headers'] = [self.model._meta.get_field(f).verbose_name for f in self.list_display]
        context['fields'] = self.list_display

        # Formulario de filtros
        if self.filter_form_class:
            context['filter_form'] = self.filter_form_class(self.request.GET)

        # Texto de paginación
        if context.get('is_paginated'):
            page_obj = context['page_obj']
            paginator = context['paginator']
            context[
                'showing_text'] = f"Mostrando {page_obj.start_index()} a {page_obj.end_index()} de {paginator.count} registros"
        else:
            context['showing_text'] = f"Mostrando {context['object_list'].count()} registros"

        return context
