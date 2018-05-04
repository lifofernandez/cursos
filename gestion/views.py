import datetime
from django.utils import timezone

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from .forms import InscriptoForm

from .models import Inscripto, Curso
from .tables import InscriptosTable, CursosTable, InscriptosXCursosTable, LiquidacionesTable


# Table Export
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport


#from django_tables2 import MultiTableMixin

def index(request):
    return HttpResponse('Hello, world.')

def inscripcion(request):
    if request.method == 'POST':
        form = InscriptoForm(request.POST)
        if form.is_valid():
            inscripto_item = form.save(commit=False)
            inscripto_item.save()
            return HttpResponse(
                render( 
                    request,
                    'ok.html',
                    {
                        'titulo':'¡Inscripcion Satisfactoria!',
                        'bajada':'En breve nos comunicaremos a traves de los datos de contacto provistos.'
                    }
                )
            )
    else:
        form = InscriptoForm()
        # ATENCION: el carpeta contenedora el teplate debe ser declarada
        # en TEMPLATES.DIRS en el fichero gestion/settings.py 
        return render(
                request,
                'inscripcion.html', 
                {'titulo':'Inscripción a Cursos','form':form}
        )


def inscriptos(request, sort='id' ):
    if request.user.is_authenticated:
        raw_fields = Inscripto._meta.get_fields()
        fields = [f.name for f in raw_fields] 
        if 'sort' in request.GET: 
           abs_sort_val = request.GET['sort'].replace("-","")
           if abs_sort_val in fields: 
               sort = request.GET['sort'] 

        #print( '[%s]' % ', '.join( map( str, fields) ) )

        INSCRIPTOS = Inscripto.objects.all().order_by(sort)
        tabla = InscriptosTable(INSCRIPTOS) 

        RequestConfig(request).configure(tabla)

        if request.method == 'GET' and 'export' in request.GET:
            export_format = request.GET['export']
            print(export_format)
            if TableExport.is_valid_format(export_format):
                exporter = TableExport(export_format, tabla)
                return exporter.response('tabla.{}'.format(export_format))

        return render(
            request, 
            'tabla.html', 
            {
                'titulo':'Todos los inscriptos',
                #'bajada':'eo',
                'boton': {'texto':'Nuevo Inscripito','destino':'/inscripcion'},
                'tabla': tabla
            }
        )
    else: 
        #return HttpResponse('No estas registrado!')
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

def cursos(request, sort='inicio_fecha'):
    if request.user.is_authenticated:
        raw_fields = Curso._meta.get_fields()
        fields = [f.name for f in raw_fields] 

        if 'sort' in request.GET:
            abs_sort_val = request.GET['sort'].replace("-","") 
            if abs_sort_val in fields:
                sort = request.GET['sort']

        CURSOS = Curso.objects.all()

        futuros = CURSOS.filter(
            inicio_fecha__gte = timezone.now()
        ).order_by(sort) 
        pasados = CURSOS.filter(
            inicio_fecha__lte = timezone.now() - timezone.timedelta(days=1)
        ).order_by(sort) 

        vigentes = {} 
        vigentes['titulo'] = 'Cursos'
        vigentes['subtitulo'] = 'Vigentes'
        vigentes['items'] = CursosTable( futuros ) 

        anteriores =  {}
        anteriores['titulo'] = 'Cursos'
        anteriores['subtitulo'] = 'Anteriores'
        anteriores['items'] = CursosTable( pasados ) 

        TABLAS = [
                vigentes,
                anteriores,
        ]

        return render(
            request, 
            'multitabla.html',
            {
                'titulo':'Todos los Cursos',
                'bajada':'eo',
                'boton': {'texto':'Nuevo Curso','destino':'/admin/gestion/curso/add'},
                'tablas':TABLAS
            }
        )
    else:
        #return HttpResponse('No estas registrado!')
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

def inscriptosxcursos(request, sort='id'): 
    if request.user.is_authenticated:

        queryset = Curso.objects.all().order_by(sort)

        CURSOS = [] 
        for curso in queryset: 
            c = {}
            c['titulo'] = curso.nombre
            c['subtitulo'] = curso.docente

            INSCRIPTOS = []
            inscriptos = curso.obtener_inscriptos()

            INSCRIPTOS = InscriptosXCursosTable(inscriptos) 
            c['items'] = INSCRIPTOS

            CURSOS.append(c)

        return render(
            request, 
            'multitabla.html', 
            {'titulo':'Inscriptos a cada curso','tablas':CURSOS}
        )
    else:
        #return HttpResponse('No estas registrado!')
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

