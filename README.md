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
```

## Ejecutar servidor
```
$ python manage.py runserver
```

