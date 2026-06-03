from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords


class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('JEFATURA', 'Jefatura'),
        ('RRHH', 'Recursos Humanos'),
        ('FINANZAS', 'Finanzas'),
        ('FUNCIONARIO', 'Funcionario'),
        ('VISUALIZADOR', 'Solo Visualización'),
    ]

    funcionario = models.OneToOneField('administracion.Funcionario', on_delete=models.CASCADE, null=True, blank=True)
    establecimiento = models.ForeignKey('administracion.Establecimiento', on_delete=models.CASCADE, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='FUNCIONARIO')

    history = HistoricalRecords()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-id']
