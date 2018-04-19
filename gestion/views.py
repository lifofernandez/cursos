import datetime
from django.utils import timezone

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import InscriptoForm

from .models import Inscripto, Curso
from .tables import InscriptosTable, CursosTable, InscriptosXCursosTable


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
        # en TEMPLATES.DIRS en el fichero gestion/settings.py 
        return render(request, 'inscripcion.html', {'form':form})


def inscriptos(request, sort='id'):
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

def cursos(request, sort='inicio_fecha'):
    if request.user.is_authenticated:
        raw_fields = Curso._meta.get_fields()
        fields = [f.name for f in raw_fields] 
        if 'sort' in request.GET:
            abs_sort_val = request.GET['sort'].replace("-","") 
            if abs_sort_val in fields:
                sort = request.GET['sort']

        pasados = Curso.objects.all().filter(
            inicio_fecha__lte=timezone.now()
        ).order_by(sort) 
        futuros = Curso.objects.all().filter(
            inicio_fecha__gte=timezone.now()
        ).order_by(sort) 

        vigentes = {} 
        vigentes['titulo'] = 'Cursos'
        vigentes['subtitulo'] = 'Vigentes'
        vigentes['items'] = CursosTable(futuros) 

        anteriores =  {}
        anteriores['titulo'] = 'Cursos'
        anteriores['subtitulo'] = 'Anteriores'
        anteriores['items'] = CursosTable(pasados) 

        TABLAS = [
                vigentes,
                anteriores,
        ]
    #    return render(request, 'tabla.html', {'table': table})


        return render(request, 'multitabla.html', {'tables':TABLAS})
    else:
        return HttpResponse('No estas registrado!')

def inscriptosxcursos(request, sort='id'): 
    if request.user.is_authenticated:

        queryset = Curso.objects.all().order_by(sort)

        cursos = [] 
        for index, curso in enumerate(queryset): 
            c = {}
            c['titulo'] = queryset[index].nombre
            c['subtitulo'] = queryset[index].docente

            #queryset[index].inscriptos = inscriptos 
            INSCRIPTOS = []
            inscriptos = curso.obtener_inscriptos()

            #for index, inscripto in enumerate(inscriptos): 
            #    i = {}
            #    i['nombre'] = inscriptos.values('nombre') 
            #    INSCRIPTOS.append(i)

            INSCRIPTOS = InscriptosXCursosTable(inscriptos) 
            c['items'] = INSCRIPTOS

            cursos.append(c)

        CURSOS = cursos 

        #print(CURSOS[1].nombre)
        #print(queryset.values('inscripto'))
        #print(queryset[1].inscriptos.values('nombre'))

        return render(request, 'multitabla.html', {'tables':CURSOS})
    else:
        return HttpResponse('No estas registrado!')

from reportlab.pdfgen import canvas

def pdftest(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its file.
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, 'Hello world.')

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

