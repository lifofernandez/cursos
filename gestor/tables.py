from  django_tables2 import tables
from  .models import Inscripto

class InscriptosTable(tables.Table):
    class Meta:
        model = Inscripto
        attrs = {'class': 'table table-striped table-bordered table-hover table-sm'}
        ordering = ('pago',)
