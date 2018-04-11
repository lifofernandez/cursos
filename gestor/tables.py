import django_tables2 as tables
from  django_tables2.utils import A
from  .models import Inscripto

class InscriptosTable(tables.Table):
    #id = tables.LinkColumn('inscripto_detalles', text='static text', args=[A('id')])
    id = tables.LinkColumn('inscripto_detalles',  args=[A('id')])
    class Meta:
        model = Inscripto
        exclude = ['subscripcion','enterado']
        attrs = {'class': 'table table-striped table-bordered table-hover table-sm'}
        ordering = ('pago',)
