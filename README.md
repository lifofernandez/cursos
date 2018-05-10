# Gestor de Cursos en Django 2

## Blanqueo previo a instalar

```
$ python manage.py flush
$ rm -rf gestion/migrations/*
```

## Instalar
```
$ pip install -r requirements.txt
$ python manage.py makemigrations gestion 
$ python manage.py migrate 
$ python manage.py createsuperuser
$ python manage.py loaddata dias.yaml
$ python manage.py runserver
```

## Hacer migraciones, aplicarlas y ejecutar server
```
$ python manage.py makemigrations gestion && python manage.py migrate && python manage.py runserver
```

## Cargar data inicial usando "fixtures"

https://docs.djangoproject.com/en/2.0/howto/initial-data/

```
$ python manage.py loaddata dias.yaml
```
