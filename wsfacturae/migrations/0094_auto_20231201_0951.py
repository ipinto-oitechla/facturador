# Generated by Django 3.2.18 on 2023-12-01 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0093_auto_20231130_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='identificacion',
            name='tipoModelo',
            field=models.ForeignKey(default='23', on_delete=django.db.models.deletion.DO_NOTHING, related_name='identificacion_tipomodelo', to='wsfacturae.detallemastercat'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='identificacion',
            name='ambiente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='identificacion_ambiente', to='wsfacturae.detallemastercat'),
        ),
        migrations.AlterField(
            model_name='identificacion',
            name='tipoDte',
            field=models.ForeignKey(default=23, on_delete=django.db.models.deletion.DO_NOTHING, related_name='identificacion_tipodte', to='wsfacturae.detallemastercat'),
            preserve_default=False,
        ),
    ]
