# Automatización de Mantenedores (CRUD Genérico)

Este documento describe la arquitectura CRUD genérica implementada en el proyecto para automatizar la creación de mantenedores, evitando la duplicación de lógica y plantillas HTML.

## 1. Estructura de Archivos

Los archivos principales que componen esta arquitectura son:

- **Mixin Principal:** `administracion/mixin/crud_mixin.py` (`CRUDListMixin`)
- **Template Tag:** `administracion/templatetags/crud_tags.py` (Filtro `get_attr`)
- **Plantilla Base:** `administracion/templates/administracion/index.html`
- **Componentes Reutilizables:**
    - `administracion/templates/administracion/components/_table.html` (Estructura de tabla y filtros `tfoot`)
    - `administracion/templates/administracion/components/_table_result.html` (Cuerpo de la tabla, filas dinámicas)
    - `administracion/templates/administracion/components/_form.html` (Formulario de creación dinámico)
    - `administracion/templates/administracion/components/_filters.html` (Buscador superior y acciones)
    - `administracion/templates/administracion/components/_pagination.html` (Paginación genérica)

---

## 2. Cómo implementar un nuevo Mantenedor

Para crear un nuevo mantenedor (ejemplo: `Banco`), sigue estos pasos:

### Paso 1: Crear el Formulario de Creación (`forms/bancos.py`)
```python
from django import forms
from administracion.models import Banco

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ['nombre', 'codigo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
        }
```

### Paso 2: Crear el Formulario de Filtros (`filtros/bancos.py`)
```python
from django import forms

class BancoFilterForm(forms.Form):
    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Nombre...'}))
    codigo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Código...'}))
```

### Paso 3: Crear la Vista (`views/bancos.py`)
Hereda de `CRUDListMixin` y `ListView`.
```python
from django.views.generic import ListView
from administracion.mixin.crud_mixin import CRUDListMixin
from administracion.models import Banco
from administracion.forms.bancos import BancoForm
from administracion.filtros.bancos import BancoFilterForm

class BancoListView(CRUDListMixin, ListView):
    model = Banco
    template_name = 'administracion/index.html'
    paginate_by = 10

    # Configuración del Mixin
    list_display = ['id', 'nombre', 'codigo', 'active'] # Campos que se verán en la tabla
    search_fields = ['nombre', 'codigo']              # Campos para el buscador general
    filter_form_class = BancoFilterForm               # Formulario de filtros (tfoot)
    form_class = BancoForm                            # Formulario de creación (card)
    title = "Mantenedor de Bancos"
    list_url_name = "banco_list"                      # Nombre de la URL para redirecciones
```

### Paso 4: Configurar la URL (`urls.py`)
```python
path('bancos/', views.bancos.BancoListView.as_view(), name='banco_list'),
```

---

## 3. Características Principales

1.  **Detección Automática de Columnas:** El Mixin lee `list_display` y obtiene los nombres legibles (`verbose_name`) de los campos del modelo automáticamente.
2.  **Formulario en la misma Vista:** Permite crear registros sin salir de la lista. El formulario se oculta/muestra con el botón "Nuevo" y mantiene su estado (abierto/cerrado) mediante `localStorage`.
3.  **Filtrado Dual:** 
    - **Buscador General:** Usa HTMX para filtrar la tabla en tiempo real mientras escribes (configurado en `search_fields`).
    - **Filtros por Columna:** Usa el `filter_form_class` para búsquedas específicas en el pie de la tabla.
4.  **Paginación Inteligente:** Mantiene los parámetros de búsqueda al cambiar de página.
5.  **Asignación Automática:** El Mixin asigna automáticamente `establecimiento`, `created_by` y `updated_by` basándose en el usuario autenticado (`request.user`), por lo que no es necesario incluirlos en los formularios de creación.
6.  **Extensibilidad:** Puedes sobreescribir métodos como `get_queryset` o `get_context_data` en la vista si necesitas lógica personalizada.
