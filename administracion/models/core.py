from django.conf import settings
from django.db import models


class StandardModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="%(class)s_created", verbose_name='Creado por')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="%(class)s_updated", verbose_name='Actualizado por')

    establecimiento = models.ForeignKey('administracion.Establecimiento', on_delete=models.CASCADE)

    active = models.BooleanField(default=True, verbose_name='Activo')

    UPPERCASE_FIELDS = []
    LOWERCASE_FIELDS = []

    def save(self, *args, **kwargs):
        # Campos a MAYÚSCULAS
        for field_name in self.UPPERCASE_FIELDS:
            value = getattr(self, field_name, None)
            if value:
                setattr(self, field_name, value.upper())

        # Campos a minúsculas (ej: email)
        for field_name in self.LOWERCASE_FIELDS:
            value = getattr(self, field_name, None)
            if value:
                setattr(self, field_name, value.lower())

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class StandardModelOnly(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="%(class)s_created_only", verbose_name='Creado por')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="%(class)s_updated_only", verbose_name='Actualizado por')

    active = models.BooleanField(default=True, verbose_name='Activo')

    UPPERCASE_FIELDS = []
    LOWERCASE_FIELDS = []

    def save(self, *args, **kwargs):
        # Campos a MAYÚSCULAS
        for field_name in self.UPPERCASE_FIELDS:
            value = getattr(self, field_name, None)
            if value:
                setattr(self, field_name, value.upper())

        # Campos a minúsculas (ej: email)
        for field_name in self.LOWERCASE_FIELDS:
            value = getattr(self, field_name, None)
            if value:
                setattr(self, field_name, value.lower())

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
