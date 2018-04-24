import django_tables2 as tables
from  django_tables2.utils import A
from  .models import Inscripto, Curso

# Columna custom, extrae el label para una opcion en un ForeingKey
class LabelColumn(tables.Column):
    def render(self,value):
        #pepe = Inscripto.objects.values('alumno_una')
        CHOICES = Inscripto._meta.get_field('alumno_una').choices
        opciones = {}
        for choice in CHOICES :
            opciones[choice[1]] = choice[0]
        label = opciones[value]
        return label

class InscriptosTable(tables.Table):
    #id = tables.LinkColumn('inscripto_detalles', text='static text', args=[A('id')])

    nombre = tables.Column()
    apellido = tables.Column()
    curso = tables.Column('Curso')
    inscripcion_fecha = tables.DateColumn(verbose_name='Fecha')
    pago = tables.Column()
    condicion = LabelColumn('Condición',accessor='alumno_una')
    recibo = tables.LinkColumn('inscripto_recibo',text='recibo',  args=[A('id')])
    id = tables.LinkColumn('inscripto_detalles',  args=[A('id')],verbose_name='Editar')

    class Meta:
        model = Inscripto
        #exclude = ['subscripcion','enterado']
        fields  = [ 'apellido','nombre','curso','inscripcion_fecha','pago']

        attrs = {'class': 'table table-striped table-hover table-sm'}
        #ordering = ('pago',)

class CursosTable(tables.Table):
    nombre = tables.Column('Nombre')
    codigo = tables.Column('Código')
    inicio_fecha = tables.DateColumn(verbose_name='Inicio')
    inscripcion_abierta = tables.BooleanColumn(verbose_name='Inscripcion')
    planilla = tables.LinkColumn('curso_planilla',text='planilla',  args=[A('id')])
    id = tables.LinkColumn('curso_detalles',  args=[A('id')],verbose_name='Editar')
    class Meta:
        model = Curso
        fields = ['nombre','docente','inicio_fecha','inscripcion_abierta','codigo'] 
        attrs = {'class': 'table table-striped table-hover table-sm' }

class InscriptosXCursosTable(tables.Table):
    nombre = tables.Column()
    apellido = tables.Column()
    #curso = tables.Column('Curso')
    inscripcion_fecha = tables.DateColumn(verbose_name='Fecha')
    pago = tables.Column()
    condicion = LabelColumn('Condición',accessor='alumno_una')
    recibo = tables.LinkColumn('inscripto_recibo',text='recibo',  args=[A('id')])
    id = tables.LinkColumn('inscripto_detalles',  args=[A('id')],verbose_name='Editar')

    class Meta:
        #attrs = {'class': 'table table-striped table-bordered table-hover table-sm'}
        attrs = {'class': 'table table-striped table-hover table-sm' }


