# Generated by Django 3.2.18 on 2023-07-24 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restser', '0005_alter_factura_fk_detalle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallefactura',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='detallefactura',
            name='monto',
            field=models.DecimalField(decimal_places=8, max_digits=11, null=True),
        ),
        migrations.AlterField(
            model_name='detallefactura',
            name='producto',
            field=models.CharField(max_length=100, null=True),
        ),
    ]