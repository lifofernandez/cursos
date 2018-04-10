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

    inicio_fecha = models.DateField(
        'Fecha de Inicio',
        default=timezone.now
    )

    inicio_hora = models.TimeField(
        verbose_name='Hora de Inicio',
        default=timezone.now
    )

    finalizacion_hora= models.TimeField(
        verbose_name='Hora de Finalizaición',
        default=timezone.now
    )

    costo = models.IntegerField(
        verbose_name='Costo',
        default=0
    )

    requisitos = models.TextField(
        verbose_name='Requisitos',
        default=''
    )

    MODALIDADES = (
        ('v','Virtual'),
        ('p','Presencial'),
    )
    modalidad = models.CharField(
       max_length=1,
       choices=MODALIDADES,
       default='p',
       verbose_name='Modalidad',
    )

    imagen = models.ImageField(
        verbose_name='Imagen del Curso',
        upload_to='cursos_img',
        default=1
    )

    inscripcion_abierta = models.BooleanField(
        verbose_name='Inscripción Abierta',
        default=1
    )

    def __str__(self):
        return self.nombre

    def fue_creado_recientemente(self):
        return self.inicio_fecha >= timezone.now() - datetime.timedelta(days=1)

class Inscripto(models.Model):
    curso = models.ForeignKey(
        Curso,
        verbose_name='Curso al que se inscribe',
        on_delete=models.CASCADE
    )

    pago = models.IntegerField(
        verbose_name='Pagó',
        default=0
    )

    nombre = models.CharField(
        verbose_name='Nombre',
        max_length=200
    )

    apellido = models.CharField(
        verbose_name='Apellido',
        max_length=200
    )

    dni = models.CharField(
        verbose_name='D.N.I.',
        max_length=200
    )

    domicilio = models.CharField(
        verbose_name='Domicilio',
        max_length=200
    )

    correo = models.CharField(
        verbose_name='Correo Electrónico',
        max_length=200
    )

    telefono = models.CharField(
        verbose_name='Numero Telefónico',
        max_length=200
    )

    COMOS = (
        ('no','No soy alumno de la UNA'),
        ('multimedia','Licenciatura en Artes Multimediales'),
        ('actuacion','Licenciatura en Actuación'),
        ('audiovisuales','Licenciatura en Artes Audiovisuales'),
        ('musica','Licenciatura en Artes Musicales'),
        ('visuales','Licenciatura en Artes Visuales'),
        ('movimiento','Licenciatura en Composición Coreográfica'),
        ('restauracion','Licenciatura en Conservación y Restauración de Bienes Culturales'),
        ('critica','Licenciatura en Crítica de Artes'),
        ('curaduria','Licenciatura en Curaduría en Artes'),
        ('teatro','Licenciatura en Dirección Escénica'),
        ('iluminacion','Licenciatura en Diseño de Iluminación de Espectáculos'),
        ('escenografia','Licenciatura en Escenografía'),
        ('folclore','Licenciatura en Folklore'),
        ('profesorado','Profesorado de Arte'),
    )
    alumno_una = models.CharField(
        max_length=50,
        choices=COMOS,
        default='no',
        verbose_name='¿Es alumno de La U.N.A.?',
    )

    REFES = ( 
        ('redes_sociales','Redes Sociales (Facebook, Twitter, otra)'),
        ('mail','Newsletter/mailing'),
        ('cartelera','Cartelera de la universidad'),
        ('amigo','Recomendado por un amigo'),
        ('otro','Otros'),
    )

    enterado = models.CharField(
        max_length=50,
        choices=REFES,
        verbose_name='¿Como se enteró del curso?',
    )

    subscripcion = models.BooleanField(
        verbose_name='¿Desea recibir novedades?',
        default=1
    )

    inscripcion_fecha = models.DateField(
        verbose_name='Fecha de Inscripción',
        default=timezone.now
    )


    def __str__(self):
        return self.nombre+' '+self.apellido+' - Pagó: '+str(self.pago)+' - Curso: '+str(self.curso)

    def fue_creado_recientemente(self):
        return self.inscripcion_fecha >= timezone.now() - datetime.timedelta(days=1)


