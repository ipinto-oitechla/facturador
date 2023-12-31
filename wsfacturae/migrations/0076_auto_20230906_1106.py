# Generated by Django 3.2.18 on 2023-09-06 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0075_factura_subtotalsinimpuestos'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='impuesTotal',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AlterField(
            model_name='factura',
            name='fk_Identificacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wsfacturae.identificacion'),
        ),
        migrations.AlterField(
            model_name='productos',
            name='codigo',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True),
        ),
    ]
