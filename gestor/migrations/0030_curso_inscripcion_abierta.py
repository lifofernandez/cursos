# Generated by Django 2.0.3 on 2018-04-05 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0029_auto_20180405_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='inscripcion_abierta',
            field=models.BooleanField(default=1, verbose_name='Inscripción Abierta'),
        ),
    ]