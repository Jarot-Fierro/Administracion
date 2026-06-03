from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.contrib.auth import get_user_model

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['columns'] = ['ID', 'Username', 'Email', 'Rol', 'Funcionario']
        return context
