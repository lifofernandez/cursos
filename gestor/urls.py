from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inscripcion/', views.agregar_inscripto, name='agregar_inscripto'),
]
