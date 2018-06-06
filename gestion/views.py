import datetime
from django.utils import timezone

from django.shortcuts import render
# la carpeta de teplates debe ser declarada
# en TEMPLATES.DIRS en el fichero gestion/settings.py 

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from .forms import InscriptoForm, CursoForm, InscriptoEditForm, InscriptoAcreditarForm

from .models import Inscripto, Curso, Dia
from .tables import InscriptosTable, CursosTable, InscriptosXCursosTable, LiquidacionesTable


# Table Export
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport


#from django_tables2 import MultiTableMixin

#def index(request):
#    return HttpResponse('Hello, world.')

# FORMULARIOS
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
        return render(
                request,
                'inscripcion.html', 
                {'titulo':'Inscripción a Cursos','form':form}
        )

def curso( request, id ):
  if request.user.is_authenticated:
    curso = Curso.objects.filter(id=id)[0]
    
    #list_display = [field.name+ ' ' + curso.field +'</br>' for field in curso._meta.get_fields()]
    o = ''
    print(curso.dia_str)
    for field in curso._meta.get_fields():
      nombre = field.name
      if nombre != 'inscripto':
        o += nombre
        valor = getattr(curso,nombre)
        #e = curso._meta.get_field(nombre)
        print(valor)
        o += ' : '+ str(valor) + '<br>'
    return HttpResponse(o)
  else:
    return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

