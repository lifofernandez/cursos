# Generated by Django 2.0.3 on 2018-06-08 21:00

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('docente', models.BooleanField(default=1, verbose_name='Es Docente?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre del Curso')),
                ('codigo', models.CharField(blank=True, editable=False, max_length=20, verbose_name='Código del Curso')),
                ('descripcion', models.TextField(default='', verbose_name='Descripción')),
                ('modalidad', models.CharField(choices=[('v', 'Virtual'), ('p', 'Presencial')], default='p', max_length=1, verbose_name='Modalidad')),
                ('inicio_fecha', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha de Inicio')),
                ('periodo', models.CharField(blank=True, editable=False, max_length=10, verbose_name='Perdiodo del Curso')),
                ('inicio_hora', models.TimeField(default=django.utils.timezone.now, verbose_name='Hora de Inicio')),
                ('finalizacion_hora', models.TimeField(default=django.utils.timezone.now, verbose_name='Hora de Finalizaición')),
                ('arancel', models.IntegerField(default=0, verbose_name='Arancel')),
                ('requisitos', models.TextField(default='', verbose_name='Requisitos')),
                ('imagen', models.ImageField(blank=True, upload_to='cursos_imgs', verbose_name='Imagen del Curso')),
                ('inscripcion_abierta', models.BooleanField(default=1, verbose_name='Inscripción Abierta')),
            ],
        ),
        migrations.CreateModel(
            name='Dia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Inscripto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pago', models.IntegerField(default=0, verbose_name='Pagó')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=200, verbose_name='Apellido')),
                ('dni', models.CharField(max_length=200, verbose_name='D.N.I.')),
                ('domicilio', models.CharField(max_length=200, verbose_name='Domicilio')),
                ('correo', models.EmailField(max_length=200, verbose_name='Correo Electrónico')),
                ('telefono', models.CharField(max_length=200, verbose_name='Numero Telefónico')),
                ('alumno_una', models.CharField(choices=[('no', 'No soy alumno de la UNA'), ('multimedia', 'Licenciatura en Artes Multimediales'), ('actuacion', 'Licenciatura en Actuación'), ('audiovisuales', 'Licenciatura en Artes Audiovisuales'), ('musica', 'Licenciatura en Artes Musicales'), ('visuales', 'Licenciatura en Artes Visuales'), ('movimiento', 'Licenciatura en Composición Coreográfica'), ('restauracion', 'Licenciatura en Conservación y Restauración de Bienes Culturales'), ('critica', 'Licenciatura en Crítica de Artes'), ('curaduria', 'Licenciatura en Curaduría en Artes'), ('teatro', 'Licenciatura en Dirección Escénica'), ('iluminacion', 'Licenciatura en Diseño de Iluminación de Espectáculos'), ('escenografia', 'Licenciatura en Escenografía'), ('folclore', 'Licenciatura en Folklore'), ('profesorado', 'Profesorado de Arte')], default='no', max_length=50, verbose_name='¿Es alumno de La U.N.A.?')),
                ('enterado', models.CharField(choices=[('redes_sociales', 'Redes Sociales (Facebook, Twitter, otra)'), ('mail', 'Newsletter/mailing'), ('cartelera', 'Cartelera de la universidad'), ('amigo', 'Recomendado por un amigo'), ('otro', 'Otros')], max_length=50, verbose_name='¿Como se enteró del curso?')),
                ('subscripcion', models.BooleanField(default=1, verbose_name='¿Desea recibir novedades?')),
                ('inscripcion_fecha', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha de Inscripción')),
                ('curso', models.ForeignKey(limit_choices_to={'inscripcion_abierta': True}, on_delete=django.db.models.deletion.CASCADE, to='gestion.Curso', verbose_name='Curso al que se inscribe')),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='dias',
            field=models.ManyToManyField(to='gestion.Dia', verbose_name='Días de Dictado'),
        ),
        migrations.AddField(
            model_name='curso',
            name='docente',
            field=models.ForeignKey(limit_choices_to={'docente': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Docente'),
        ),
    ]
