from django.forms import ModelForm
from .models import Inscripto, Curso

class InscriptoForm(ModelForm):
    class Meta:
        model = Inscripto
        exclude = ['pago','inscripcion_fecha']

class CursoForm(ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
