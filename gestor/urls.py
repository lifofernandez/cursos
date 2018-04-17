from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inscripcion/', views.inscripcion, name='inscripcion'),
    path('inscriptos/', views.inscriptos_list, name='inscriptos_list'),
    path('../admin/gestor/inscripto/<int:id>/change', views.inscriptos_list, name='inscripto_detalles'),
    path('cursos/', views.cursos_list, name='cursos_list'),

    path('inscriptos_cursos/', views.inscriptos_cursos_list, name='inscriptos_cursos_list'),
    path('../admin/gestor/curso/<int:id>/change', views.cursos_list, name='curso_detalles'),

]


