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
    inicio_fecha = forms.DateField(
        #widget = forms.DateInput( 
        #    #format='%d/%m/%Y',
        #    ##input_type='date',
        #    #attrs={
        #    #    'type':'date',
        #    #},
        #),
        widget=forms.SelectDateWidget(
            empty_label=(
                "Elegí un día",
                "Elegí un mes",
                "Elegí un año",

            ),
        ),
    )
    inicio_inscripcion = inicio_fecha
    fin_inscripcion = inicio_fecha

    inicio_hora = forms.TimeField(
        widget = forms.TimeInput( 
            format='%H:%M',
            attrs={
                'type':'time',
                #'value' : '20:20',
            },
        ),
    )
    finalizacion_hora = inicio_hora
    class Meta:
        model = Curso
        fields = '__all__'
#Form contains a file input, but is missing method=POST and enctype=multipart/form-data on the form.  The file will not be sent.
