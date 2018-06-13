from django.contrib import admin

# Register your models here.

from .models import Curso, Inscripto, User, Categoria, Lugar

admin.site.register(User)
admin.site.register(Curso)
admin.site.register(Inscripto)
admin.site.register(Categoria)
admin.site.register(Lugar)

