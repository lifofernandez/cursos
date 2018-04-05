import datetime

from django.db import models
from django.utils import timezone

# Aca creamos grupos de usuarios
# https://stackoverflow.com/questions/22250352
from django.contrib.auth.models import Group, User
new_group, created = Group.objects.get_or_create(name='docentes')

# MODELOS

# Este es un modelo (una especie de 'term')
# para usar en campo 'dias' en el modelo Curso.
# Estos 'dias' son cargados usando loaddata y fixtures
# https://docs.djangoproject.com/en/2.0/howto/initial-data/
class Dia(models.Model):
    
    dia = models.CharField(max_length=20)

    def __str__(self):
       return self.dia

    class Meta:
       ordering = ('pk',)

# Modelo para los cursos
class Curso(models.Model):
    # Nombre del curso
    nombre = models.CharField(
        verbose_name='Nombre del Curso',
        max_length=200
    )

    # Usuarios dentro del grupo 'docentes'
    docente = models.ForeignKey(
        User,
        verbose_name='Docente',
        limit_choices_to={'groups__name':'docentes'},
        on_delete=models.CASCADE
    )

    # Texto acerca de los contenidos del curso
    descripcion = models.TextField(
        'Descripción',
        default=''
    )

    dias = models.ManyToManyField(
        Dia,
        verbose_name='Días de Dictado'
    )

    creacion_fecha = models.DateTimeField('Fecha de Creación')

    def __str__(self):
        return self.nombre

    def fue_creado_recientemente(self):
        return self.creacion_fecha >= timezone.now() - datetime.timedelta(days=1)

