# Generated by Django 2.0.3 on 2018-04-23 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_auto_20180419_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscripto',
            name='correo',
            field=models.EmailField(max_length=200, verbose_name='Correo Electrónico'),
        ),
    ]