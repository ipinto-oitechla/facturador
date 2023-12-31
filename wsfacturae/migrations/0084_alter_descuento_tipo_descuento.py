# Generated by Django 3.2.18 on 2023-11-14 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0083_alter_descuento_tipo_descuento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descuento',
            name='tipo_descuento',
            field=models.CharField(choices=[('CANTIDAD_ITEM', 'Cantidad items'), ('MONTO_FACTURA', 'Monto factura'), ('MONTO_ITEM', 'Monto item'), ('PORCENTUAL_FACTURA', 'Porcentual factura'), ('PORCENTUAL_ITEM', 'Porcentual item')], max_length=100),
        ),
    ]
