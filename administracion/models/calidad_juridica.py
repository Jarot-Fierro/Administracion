from django.db import models
from simple_history.models import HistoricalRecords

from administracion.models.core import StandardModel


class CalidadJuridica(StandardModel):
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=20, blank=True)

    history = HistoricalRecords()

    UPPERCASE_FIELDS = ['nombre', ]

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Calidad Jurídica'
        verbose_name_plural = 'Calidades Jurídicas'
        ordering = ['nombre']
