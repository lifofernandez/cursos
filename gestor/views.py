from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import InscriptoForm

from .models import Inscripto
from .tables import InscriptosTable


def index(request):
    return HttpResponse('Hello, world.')

def inscripcion(request):
    if request.method == 'POST':
        form = InscriptoForm(request.POST)
        if form.is_valid():
            inscripto_item = form.save(commit=False)
            inscripto_item.save()
            return HttpResponse('LISTO ISCRITO!!!.')
    else:
        form = InscriptoForm()
        # ATENCION: el carpeta contenedora el teplate debe ser declarada
        # en TEMPLATES.DIRS en el fichero gestor/settings.py 
        return render(request, 'inscripcion.html', {'form':form})


def inscriptos_list(request):
    queryset = Inscripto.objects.all()
    table = InscriptosTable(queryset)
    return render(request, 'inscriptos_list.html', {'table': table})
