# Generated by Django 2.0.3 on 2018-06-13 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0012_auto_20180613_1808'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lugar',
            options={'ordering': ('nombre',), 'verbose_name_plural': 'Lugares'},
        ),
    ]