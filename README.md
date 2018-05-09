# Gestor de Cursos en Django 2
hacer migraciones, aplicarlas y ejecutar server
```
$ python manage.py makemigrations gestion && python manage.py migrate && python manage.py runserver
```

Cargar data inicial usando "fixtures"

https://docs.djangoproject.com/en/2.0/howto/initial-data/

```
$ python manage.py loaddata dias.yaml
```
TODO: agregar pago a editar inscripto
