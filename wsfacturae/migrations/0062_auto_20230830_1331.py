# Generated by Django 3.2.18 on 2023-08-30 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0061_factura_descutotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='identificacion',
            name='codigoGeneracion',
            field=models.CharField(max_length=36, null=True),
        ),
        migrations.AddField(
            model_name='identificacion',
            name='numeroControl',
            field=models.CharField(max_length=32, null=True),
        ),
    ]