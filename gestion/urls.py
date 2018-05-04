from django.urls import path
from . import views

urlpatterns = [
    # argumentos(url, funcion que ejecuta, identificador de la url)
    #path('', views.index, name='index'),
    #path('inscripcion/', views.inscripcion, name='inscripcion'),

    path('', views.inscriptos, name='inscriptos'),
    path('inscriptos/', views.inscriptos, name='inscriptos'),
    path('../admin/gestion/inscripto/<int:id>/change', views.inscriptos, name='inscripto_detalles'),
    path('inscripto/<int:id>/recibo/', views.inscripto_recibo, name='inscripto_recibo'),

    path('cursos/', views.cursos, name='cursos'),
    path('../admin/gestion/curso/<int:id>/change', views.cursos, name='curso_detalles'),
    path('cursos/<int:id>/planilla/', views.curso_planilla, name='curso_planilla'),

    path('inscriptosxcursos/', views.inscriptosxcursos, name='inscriptosxcursos'),

    path('liquidaciones/', views.liquidaciones, name='liquidaciones'),
    path('curso/<int:id>/liquidacion/', views.curso_liquidacion, name='curso_liquidacion'),

    #path('pdftest/', views.pdftest, name='pdftest'),

]


