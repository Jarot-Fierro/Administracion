from django.db import models
from simple_history.models import HistoricalRecords

from administracion.models.core import StandardModel


class Departamento(StandardModel):
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField()
    email_contacto = models.EmailField(blank=True)

    history = HistoricalRecords()

    UPPERCASE_FIELDS = ['nombre', ]
    LOWERCASE_FIELDS = ['email_contacto',]

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre']