def curso_nuevo(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CursoForm(data = request.POST)
            if form.is_valid():
                curso = form.save( commit = True )
                curso.save()
                return HttpResponseRedirect( '/gestion/cursos' )
        else:
            form = CursoForm()
            return render(
                    request,
                    'curso.html', 
                    {'titulo':'Crear Curso','form':form}
            )
    else:        
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

def curso_clonar( request, id ):
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = CursoForm(request.POST)
            if form.is_valid():
                curso = form.save( commit = True )
                curso.save()
                return HttpResponseRedirect( '/gestion/cursos' )
        else:
            if not id:
                return HttpResponse('Dame un ID!')

            original = Curso.objects.filter( id = id )[0]
            dias = Dia.objects.filter( id__in = original.dias.values('id') )
            form = CursoForm(
                initial={ 
                    'nombre': original.nombre,
                    'docente': original.docente.id,
                    'descripcion': original.descripcion,
                    'inicio_fecha':'',
                    'dias': dias,
                    'inicio_hora': original.inicio_hora,
                    'finalizacion_hora': original.finalizacion_hora,
                    'costo': original.costo,
                    'requisitos': original.requisitos,
                    'modalidad': original.modalidad,
                    'imagen': original.imagen,
                }
            )
            return render(
                    request,
                    'curso.html', 
                    {'titulo':'Clonar Curso','form':form}
            )

    else:
       return HttpResponseRedirect('/admin/login/?next=%s' % request.path)


def curso_editar(request, id): 
    if request.user.is_authenticated:
        instance = Curso.objects.filter( id = id )[0]
        form = CursoForm(request.POST or None, instance = instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( '/gestion/cursos' )
        return render(
                request,
                'curso.html', 
                {
                    'titulo':'Editar Curso',
                    'form' : form
                }
        )
    else:
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

def inscripto_editar(request, id): 
    if request.user.is_authenticated:
        instance = Inscripto.objects.filter( id = id )[0]
        form = InscriptoEditForm( request.POST or None, instance = instance )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( '/gestion/inscriptos' )
        return render(
                request,
                'inscripto.html', 
                {
                    'titulo':'Editar Inscripto: ' + instance.nombre + ' ' + instance.apellido,
                    'form':form
                }
        )
    else:
        return HttpResponseRedirect( '/admin/login/?next=%s' % request.path )

def inscripto_acreditar(request, id): 
    if request.user.is_authenticated:
        instance = Inscripto.objects.filter( id = id )[0]
        form = InscriptoAcreditarForm( request.POST or None, instance = instance )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( '/gestion/liquidaciones' )
        return render(
                request,
                'inscripto.html', 
                {
                    'titulo':'Acreditar Inscripto: ' + instance.nombre + ' ' + instance.apellido,
                    'form':form
                }
        )
    else:
        return HttpResponseRedirect( '/admin/login/?next=%s' % request.path )

# TABLAS CON INFO
def inscriptos( request, sort = 'id' ):
    if request.user.is_authenticated:

        if request.method == 'GET' and 'sort' in request.GET:
            sort = request.GET['sort']
        INSCRIPTOS = Inscripto.objects.all().order_by(sort)
        tabla = InscriptosTable( INSCRIPTOS ) 
        titulo = 'inscriptos-' + str(timezone.now())

        if request.method == 'GET' and 'export' in request.GET:
            RequestConfig( request ).configure( tabla )
            export_format = request.GET['export']
            if TableExport.is_valid_format( export_format ):
                exporter = TableExport( export_format, tabla )
                return exporter.response( titulo + '.{}'.format( export_format ) )

        botones = [
            {'texto':'descargar CSV ','destino':'.?export=csv', },
            {'texto':'descargar XLS ','destino':'.?export=xls', },
        ]
        tabla.botones = botones 

        return render(
            request, 
            'tabla.html', 
            {
                'titulo':'Todos los inscriptos',
                #'bajada':'eo',
                'botones': [
                    {'texto':'Nuevo Inscripito','destino':'/inscripcion', 'clase' : 'btn-success'},
                 ],
                'tabla': tabla
            }
        )
    else: 
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)


def cursos(request, sort='inicio_fecha'):
    if request.user.is_authenticated:
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
        vigentes['botones'] = [
            {'texto':'descargar CSV ','destino':'.?export=csv&tabla=0', },
            {'texto':'descargar XLS ','destino':'.?export=xls&tabla=0', },
        ]

        anteriores =  {}
        anteriores['titulo'] = 'Cursos'
        anteriores['subtitulo'] = 'Anteriores'
        anteriores['items'] = CursosTable( pasados ) 
        anteriores['botones'] = [
            {'texto':'descargar CSV ','destino':'.?export=csv&tabla=1', },
            {'texto':'descargar XLS ','destino':'.?export=xls&tabla=1', },
        ]

        TABLAS = [
                vigentes,
                anteriores,
        ]

        if request.method == 'GET' and 'export' in request.GET and 'tabla' in request.GET:
            n_tabla = int(request.GET['tabla'])
            tabla = TABLAS[n_tabla]['items']
            titulo = TABLAS[n_tabla]['titulo'] + '_' + TABLAS[n_tabla]['subtitulo']
            RequestConfig( request ).configure( tabla )
            export_format = request.GET['export']
            if TableExport.is_valid_format( export_format ):
                exporter = TableExport( export_format, tabla)
                return exporter.response( titulo.lower().replace(" ","_") +'.{}'.format( export_format ) )

        return render(
            request, 
            'multitabla.html',
            {
                'titulo':'Todos los Cursos',
                'bajada':'eo',
                'botones': [
                    {'texto':'Nuevo Curso','destino':'/gestion/curso/nuevo','clase':'btn-success'}
                 ],
                'tablas':TABLAS
            }
        )
    else:
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

def inscriptosxcursos(request, sort='inicio_fecha'): 
    if request.user.is_authenticated:

        queryset = Curso.objects.all().order_by(sort)

        botones=[
            {'texto':'descargar CSV ','destino':'.?export=csv' },
            {'texto':'descargar XLS ','destino':'.?export=xls' },
        ]
        CURSOS = [] 
        for index, curso in enumerate(queryset): 
            c = {}
            c['titulo'] = curso.nombre
            c['subtitulo'] = curso.docente.get_full_name()
            c['codigo'] = curso.codigo
            c['fecha'] = curso.inicio_fecha

            INSCRIPTOS = []
            inscriptos = curso.inscriptos

            INSCRIPTOS = InscriptosXCursosTable(inscriptos) 
            c['items'] = INSCRIPTOS
            c['botones'] = [
                {'texto':'descargar CSV ','destino':'.?export=csv&tabla=' + str( index ), },
                {'texto':'descargar XLS ','destino':'.?export=xls&tabla=' + str( index ), },
            ]

            CURSOS.append(c)

        if request.method == 'GET' and 'export' in request.GET and 'tabla' in request.GET:
            n_tabla = int(request.GET['tabla'])
            tabla = CURSOS[n_tabla]['items']
            titulo = str(CURSOS[n_tabla]['codigo']) + '_' + str(CURSOS[n_tabla]['subtitulo'])
            RequestConfig( request ).configure( tabla )
            export_format = request.GET['export']
            if TableExport.is_valid_format( export_format ):
                exporter = TableExport( export_format, tabla)
                return exporter.response( titulo.lower().replace(" ","_") +'.{}'.format( export_format ) )

        return render(
            request, 
            'multitabla.html', 
            {
                'titulo':'Inscriptos a cada curso',
                'tablas':CURSOS,
                #'botones': [{'texto':'PRUEBA ','destino':'/gestion/curso/nuevo','clase':'btn-success'}],
            }
        )
    else:
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

def liquidaciones(request, sort='id'): 
    if request.user.is_authenticated:

        queryset = Curso.objects.all().order_by(sort)

        CURSOS = [] 
        for curso in queryset: 
            inscriptos = curso.inscriptos
            if inscriptos:
                c = {}
                c['titulo'] = curso.nombre
                c['subtitulo'] = curso.docente.get_full_name()

                INSCRIPTOS = []
                INSCRIPTOS = InscriptosXCursosTable(inscriptos) 
                c['items'] = INSCRIPTOS


                liquidacion = {}
                liquidacion['titulo'] = 'Liquidacion' 
                liquidacion['subtitulo'] = curso.codigo

                calculo = curso.liquidacion
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
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)


