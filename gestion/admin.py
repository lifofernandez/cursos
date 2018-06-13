from django.contrib import admin

# Register your models here.

from .models import Curso, Inscripto, User, Categoria

admin.site.register(User)
admin.site.register(Curso)
admin.site.register(Inscripto)
admin.site.register(Categoria)

