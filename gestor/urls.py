from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('inscripcion/', views.inscripcion, name='inscripcion'),

    path('inscriptos/', views.inscriptos, name='inscriptos'),
    path('../admin/gestor/inscripto/<int:id>/change', views.inscriptos, name='inscripto_detalles'),

    path('cursos/', views.cursos, name='cursos'),
    path('../admin/gestor/curso/<int:id>/change', views.cursos, name='curso_detalles'),

    path('inscriptosxcursos/', views.inscriptosxcursos, name='inscriptosxcursos'),

]


