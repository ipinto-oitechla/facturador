# Generated by Django 3.2.18 on 2023-08-15 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0043_detallefactura_factura'),
    ]

    operations = [
        migrations.CreateModel(
            name='Establecimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complementodir', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=30)),
                ('celular', models.CharField(max_length=30)),
                ('codestablemh', models.CharField(blank=True, max_length=4, null=True)),
                ('codestablec', models.CharField(blank=True, max_length=4, null=True)),
                ('direccionMun', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cod_munip', to='wsfacturae.municipio')),
                ('tipoEstable', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cod_tipoEstable', to='wsfacturae.detallemastercat')),
            ],
        ),
        migrations.RemoveField(
            model_name='emisorn',
            name='celular',
        ),
        migrations.RemoveField(
            model_name='emisorn',
            name='codestablec',
        ),
        migrations.RemoveField(
            model_name='emisorn',
            name='codestablemh',
        ),
        migrations.RemoveField(
            model_name='emisorn',
            name='codpuntoventa',
        ),
        migrations.RemoveField(
            model_name='emisorn',
            name='codpuntoventamh',
        ),
        migrations.RemoveField(
            model_name='emisorn',
            name='complementodir',
        ),
        migrations.RemoveField(
            model_name='emisorn',
            name='direccionDep',
        ),
        migrations.RemoveField(
            model_name='emisorn',
            name='direccionMun',
        ),
        migrations.RemoveField(
            model_name='emisorn',
            name='telefono',
        ),
        migrations.RemoveField(
            model_name='emisorn',
            name='tipoEstable',
        ),
        migrations.AddField(
            model_name='productos',
            name='descUnidad',
            field=models.DecimalField(decimal_places=8, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='productos',
            name='exentoIva',
            field=models.CharField(choices=[('S', 'Sí'), ('N', 'No')], max_length=1, null=True),
        ),
        migrations.CreateModel(
            name='PuntoVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codpuntoventamh', models.CharField(blank=True, max_length=4, null=True)),
                ('codpuntoventa', models.CharField(blank=True, max_length=4, null=True)),
                ('establecimiento_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='wsfacturae.establecimiento')),
            ],
        ),
    ]
