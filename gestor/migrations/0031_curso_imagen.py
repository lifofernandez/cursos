# Generated by Django 2.0.3 on 2018-04-05 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0030_curso_inscripcion_abierta'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='imagen',
            field=models.ImageField(default=1, upload_to='', verbose_name='Imagen del Curso'),
        ),
    ]