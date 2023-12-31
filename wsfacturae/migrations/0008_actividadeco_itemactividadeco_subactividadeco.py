# Generated by Django 3.2.18 on 2023-04-07 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0007_auto_20230407_0659'),
    ]

    operations = [
        migrations.CreateModel(
            name='actividadeco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
                ('nm_estado', models.IntegerField(choices=[(-1, 'INACTIVE'), (1, 'ACTIVE')], default=1, help_text='Activo o Inactivo el Registro')),
            ],
        ),
        migrations.CreateModel(
            name='subactividadeco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
                ('nm_estado', models.IntegerField(choices=[(-1, 'INACTIVE'), (1, 'ACTIVE')], default=1, help_text='Activo o Inactivo el Registro')),
            ],
        ),
        migrations.CreateModel(
            name='itemactividadeco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20)),
                ('descripcion', models.CharField(max_length=200)),
                ('nm_estado', models.IntegerField(choices=[(-1, 'INACTIVE'), (1, 'ACTIVE')], default=1, help_text='Activo o Inactivo el Registro')),
                ('subactividadeco', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='wsfacturae.subactividadeco')),
            ],
        ),
    ]
