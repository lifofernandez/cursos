from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('inscripcion/', views.inscripcion, name='inscripcion'),

    path('inscriptos/', views.inscriptos, name='inscriptos'),
    path('../admin/gestion/inscripto/<int:id>/change', views.inscriptos, name='inscripto_detalles'),
    # argumentos(url, funcion que ejecuta, identificador de la url)
    path('inscripto/<int:id>/recibo/', views.inscripto_recibo, name='inscripto_recibo'),

    path('cursos/', views.cursos, name='cursos'),
    path('../admin/gestion/curso/<int:id>/change', views.cursos, name='curso_detalles'),

    path('inscriptosxcursos/', views.inscriptosxcursos, name='inscriptosxcursos'),

    #path('pdftest/', views.pdftest, name='pdftest'),

]


