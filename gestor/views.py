from pprint import PrettyPrinter
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import InscriptoForm

from .models import Inscripto, Curso
from .tables import InscriptosTable, CursosTable, InscriptosCursosTable


from django_tables2 import MultiTableMixin

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
        table = CursosTable(queryset) 
        return render(request, 'tabla.html', {'table': table})
    else:
        return HttpResponse('No estas registrado!')

def inscriptos_cursos_list(request, sort='id'): 
    if request.user.is_authenticated:

        queryset = Curso.objects.all().order_by(sort)

        cursos = [] 
        for index, curso in enumerate(queryset): 
            c = {}
            c['nombre'] = queryset[index].nombre
            c['docente'] = queryset[index].docente

            #queryset[index].inscriptos = inscriptos 
            INSCRIPTOS = []
            inscriptos = curso.ver_inscriptos()

            #for index, inscripto in enumerate(inscriptos): 
            #    i = {}
            #    i['nombre'] = inscriptos.values('nombre') 
            #    INSCRIPTOS.append(i)

            INSCRIPTOS = InscriptosCursosTable(inscriptos) 
            c['inscriptos'] = INSCRIPTOS

            cursos.append(c)

        CURSOS = cursos 

        #print(CURSOS[1].nombre)
        #print(queryset.values('inscripto'))
        #print(queryset[1].inscriptos.values('nombre'))


        #curso2 = [
        #        {'nombre': 'Bradley','docente': 'Forves'},
        #        {'nombre': 'Perro','docente': 'Ooeeo'},
        #        {'nombre': 'Gato','docente': 'MAcri'},
        #]

        #table2 = InscriptosCursosTable(curso2)
        #tables = [
        #    CURSOS,
        #    table2,
        #]
        
        return render(request, 'multitabla.html', {'cursos':CURSOS})
    else:
        return HttpResponse('No estas registrado!')

