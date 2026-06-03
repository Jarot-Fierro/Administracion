from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView

from administracion.forms.usuarios import UsuarioForm

Usuario = get_user_model()


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios_count'] = Usuario.objects.count()
        return context


class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuarios/list.html'
    context_object_name = 'usuarios'
    paginate_by = 10
    list_filter = ['username', 'first_name', 'last_name', 'email']

    def get_paginate_by(self, queryset):
        """
        Permite cambiar la cantidad de registros por página dinámicamente.
        """
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtros segmentados del tfoot y otros
        username = self.request.GET.get('username', '').strip()
        first_name = self.request.GET.get('first_name', '').strip()
        last_name = self.request.GET.get('last_name', '').strip()
        email = self.request.GET.get('email', '').strip()

        if username:
            queryset = queryset.filter(username__icontains=username)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if email:
            queryset = queryset.filter(email__icontains=email)

        # Mantenemos búsqueda general por compatibilidad si se usa 'q' (buscador HTMX)
        q = self.request.GET.get('q', '').strip()
        if q:
            query = Q()
            for field in self.list_filter:
                query |= Q(**{f"{field}__icontains": q})
            queryset = queryset.filter(query)

        return queryset.order_by('-id')

    def render_to_response(self, context, **response_kwargs):
        # Manejo de exportación CSV si se solicita
        if self.request.GET.get('export') == 'csv':
            import csv
            from django.http import HttpResponse

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'
            response.write('\ufeff'.encode('utf-8'))  # BOM para Excel

            writer = csv.writer(response)
            writer.writerow(['ID', 'Username', 'Nombre', 'Apellido', 'Email', 'Rol'])

            # Usamos el queryset filtrado pero sin paginar
            for u in self.get_queryset():
                writer.writerow([
                    u.id,
                    u.username,
                    u.first_name,
                    u.last_name,
                    u.email,
                    u.get_rol_display()
                ])
            return response

        return super().render_to_response(context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios_list')

        # Si el formulario es inválido, volvemos a renderizar la lista con los errores
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list, form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['columns'] = ['ID', 'Username', 'Nombre Completo', 'Email', 'Rol', 'Funcionario']

        # Si ya viene un formulario en el contexto (por error en POST), lo usamos, si no creamos uno nuevo
        if 'form' not in context:
            context['form'] = UsuarioForm()

        # Calculamos el rango de registros mostrados
        if context['is_paginated']:
            page_obj = context['page_obj']
            paginator = context['paginator']
            start_index = page_obj.start_index()
            end_index = page_obj.end_index()
            total_count = paginator.count
            context['showing_text'] = f"Mostrando {start_index} a {end_index} de {total_count} registros"
        else:
            total_count = context['object_list'].count()
            context['showing_text'] = f"Mostrando {total_count} registros"

        return context


def buscar_usuarios(request):
    username = request.GET.get('username', '').strip()
    first_name = request.GET.get('first_name', '').strip()
    last_name = request.GET.get('last_name', '').strip()
    email = request.GET.get('email', '').strip()
    q = request.GET.get("q", "").strip()

    usuarios = Usuario.objects.all()

    if username:
        usuarios = usuarios.filter(username__icontains=username)
    if first_name:
        usuarios = usuarios.filter(first_name__icontains=first_name)
    if last_name:
        usuarios = usuarios.filter(last_name__icontains=last_name)
    if email:
        usuarios = usuarios.filter(email__icontains=email)

    if q:
        list_filter = ['username', 'first_name', 'last_name', 'email']
        query = Q()
        for field in list_filter:
            query |= Q(**{f"{field}__icontains": q})
        usuarios = usuarios.filter(query)

    usuarios = usuarios.order_by("-id")[:20]

    return render(
        request,
        "usuarios/partials/list_results.html",
        {
            "usuarios": usuarios,
        },
    )
