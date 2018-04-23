import django_tables2 as tables
from  django_tables2.utils import A
from  .models import Inscripto, Curso

class InscriptosTable(tables.Table):
    #id = tables.LinkColumn('inscripto_detalles', text='static text', args=[A('id')])
    id = tables.LinkColumn('inscripto_detalles',  args=[A('id')])
    recibo = tables.LinkColumn('inscripto_recibo',text='recibo',  args=[A('id')])
    class Meta:
        model = Inscripto
        exclude = ['subscripcion','enterado']
        attrs = {'class': 'table table-striped table-bordered table-hover table-sm'}
        #ordering = ('pago',)

class CursosTable(tables.Table):
    id = tables.LinkColumn('curso_detalles',  args=[A('id')])
    class Meta:
        model = Curso
        fields = ['id','nombre','docente','inicio_fecha','inscripcion_abierta','codigo'] 
        attrs = {'class': 'table table-striped table-bordered table-hover table-sm'}

class InscriptosXCursosTable(tables.Table):
    nombre = tables.Column()
    apellido = tables.Column()
    pago = tables.Column()

    class Meta:
        attrs = {'class': 'table table-striped table-bordered table-hover table-sm'}
