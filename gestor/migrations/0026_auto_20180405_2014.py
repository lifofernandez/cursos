# Generated by Django 2.0.3 on 2018-04-05 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0025_auto_20180405_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='nombre',
            field=models.CharField(max_length=200, verbose_name='Nombre del Curso'),
        ),
    ]