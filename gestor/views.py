from pprint import PrettyPrinter
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import InscriptoForm

from .models import Inscripto, Curso
from .tables import InscriptosTable, CursosTable


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


def inscriptos_list(request, sort='id'):
    if request.user.is_authenticated:
        raw_fields = Inscripto._meta.get_fields()
        fields = [f.name for f in raw_fields]
        if 'sort' in request.GET: 
            abs_sort_val = request.GET['sort'].replace("-","")
            if abs_sort_val in fields: 
               sort = request.GET['sort'] 

        #print( '[%s]' % ', '.join( map( str, fields) ) )

        queryset = Inscripto.objects.all().order_by(sort)
        table = InscriptosTable(queryset)
        return render(request, 'tabla.html', {'table': table})
    else:
        return HttpResponse('No estas registrado!')

def cursos_list(request, sort='id'):
    if request.user.is_authenticated:
        raw_fields = Curso._meta.get_fields()
        fields = [f.name for f in raw_fields]
        if 'sort' in request.GET: 
            abs_sort_val = request.GET['sort'].replace("-","")
            if abs_sort_val in fields: 
               sort = request.GET['sort'] 

        queryset = Curso.objects.all().order_by(sort)
        for curso in queryset:
            inscriptos = curso.ver_inscriptos()
            print(inscriptos)

        table = CursosTable(queryset)
        return render(request, 'tabla.html', {'table': table})
    else:
        return HttpResponse('No estas registrado!')
