import django_tables2 as tables
from  django_tables2.utils import A
from  .models import Inscripto, Curso

# Columna custom, extrae el label para una opcion en un ForeingKey
class LabelColumn(tables.Column):
    def render(self, value):
        CHOICES = Inscripto._meta.get_field('alumno_una').choices
        opciones = {}
        for choice in CHOICES :
            opciones[ choice[1] ] = choice[0]
        label = opciones[value]
        return label

class CantidadInscriptosColumn(tables.Column):
    def render(self, value):
        curso = Curso.objects.filter(id=value)[0]
        cantidad_inscriptos = len(curso.inscriptos)
        return cantidad_inscriptos

class CursosTable(tables.Table):
    id = tables.Column('#')
    nombre = tables.Column('Nombre')
    codigo = tables.Column('Código')
    # to do: cantidad de inscriptos
    # total_inscriptos = tables.Column('Inscriptos')
    inicio_fecha = tables.DateColumn(verbose_name='Inicio')

    inscriptos = CantidadInscriptosColumn(
        verbose_name='Inscriptos',
        accessor='id'
    )

    inscripcion_abierta = tables.BooleanColumn(verbose_name='Inscripcion')
    planilla = tables.LinkColumn(
        'curso_planilla',
        text='planilla',
        args=[A('id')],
        verbose_name='Obtener',
        orderable=False,
        exclude_from_export = True
    )
    clonar = tables.LinkColumn(
        'curso_clonar',
        text='clonar curso',
        args=[A('id')],
        verbose_name='Clonar',
        orderable = False,
        exclude_from_export = True
    )
    editar = tables.LinkColumn(
        'curso_editar',
        text='editar curso',
        args=[A('id')],
        verbose_name='Editar',
        orderable = False,
        exclude_from_export = True
    )
    #editar = tables.LinkColumn(
    #    'curso_detalles',
    #    text='editar curso',
    #    args=[A('id')],
    #    verbose_name='Editar',
    #    exclude_from_export = True
    #)

    class Meta:
        model = Curso
        fields = ['id','nombre','docente','inicio_fecha','inscripcion_abierta','codigo','modalidad'] 
        attrs = {'class': 'table table-striped table-hover table-sm' }

class InscriptosTable(tables.Table):
    id = tables.Column('#')
    apellido = tables.Column()
    nombre = tables.Column()
    curso = tables.Column('Curso')
    inscripcion_fecha = tables.DateColumn(verbose_name='Fecha')
    pago = tables.Column()
    alumno_una = LabelColumn(
        'Condición',
        accessor='alumno_una',
        #orderable=False,
    )
    recibo = tables.LinkColumn(
        'inscripto_recibo',
        text='recibo',
        args=[A('id')],
        verbose_name='Obtener',
        orderable=False,
        exclude_from_export = True
    )
    editar = tables.LinkColumn(
        'inscripto_editar',
        text='editar inscripto',
        args=[A('id')],
        verbose_name='Editar',
        orderable = False,
        exclude_from_export = True
    )
    #editar = tables.LinkColumn(
    #    'inscripto_detalles',
    #    text='editar inscripto',
    #    args=[A('id')],
    #    verbose_name='Editar',
    #    orderable=False,
    #    exclude_from_export = True
    #)

    class Meta:
        model = Inscripto
        #exclude = ['subscripcion','enterado']
        fields  = [ 'id','apellido','nombre','curso','inscripcion_fecha','pago']
        attrs = {'class': 'table table-striped table-hover table-sm'}


class InscriptosXCursosTable(tables.Table):
    id = tables.Column('#')
    apellido = tables.Column()
    nombre = tables.Column()
    # curso = tables.Column('Curso')
    inscripcion_fecha = tables.DateColumn(verbose_name='Fecha')
    pago = tables.Column()
    condicion = LabelColumn('Condición',accessor='alumno_una')
    recibo = tables.LinkColumn(
        'inscripto_recibo',
        text='recibo',  
        args=[A('id')],
        verbose_name='Obtener',
        orderable=False,
        exclude_from_export = True
    )
    editar = tables.LinkColumn(
        #'curso_detalles',
        'inscripto_detalles',
        text='editar inscripto',
        args=[A('id')],
        verbose_name='Editar',
        exclude_from_export = True
    )

    class Meta:
        #attrs = {'class': 'table table-striped table-bordered table-hover table-sm'}
        attrs = {'class': 'table table-striped table-hover table-sm' }

class LiquidacionesTable(tables.Table):

    arancel        = tables.Column()
    cant100        = tables.Column()
    cant75         = tables.Column()
    cant50         = tables.Column()
    #total_esperado = tables.Column()
    total_pagaron  = tables.Column('Total')
    monto_docente  = tables.Column()
    monto_ATAM     = tables.Column()
    descargar = tables.LinkColumn(
        'curso_liquidacion',
        text='liquidación', 
        args=[A('curso')],
        orderable=False,
        exclude_from_export = True
    )

    class Meta:
        #attrs = {'class': 'table table-striped table-bordered table-hover table-sm'}
        attrs = {'class': 'table table-striped table-hover table-sm' }

