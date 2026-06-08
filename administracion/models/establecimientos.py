from django.db import models
from simple_history.models import HistoricalRecords

from administracion.models.core import StandardModelOnly


class Establecimiento(StandardModelOnly):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20, unique=True)
    region = models.CharField(max_length=100, blank=True)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email_contacto = models.EmailField(blank=True)

    history = HistoricalRecords()

    UPPERCASE_FIELDS = ['nombre', 'region', 'direccion', ]
    LOWERCASE_FIELDS = ['email_contacto',]

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Establecimiento'
        verbose_name_plural = 'Establecimientos'
        ordering = ['nombre']
