# Generated by Django 3.2.18 on 2023-11-14 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0082_auto_20231114_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descuento',
            name='tipo_descuento',
            field=models.CharField(choices=[('MONTO_ITEM', 'Monto item'), ('PORCENTUAL_ITEM', 'Porcentual item'), ('MONTO_FACTURA', 'Monto factura'), ('PORCENTUAL_FACTURA', 'Porcentual factura')], max_length=100),
        ),
    ]
