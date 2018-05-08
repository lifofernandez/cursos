import datetime

from django.db import models
from django.db.models import Q
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

    codigo = models.CharField(
        verbose_name='Código del Curso',
        max_length=20,
        blank=True,
        editable=False,
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

    inicio_fecha = models.DateField(
        'Fecha de Inicio',
        default=timezone.now
    )

    periodo = models.CharField(
        verbose_name='Perdiodo del Curso',
        max_length=10,
        blank=True,
        editable=False,
    )

    dias = models.ManyToManyField(
        Dia,
        verbose_name='Días de Dictado'
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
        blank=True,
    )

    inscripcion_abierta = models.BooleanField(
        verbose_name='Inscripción Abierta',
        default=1
    )

    def __str__(self):
        return self.nombre

    def obtener_inscriptos(self):
        # TO DO: sort, pasar value para ordenar comoa argumento
        inscriptos = Inscripto.objects.filter( curso = self.id )
        return inscriptos 

    def liquidacion(self):
        inscriptos = self.obtener_inscriptos().filter(~Q(pago=0))
        
        pagan100 = inscriptos.filter( alumno_una='no' )
        pagan75 = inscriptos.filter( 
            ~Q(alumno_una='no') 
        ).filter(
            ~Q(alumno_una='multimedia' )
        ) 
        pagan50 = inscriptos.filter( alumno_una='multimedia' )

        total100 = len(pagan100) * self.costo
        total75  = len(pagan75) * (self.costo * .75)
        total50  = len(pagan50) * (self.costo * .5)
        #esperado = total100 + total75 + total50

        pagaron = sum( [inscripto.pago for inscripto in inscriptos] )
        exclusivo_docente = self.costo * 3

        monto_docente = pagaron
        monto_atam = 0
        if( pagaron > exclusivo_docente ):
            resto_a_repartir = pagaron - exclusivo_docente
            monto_docente = exclusivo_docente + ( resto_a_repartir * .5 ) 
            monto_atam = resto_a_repartir * .5 

        liquidacion = {
            'curso':          self.id,
            'arancel':        self.costo,
            'cant100':        len( pagan100 ),
            'total100':       total100,
            'cant75':         len( pagan75 ),
            'total75':        total75,
            'cant50':         len( pagan50 ),
            'total50':        total50,
            #'total_esperado': esperado,
            'total_pagaron':  pagaron ,
            'monto_docente':  monto_docente,
            'monto_ATAM':     monto_atam,
        }
        return liquidacion

    # Override de la funcion "save" de Model
    def save(self, *args, **kwargs):
        año = self.inicio_fecha.year
        mes = self.inicio_fecha.month
        semestre = 1
        if mes > 5:
            semestre = 2
        periodo = str(año) + '.' + str(semestre)
        if self.periodo != periodo:
            self.periodo = periodo


        # Obtener Sigla 
        iniciales = self.nombre
        if len( iniciales ) > 2:
            NOMBRE = iniciales.split(' ')
            if len( NOMBRE ) == 1:
                iniciales = NOMBRE[0][:3]
            if len( NOMBRE ) == 2:
                iniciales = NOMBRE[0][:2] + NOMBRE[1][:1]
            if len( NOMBRE ) == 3:
                iniciales = ''.join( [ palabra[0] for palabra in NOMBRE ] )
            if len( NOMBRE ) >= 4:
                iniciales = ''.join( [ palabra[0] for palabra in NOMBRE if palabra[0].isupper() ] )
                if len( iniciales ) < 3:
                   iniciales = ''.join( [ palabra[0] for palabra in NOMBRE if len( palabra ) > 3 ] )
                   if len( iniciales ) < 3:
                      iniciales = ''.join( [ palabra[0] for palabra in NOMBRE ] )
        sigla = iniciales[:3].upper()

        # armar codigo con sigla + periodo
        codigo = sigla + periodo
        if self.codigo != codigo:
            self.codigo = codigo 

        super(Curso, self).save(*args, **kwargs)

class Inscripto(models.Model):
    curso = models.ForeignKey(
        Curso,
        limit_choices_to={'inscripcion_abierta':True},
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

    correo = models.EmailField(
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
        return self.nombre+' '+self.apellido

    def fue_creado_recientemente(self):
        return self.inscripcion_fecha >= timezone.now() - datetime.timedelta(days=1)

    def descuento(self):
        condicion = self.alumno_una
        descuento = .75
        if condicion == 'no':
            descuento = 1
        if condicion == 'multimedia':
            descuento = .5
        return descuento

    def abona(self):
        descuento = self.descuento()
        costo = self.curso.costo
        abona = costo * float(descuento)
        return abona
        

