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
    path('inscripto/<int:id>/editar', views.inscripto_editar, name='inscripto_editar'),

    path('curso/nuevo', views.curso_nuevo, name='curso_nuevo'),
    path('cursos/', views.cursos, name='cursos'),

    #path('../admin/gestion/curso/<int:id>/change', views.cursos, name='curso_detalles'),

    path('cursos/<int:id>/planilla/', views.curso_planilla, name='curso_planilla'),
    path('curso/<int:id>/clonar', views.curso_clonar, name='curso_clonar'),
    path('curso/<int:id>/editar', views.curso_editar, name='curso_editar'),

    path('inscriptosxcursos/', views.inscriptosxcursos, name='inscriptosxcursos'),

    path('liquidaciones/', views.liquidaciones, name='liquidaciones'),
    path('curso/<int:id>/liquidacion/', views.curso_liquidacion, name='curso_liquidacion'),

    #path('pdftest/', views.pdftest, name='pdftest'),

]


