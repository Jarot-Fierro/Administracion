from django.db import models
from simple_history.models import HistoricalRecords

from administracion.models.core import StandardModel


class Funcionario(StandardModel):
    rut = models.CharField(max_length=13)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    calidad_juridica = models.ForeignKey('administracion.CalidadJuridica', on_delete=models.SET_NULL, null=True)
    departamento = models.ForeignKey('administracion.Departamento', on_delete=models.SET_NULL, null=True)
    comuna_residencia = models.ForeignKey('administracion.Comuna', on_delete=models.SET_NULL, null=True)
    banco = models.ForeignKey('administracion.Banco', on_delete=models.SET_NULL, null=True)
    numero_cuenta = models.CharField(max_length=25, blank=True)
    tipo_cuenta = models.CharField(max_length=20, blank=True)
    cargo = models.CharField(max_length=250)
    grado = models.CharField(max_length=10, blank=True)
    horas_contrato = models.IntegerField(null=True, blank=True)

    history = HistoricalRecords()

    UPPERCASE_FIELDS = ['nombres', 'apellido_paterno', 'apellido_materno', 'cargo', 'grado', 'numero_cuenta',
                        'tipo_cuenta',]
    LOWERCASE_FIELDS = ['email',]

    def __str__(self):
        return self.nombres

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'
        ordering = ['nombres']
