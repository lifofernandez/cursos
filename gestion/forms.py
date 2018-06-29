from django.forms import ModelForm
from django import forms
from django.utils import timezone
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
    inicio_hora = forms.TimeField(
        widget = forms.TimeInput( 
            #format='%H:%M',
            attrs={
                'type':'time',
                'value' : '20:20',
            },
        ),
    )
    finalizacion_hora = inicio_hora
    class Meta:
        model = Curso
        fields = '__all__'
