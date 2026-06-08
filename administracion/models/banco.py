from django.db import models
from simple_history.models import HistoricalRecords

from administracion.models.core import StandardModel


class Banco(StandardModel):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    website = models.URLField(blank=True)

    history = HistoricalRecords()

    UPPERCASE_FIELDS = ['nombre',]

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'

        ordering = ['nombre']
