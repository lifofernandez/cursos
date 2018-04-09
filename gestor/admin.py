from django.contrib import admin

# Register your models here.

from .models import Curso, Inscripto

admin.site.register(Curso)
admin.site.register(Inscripto)

