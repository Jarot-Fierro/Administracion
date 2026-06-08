from django.db import models
from django.db.models import Q
from django.shortcuts import redirect


class CRUDListMixin:
    """
    Mixin para gestionar automáticamente filtrado, búsqueda, paginación,
    ordenamiento y generación del contexto para tablas en mantenedores.
    """
    model = None
    list_display = []  # Campos a mostrar en la tabla ['nombre', 'codigo']
    filter_form_class = None  # Clase del formulario de filtros
    search_fields = []  # Campos para la búsqueda general (HTMX)
    title = ""  # Título del mantenedor
    list_url_name = ""  # Nombre de la URL de la lista para redirecciones

    def get_queryset(self):
        queryset = super().get_queryset()

        # 1. Filtrado por Formulario de Filtros
        if self.filter_form_class:
            form = self.filter_form_class(self.request.GET)
            if form.is_valid():
                for field, value in form.cleaned_data.items():
                    if value is not None and value != '':
                        # Intentar determinar si el campo es booleano en el modelo
                        is_bool_field = False
                        try:
                            model_field = self.model._meta.get_field(field)
                            if isinstance(model_field, models.BooleanField):
                                is_bool_field = True
                        except:
                            pass

                        if is_bool_field:
                            # Convertir strings 'True'/'False' a booleanos si es necesario
                            if isinstance(value, str):
                                if value.lower() == 'true':
                                    value = True
                                elif value.lower() == 'false':
                                    value = False
                            queryset = queryset.filter(**{field: value})
                        elif isinstance(value, str):
                            queryset = queryset.filter(**{f"{field}__icontains": value})
                        else:
                            queryset = queryset.filter(**{field: value})

        # 2. Búsqueda General (HTMX)
        q = self.request.GET.get('q', '').strip()
        if q and self.search_fields:
            # Traducción de términos de búsqueda para el campo 'active' o 'is_active'
            active_q = None
            if q.lower() in ['activo', 'activa']:
                active_q = True
            elif q.lower() in ['inactivo', 'inactiva']:
                active_q = False

            query = Q()
            for field in self.search_fields:
                if (field == 'active' or field == 'is_active') and active_q is not None:
                    query |= Q(**{field: active_q})
                else:
                    query |= Q(**{f"{field}__icontains": q})
            queryset = queryset.filter(query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Evitar errores si self.model no está definido (aunque debería estarlo)
        if not self.model and hasattr(self, 'get_queryset'):
            self.model = self.get_queryset().model

        # Metadatos del modelo para las columnas
        table_columns = []
        for field_name in self.list_display:
            try:
                field = self.model._meta.get_field(field_name)
                label = field.verbose_name.capitalize()
            except:
                # Si no es un campo del modelo (ej: un method), usamos el nombre directamente
                label = field_name.replace('_', ' ').capitalize()

            table_columns.append({
                'name': field_name,
                'label': label,
                'is_boolean': isinstance(field, models.BooleanField) if 'field' in locals() else False
            })

        context.update({
            'table_columns': table_columns,
            'list_url': self.request.path,
            'title': self.title or self.model._meta.verbose_name_plural,
            'filter_form': self.filter_form_class(self.request.GET) if self.filter_form_class else None,
            'form': kwargs.get('form') or (self.form_class() if self.form_class else None),
            'search_url': self.request.path,  # Por defecto busca en la misma URL
            'showing_text': self.get_showing_text(context),
        })
        return context

    def get_showing_text(self, context):
        if context.get('is_paginated'):
            page_obj = context['page_obj']
            paginator = context['paginator']
            return f"Mostrando {page_obj.start_index()} a {page_obj.end_index()} de {paginator.count} registros"

        count = context['object_list'].count() if hasattr(context['object_list'], 'count') else len(
            context['object_list'])
        return f"Mostrando {count} registros"

    def post(self, request, *args, **kwargs):
        """
        Lógica genérica para creación y edición rápida desde la misma vista de lista.
        """
        # Verificamos si es una acción de eliminar (desactivar)
        if request.POST.get('action') == 'delete' and request.POST.get('pk'):
            try:
                obj = self.model.objects.get(pk=request.POST.get('pk'))
                obj.active = False
                if hasattr(obj, 'updated_by'):
                    obj.updated_by = request.user
                obj.save()
                return redirect(self.list_url_name or request.path)
            except self.model.DoesNotExist:
                pass

        form_class = None
        if hasattr(self, 'get_form_class'):
            form_class = self.get_form_class()
        elif self.form_class:
            form_class = self.form_class

        if form_class:
            # Si viene un pk en el POST, es una edición
            instance = None
            pk = request.POST.get('pk')
            if pk:
                try:
                    instance = self.model.objects.get(pk=pk)
                except (self.model.DoesNotExist, ValueError):
                    pass

            form = form_class(request.POST, instance=instance)
            if form.is_valid():
                obj = form.save(commit=False)
                
                # Asignación automática de campos de StandardModel si existen
                # 1. Establecimiento
                # Verificamos en el modelo si existe el campo para evitar problemas con descriptores
                has_establecimiento = any(f.name == 'establecimiento' for f in obj._meta.fields)
                if has_establecimiento and not instance: # Solo en creación si no viene de la instancia
                    user_establecimiento = getattr(request.user, 'establecimiento', None)
                    if user_establecimiento:
                        obj.establecimiento = user_establecimiento
                        obj.establecimiento_id = user_establecimiento.id
                
                # 2. Auditoría
                if hasattr(obj, 'created_by') and not obj.pk:
                    obj.created_by = request.user
                
                if hasattr(obj, 'updated_by'):
                    obj.updated_by = request.user

                try:
                    obj.save()
                    return redirect(self.list_url_name or request.path)
                except Exception as e:
                    # Si falla el save (ej: IntegrityError por establecimiento nulo),
                    # agregamos el error al formulario para mostrarlo al usuario
                    form.add_error(None, f"Error al guardar: {str(e)}")
                    if "establecimiento_id" in str(e):
                        form.add_error(None, "El usuario actual no tiene un establecimiento asignado. Por favor, asigne uno en su perfil de usuario.")

            # Si el formulario es inválido, re-renderizamos la lista con el formulario y errores
            self.object_list = self.get_queryset()
            context = self.get_context_data(object_list=self.object_list, form=form)
            return self.render_to_response(context)
        
        # Si llegamos aquí y no hay post en las clases base, simplemente redirigimos o 
        # devolvemos error. ListView NO tiene method post por defecto.
        try:
            return super().post(request, *args, **kwargs)
        except AttributeError:
            # Si ninguna clase base tiene post(), simplemente redirigimos a la lista
            return redirect(self.list_url_name or request.path)
