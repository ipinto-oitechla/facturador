# Generated by Django 3.2.18 on 2023-12-05 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0098_factura_totaliva'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_estado', models.CharField(max_length=100)),
                ('codigo_estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='factura',
            name='hacienda_codigo_mensaje',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='factura',
            name='hacienda_fecha_procesamiento',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='factura',
            name='hacienda_response',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='factura',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='factura',
            name='sello_hacienda',
            field=models.TextField(blank='', null=True),
        ),
    ]