# Generated by Django 3.2.18 on 2023-07-19 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0016_alter_identification_tipomodelo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emisorn',
            name='direccionDep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cod_dep', to='wsfacturae.departamento'),
        ),
        migrations.AlterField(
            model_name='emisorn',
            name='direccionMun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cod_munip', to='wsfacturae.municipio'),
        ),
    ]