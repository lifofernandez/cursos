from django.forms import ModelForm
from .models import Inscripto

class InscriptoForm(ModelForm):
    class Meta:
        model = Inscripto
        #fields = '__all__'
        exclude = ['pago','inscripcion_fecha']