def liquidaciones(request, sort='id'): 
    if request.user.is_authenticated:

        queryset = Curso.objects.all().order_by(sort)

        CURSOS = [] 
        for curso in queryset: 
            inscriptos = curso.obtener_inscriptos()
            if inscriptos:
                c = {}
                c['titulo'] = curso.nombre
                c['subtitulo'] = curso.docente

                INSCRIPTOS = []
                INSCRIPTOS = InscriptosXCursosTable(inscriptos) 
                c['items'] = INSCRIPTOS


                liquidacion = {}
                liquidacion['titulo'] = 'Liquidacion' 
                liquidacion['subtitulo'] = curso.codigo

                calculo = curso.liquidacion()
                calculos = [calculo]
                CALCULOS = []
                CALCULOS = LiquidacionesTable(calculos) 
                liquidacion['items'] = CALCULOS 
                c['subtabla'] = liquidacion

                CURSOS.append(c)

        return render(
            request,
            'multitabla.html',
            {'titulo':'Liquidaciones','tablas':CURSOS}
        )
    else:
        #return HttpResponse('No estas registrado!')
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

# RECIBOS Y PLANILLAS PDF
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
                    str( 100 - ( 100 * descuento ) ) +
                    ' por su condicion de ' + 
                    condicion
            )

        p.drawString(
                100, 
                125, 
                'En concepto de: matriculacion al curso "' + 
                curso.nombre + '"' 
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
        #return HttpResponse('No estas registrado!')
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

def curso_planilla(request, id):
    if request.user.is_authenticated:
        
        #id = 1
        if not id:
            return HttpResponse('Dame un ID!')

        curso = Curso.objects.filter(id=id)
        nombre = curso[0].nombre
        codigo = curso[0].codigo 
        docente = str(curso[0].docente )

        costo = str(curso[0].costo)

        INSCRIPTOS = []
        inscriptos = curso[0].obtener_inscriptos()


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
        #return HttpResponse('No estas registrado!')
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

def curso_liquidacion(request, id):
    if request.user.is_authenticated:
        if not id:
            return HttpResponse('Dame un ID!')

        curso = Curso.objects.filter(id=id)
        nombre = curso[0].nombre
        codigo = curso[0].codigo 
        docente = str( curso[0].docente )

        costo = str( curso[0].costo )

        liquidacion = curso[0].liquidacion()
        INSCRIPTOS = curso[0].obtener_inscriptos()

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="liquidacion-'+codigo+'-'+docente+'.pdf"'

        # Create the PDF object, using the response object as its file.
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        for index, inscripto in enumerate(INSCRIPTOS):
            p.drawString(
                100, 
                230 + ( index * 10 ), 
                str( len(INSCRIPTOS) - index )+
                ' ' +
                inscripto.apellido +
                ' ' +
                inscripto.nombre + 
                ' -- ' +
                inscripto.dni + 
                ' -- ' +
                inscripto.alumno_una +
                ' -- pago: $' +
                str(inscripto.pago)
            )

        p.drawString(
            100, 
            210, 
            'Curso: ' +
            nombre 
        )
        p.drawString(
            100, 
            200, 
            'Código: ' +
            codigo
        )
        p.drawString(
            100, 
            190, 
            'Docente: ' +
            docente
        )
        p.drawString(
            100, 
            180, 
            'Arancel del curso: $' +
            str(liquidacion['arancel'])
        )

        p.drawString(
            100, 
            170, 
            'Pagaron %100: ' +
            str(liquidacion['cant100']) +
            ' x $' +
            costo +
            ' = $' +
            str(liquidacion['total100']) 
        )
        p.drawString(
            100, 
            160, 
            'Pagaron %75: ' +
            str(liquidacion['cant75']) +
            ' x $' +
            str(float(costo) * .75) +
            ' = $' +
            str(liquidacion['total75']) 
        )
        p.drawString(
            100, 
            150, 
            'Pagaron %50: ' +
            str(liquidacion['cant50']) +
            ' x $' +
            str(float(costo) * .5) +
            ' = $' +
            str(liquidacion['total50']) 
        )
        #p.drawString(
        #    100, 
        #    140, 
        #    'Total Esperado: ' +
        #    liquidacion['total_esperado']
        #)
        p.drawString(
            100, 
            130, 
            'Total Pagaron: $' +
            str(liquidacion['total_pagaron'])
        )
        p.drawString(
            100, 
            120, 
            'Monto Docente: $' +
            str(liquidacion['monto_docente'])
        )
        p.drawString(
            100, 
            110, 
            'Monto Atam: $' +
            str(liquidacion['monto_ATAM'])
        )    
        

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response

    else:
        #return HttpResponse('No estas registrado!')
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)
