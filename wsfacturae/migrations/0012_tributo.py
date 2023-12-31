# Generated by Django 3.2.18 on 2023-04-09 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0011_subactividadeco_catactividadeco'),
    ]

    operations = [
        migrations.CreateModel(
            name='tributo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seccion', models.IntegerField(choices=[(1, 'TRIBUTOS APLICADOS POR ÍTEMS REFLEJADOS EN EL RESUMEN DEL DTE'), (2, 'TRIBUTOS APLICADOS POR ÍTEMS REFLEJADOS EN EL CUERPO DEL DOCUMENTO'), (3, 'IMPUESTOS AD-VALOREM APLICADOS POR ÍTEM DE USO INFORMATIVO REFLEJADOS EL RESUMEN DEL DOCUMENTO')], default=1, help_text='Sección donde se ve reflejado')),
                ('codigo', models.CharField(max_length=20)),
                ('valor', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('tipo', models.IntegerField(choices=[(1, 'Monto'), (2, 'Porcentual'), (3, 'No Definido')], default=1, help_text='Tipo de Valor')),
                ('descripcion', models.CharField(max_length=200)),
                ('nm_estado', models.IntegerField(choices=[(-1, 'INACTIVE'), (1, 'ACTIVE')], default=1, help_text='Activo o Inactivo el Registro')),
            ],
        ),
    ]
