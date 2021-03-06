
# GESTOR CURSOS
## APPS (secciones) !TO DO
- GESTION
  - crear usuarios docentes
  - creacion de cursos 

- MONITOR 
  - ver reportes de inscriptos
  - ver reporte cursos vigentes y pasados 

- LIQUIDACION
  - actualizar pago de los incriptos
  - generar liquidacion para docente

## USUARIOS roles/grupos 
* DOCENTES (los crea el gestor) 
* EDITOR
* LIQUIDADOR

## MODELOS

* CURSO
  - ID 
  - NOMBRE
  - DOCENTE (relación con usuario pre generado)
  - DESCRIPCION
  - DIAS DE DICTADO
  - FECHA DE INICIO
  - HORA DE INICIO
  - HORA DE FINALICACION
  - COSTO
  - REQUISITOS
  - MODALIDAD 
  - IMAGEN
  - INSCRIPCION ABIERTA (0/1) 

* INSCRIPTO
  - ID 
  - CURSO (relacion)
  - NOMBRE
  - APELLIDO
  - DNI
  - DOMICILIO
  - CORREO ELECTRONICO
  - NUMERO DE TELEFONO
  - ALUMNO UNA?
  - COMO SE ENTERÓ?
  - SUBSCRIPCION A BOLETÍN?
  - FECHA DE INSCRIPCION (automatico)
  - PAGO (privado)


## VISTAS
### FORMULARIOS
* FORMULARIO CREAR CURSO (admin / privado)
* FORMULARIO INSCRIPCION (público)
  - url: /inscripcion

### LISTAS
* lista completa de CURSOS (separada vigentes y anteriores)
* lista completa de INSCRIPTOS 
* lista de INSCRIPTOS (agrupados por CURSOS con INSCRIPCION ABIERTA)
* LIQUIDACIONES: lista de INSCRIPTOS a CURSOS VIGENTES con info de PAGO 

## ACCIONES
* CREAR/EDITAR CURSO (editor/gestor)
* AGREGAR INSCRIPTO (formulario publico)
* ACTUALIZAR PAGO INSCRIPTO (liquidador)

## UTILIDADES
* Imprimir Recibos
* Imprimir Certificados
* Descargar listas de inscriptos, liquidaciones

## TO DO
- [x] Crear grupo de user "Docente"
- [x] Crear modelo curso
- [x] Crear modelo inscripto
- [x] Crear formulario publico de insrcipcion
- [x] Recibo alumno imprimible 
- [x] Certificado alumno imprimible 
- [x] Liquidacion docente imprimible 
- [x] Configurar permisos de usuario
- [x] Front-End 

## IDEAS:
- [ ] ficha de curso txt: toda info para para publicar, prensa y promocion
- [ ] vista de curso individual con inscriptos 
- [ ] vista semanal de cursos
## Al hacer migraciones, aplicarlas y ejecutar server
```
$ python manage.py makemigrations gestion && python manage.py migrate && python manage.py runserver
```

## Cargar data inicial usando "fixtures"

https://docs.djangoproject.com/en/2.0/howto/initial-data/

```
$ python manage.py loaddata dias.yaml
```
