# Generated by Django 3.2.18 on 2023-09-05 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0074_detallefactura_totaldescuento'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='subtotalSinImpuestos',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
    ]