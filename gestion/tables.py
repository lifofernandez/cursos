import django_tables2 as tables
from  django_tables2.utils import A
from  .models import Inscripto, Curso

class InscriptosTable(tables.Table):
    #id = tables.LinkColumn('inscripto_detalles', text='static text', args=[A('id')])
    id = tables.LinkColumn('inscripto_detalles',  args=[A('id')])
    recibo = tables.LinkColumn('inscripto_recibo',text='recibo',  args=[A('id')])

    nombre = tables.Column()
    apellido = tables.Column()
    curso = tables.Column('Curso')
    pago = tables.Column()
    inscripcion_fecha = tables.DateColumn()
    alumno_una = tables.Column('Condición')
    class Meta:
        model = Inscripto
        #exclude = ['subscripcion','enterado']
        fields  = [ 'apellido','nombre','curso','inscripcion_fecha','pago','alumno_una']

        attrs = {'class': 'table table-striped table-hover table-sm'}
        #ordering = ('pago',)

class CursosTable(tables.Table):
    id = tables.LinkColumn('curso_detalles',  args=[A('id')])
    class Meta:
        model = Curso
        fields = ['id','nombre','docente','inicio_fecha','inscripcion_abierta','codigo'] 
        attrs = {'class': 'table table-striped table-hover table-sm' }

class InscriptosXCursosTable(tables.Table):
    nombre = tables.Column()
    apellido = tables.Column()
    curso = tables.Column('Curso')
    pago = tables.Column()
    inscripcion_fecha = tables.DateColumn()
    alumno_una = tables.Column('Condición')

    class Meta:
        #attrs = {'class': 'table table-striped table-bordered table-hover table-sm'}
        attrs = {'class': 'table table-striped table-hover table-sm' }


