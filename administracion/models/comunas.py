from django.db import models
from simple_history.models import HistoricalRecords

from administracion.models.core import StandardModel


class Comuna(StandardModel):
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField(unique=True)

    history = HistoricalRecords()

    UPPERCASE_FIELDS = ['nombre', ]

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'
        ordering = ['nombre']
