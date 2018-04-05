import datetime

from django.db import models
from django.utils import timezone

# Aca creamos grupos de usuarios
# https://stackoverflow.com/questions/22250352
from django.contrib.auth.models import Group, User
new_group, created = Group.objects.get_or_create(name='docentes')

# Create your models here.

class Dia(models.Model):
    dia = models.CharField(max_length=20)
    #orden = models.IntegerField(default=0)

    def __str__(self):
       return self.dia
    class Meta:
       ordering = ('pk',)

class Curso(models.Model):
    # Nombre del curso
    nombre = models.CharField(max_length=200)
    # Usuarios dentro del grupo 'docentes'
    docente = models.ForeignKey(
        User,
        limit_choices_to={'groups__name':'docentes'},
        on_delete=models.CASCADE
    )
    # Texto acerca de los contenidos del curso
    descripcion = models.TextField(default='')

    #DAYS_OF_WEEK = (
    #    (0, 'Monday'),
    #    (1, 'Tuesday'),
    #    (2, 'Wednesday'),
    #    (3, 'Thursday'),
    #    (4, 'Friday'),
    #    (5, 'Saturday'),
    #    (6, 'Sunday')
    #)

    dias = models.ManyToManyField(Dia)

    creacion_fecha = models.DateTimeField('fecha de creación')

    def __str__(self):
        return self.nombre

    def fue_creado_recientemente(self):
        return self.creacion_fecha >= timezone.now() - datetime.timedelta(days=1)

