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

        INSCRIPTOS = Inscripto.objects.all().order_by(sort)
        table = InscriptosTable(INSCRIPTOS) 
        #print(table.columns['curso'].header)
        return render(request, 'tabla.html', {'titulo':'Todos los inscriptos','table': table})
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

        futuros = Curso.objects.all().filter(
            inicio_fecha__gte = timezone.now()
        ).order_by(sort) 
        pasados = Curso.objects.all().filter(
            inicio_fecha__lte = timezone.now() - timezone.timedelta(days=1)
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


        return render(request, 'multitabla.html', {'titulo':'Todos los Cursos','tables':TABLAS})
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

        return render(request, 'multitabla.html', {'titulo':'Inscriptos a cada curso','tables':CURSOS})
    else:
        return HttpResponse('No estas registrado!')

from reportlab.pdfgen import canvas

def inscripto_recibo(request, id):
    if request.user.is_authenticated:
        
        #id = 1
        if not id:
            return HttpResponse('Dame un ID!')

        inscripto = Inscripto.objects.filter(id=id)
        nombre = inscripto[0].nombre
        apellido = inscripto[0].apellido 

        alumno_una = inscripto[0].alumno_una

        pago = inscripto[0].pago
        costo = inscripto[0].curso.costo
        curso = inscripto[0].curso

        descuento = inscripto[0].descuento()
        abona = inscripto[0].abona()


        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="inscripcion_'+curso.codigo+'-'+apellido+'_'+nombre+'.pdf"'

        # Create the PDF object, using the response object as its file.
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(
                100, 
                200, 
                'El estudiante: ' +
                nombre + 
                ' ' + 
                apellido
        )
        p.drawString(
                100, 
                175, 
                'abona: $' + 
                str(abona) 
        )
        if alumno_una != 'no':
            if alumno_una != 'multimedia':
                condicion = 'Alumno de La U.N.A'
            if alumno_una == 'multimedia':
                condicion = 'Alumno de A.T.A.M'
            p.drawString(
                    100, 
                    150, 
                    'gracias a un descuento de %' + 
                    str( 100 * descuento ) +
                    ' por su condicion de ' + 
                    condicion
            )

        p.drawString(
                100, 
                125, 
                'En concepto de matriculacion al curso: ' + 
                curso.nombre  
        )
        p.drawString(
                100, 
                100, 
                'cuyo costo es: $' + 
                str(costo) +
                '.' 
        )

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response

    else:
        return HttpResponse('No estas registrado!')

def curso_planilla(request, id):
    if request.user.is_authenticated:
        
        #id = 1
        if not id:
            return HttpResponse('Dame un ID!')

        curso = Curso.objects.filter(id=id)
        nombre = curso [0].nombre
        codigo = curso [0].codigo 
        docente = str(curso [0].docente )

        costo = str(curso[0].costo)

        INSCRIPTOS = []
        inscriptos = curso[0].obtener_inscriptos()

        #INSCRIPTOS = InscriptosXCursosTable(inscriptos) 
        #c['items'] = INSCRIPTOS



        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="planilla-'+codigo+'-'+docente+'.pdf"'

        # Create the PDF object, using the response object as its file.
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        for index, inscripto in enumerate(inscriptos):
            p.drawString(
                    100, 
                    160 + ( index * 10 ), 
                    str( len(inscriptos) - index )+
                    ' ' +
                    inscripto.apellido +
                    ' ' +
                    inscripto.nombre + 
                    ' -- ' +
                    inscripto.correo +
                    ' -- ' +
                    inscripto.dni

            )

        p.drawString(
                100, 
                130, 
                'Curso: ' +
                nombre 
        )
        p.drawString(
                100, 
                120, 
                'Codigo: ' +
                codigo
        )
        p.drawString(
                100, 
                110, 
                'Docente: ' +
                docente
        )
        p.drawString(
                100, 
                100, 
                'Costo: $' +
                costo
        )

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response

    else:
        return HttpResponse('No estas registrado!')
