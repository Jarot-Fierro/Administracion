======================
django-administracion
======================

django-administracion es una aplicación de Django que proporciona un sistema de CRUD genérico, mixins de abstracción y modelos base estandarizados para acelerar el desarrollo de mantenedores.

Documentación detallada en el directorio "docs".

Inicio rápido
------------

1. Añade "administracion" a tu configuración INSTALLED_APPS de esta manera::

    INSTALLED_APPS = [
        ...,
        "django_htmx",
        "administracion",
    ]

2. Incluye el URLconf de administracion en el archivo urls.py de tu proyecto de esta manera::

    path("administracion/", include("administracion.urls")),

3. Ejecuta ``python manage.py migrate`` para crear los modelos.

4. Inicia el servidor de desarrollo y visita el administrador para gestionar los datos.

Características
---------------

* CRUD Genérico mediante ``CRUDListMixin``.
* Modelos Base con auditoría automática.
* Integración con HTMX para búsquedas y filtrado dinámico.
* Componentes de frontend reutilizables.
