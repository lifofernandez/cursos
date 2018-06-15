# Generated by Django 2.0.3 on 2018-06-15 19:19

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0015_auto_20180615_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='etiquetas',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Etiquetas'),
        ),
    ]