# RECIBOS Y PLANILLAS PDF
from reportlab.pdfgen import canvas

def inscripto_recibo(request, id):
    if request.user.is_authenticated:
        
        if not id:
            return HttpResponse('Dame un ID!')

        inscripto = Inscripto.objects.filter(id=id)[0]
        nombre = inscripto.nombre
        apellido = inscripto.apellido 

        alumno_una = inscripto.alumno_una

        pago = inscripto.pago
        costo = inscripto.curso.costo
        curso = inscripto.curso

        descuento = inscripto.descuento
        abona = inscripto.abona


        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        nombre_archivo ='"inscripcion_' + curso.codigo + '-' + apellido +'_'+ nombre +'.pdf"'
        response['Content-Disposition'] = 'attachment; filename=' + nombre_archivo.lower().replace(" ","_")


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
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

def curso_planilla(request, id):
    if request.user.is_authenticated:
        
        #id = 1
        if not id:
            return HttpResponse('Dame un ID!')

        curso = Curso.objects.filter(id=id)
        nombre = curso[0].nombre
        codigo = curso[0].codigo 
        docente = curso[0].docente.get_full_name()

        costo = str(curso[0].costo)

        INSCRIPTOS = []
        inscriptos = curso[0].inscriptos


        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        nombre_archivo ='"planilla-' + codigo + '-' + docente+'.pdf"'
        response['Content-Disposition'] = 'attachment; filename='+nombre_archivo.lower().replace(" ","_")

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
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

def curso_liquidacion(request, id):
    if request.user.is_authenticated:
        if not id:
            return HttpResponse('Dame un ID!')

        curso = Curso.objects.filter(id=id)[0]
        nombre = curso.nombre
        codigo = curso.codigo 
        docente = curso.docente.get_full_name()

        costo = str( curso.costo )

        liquidacion = curso.liquidacion
        INSCRIPTOS = curso.inscriptos

        response = HttpResponse(content_type='application/pdf')
        nombre_archivo ='"liquidacion-' + codigo + '-' + docente + '.pdf"'
        response['Content-Disposition'] = 'attachment; filename='+nombre_archivo.lower().replace(" ","_")


        p = canvas.Canvas(response)

        for index, inscripto in enumerate(INSCRIPTOS):
            p.drawString(
                100, 
                230 + ( index * 10 ), 
                str( len(INSCRIPTOS) - index ) +
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
        

        p.showPage()
        p.save()
        return response

    else:
        return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

