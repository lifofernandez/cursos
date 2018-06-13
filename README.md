# Gestor de Cursos en Django 2

## Blanqueo previo a instalar

```
$ python manage.py flush
```
ó
```
$ rm db.sqlite3
$ rm cursos/__pycache__ -r
$ rm gestion/__pycache__ -r
$ rm -rf gestion/migrations/*
```

## Instalar
```
$ pip install -r requirements.txt
$ python manage.py makemigrations gestion 
$ python manage.py migrate 
$ python manage.py loaddata dias.yaml categorias.yaml lugares.yaml
$ python manage.py createsuperuser
```

## Ejecutar servidor
```
$ python manage.py runserver
```

