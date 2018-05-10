from django.forms import ModelForm
from .models import Inscripto, Curso

class InscriptoForm( ModelForm ):
    class Meta:
        model = Inscripto
        exclude = ['pago','inscripcion_fecha']

class InscriptoEditForm( ModelForm ):
    class Meta:
        model = Inscripto
        fields = '__all__'

class InscriptoAcreditarForm( ModelForm ):
    class Meta:
        model = Inscripto
        fields = ['pago']

class CursoForm( ModelForm ):
    class Meta:
        model = Curso
        fields = '__all__'
