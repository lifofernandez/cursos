# Generated by Django 2.0.3 on 2018-06-13 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0004_auto_20180613_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=20)),
            ],
        ),
    ]