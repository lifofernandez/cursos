from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inscripcion/', views.inscripcion, name='inscripcion'),
    path('inscriptos/', views.inscriptos_list, name='inscriptos_list'),
    path('../admin/gestor/inscripto/<int:id>/change', views.inscriptos_list, name='inscripto_detalles')
]
