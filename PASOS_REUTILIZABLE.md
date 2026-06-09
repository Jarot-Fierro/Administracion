# Guía para Crear y Empaquetar tu Aplicación Reutilizable

Este documento detalla los pasos necesarios para convertir tu aplicación `administracion` en un paquete instalable de Python/Django.

## 1. Preparación de la Estructura
Asegúrate de tener los siguientes archivos en la raíz de tu proyecto:
- `README.rst`: Descripción e instrucciones de instalación.
- `pyproject.toml`: Configuración del sistema de construcción y dependencias.
- `MANIFEST.in`: Define qué archivos no-Python (plantillas, estáticos) se deben incluir.
- `LICENSE` (Recomendado): Un archivo de texto con la licencia (ej. MIT o BSD).

## 2. Pasos para Generar el Paquete

### A. Instalar herramientas de construcción
Asegúrate de tener instalada la última versión de `build`:
```powershell
python -m pip install --upgrade build
```

### B. Construir el paquete
Desde la raíz del proyecto (donde está el archivo `pyproject.toml`), ejecuta:
```powershell
python -m build
```
Esto creará una carpeta llamada `dist/` que contiene:
- Un archivo `.tar.gz` (distribución de código fuente).
- Un archivo `.whl` (archivo de rueda o "wheel").

## 3. Instalación en otro proyecto

### Opción 1: Instalación Local
Para probarlo en otro proyecto localmente, navega a la carpeta de ese proyecto y ejecuta:
```powershell
pip install C:/ruta/a/tu/proyecto/dist/django-administracion-generica-0.1.0.tar.gz
```

### Opción 2: Instalación vía Git
Si subes tu código a un repositorio (ej. GitHub), puedes instalarlo directamente:
```powershell
pip install git+https://github.com/tu-usuario/nombre-del-repo.git
```

## 4. Configuración en el Proyecto Destino

1. **Añadir a INSTALLED_APPS:**
   ```python
   INSTALLED_APPS = [
       ...,
       'django_htmx',
       'administracion',
   ]
   ```

2. **Configurar URLs:**
   En el `urls.py` principal del nuevo proyecto:
   ```python
   path('administracion/', include('administracion.urls')),
   ```

3. **Migraciones:**
   ```powershell
   python manage.py migrate
   ```

## 5. Mantenimiento
Cada vez que realices cambios y quieras generar una nueva versión:
1. Incrementa el número de `version` en `pyproject.toml`.
2. Borra la carpeta `dist/` anterior.
3. Vuelve a ejecutar `python -m build`.
