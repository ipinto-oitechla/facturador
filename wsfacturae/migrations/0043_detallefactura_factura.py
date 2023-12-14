# Generated by Django 3.2.18 on 2023-08-11 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0042_alter_doctributarioelec_fk_ventasterc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigoFactura', models.CharField(max_length=8, null=True)),
                ('fecha', models.DateField(null=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=11, null=True)),
                ('fk_receptor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='wsfacturae.receptorn')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=11, null=True)),
                ('fk_Producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='wsfacturae.productos')),
                ('fk_factura', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='wsfacturae.factura')),
            ],
        ),
    ]
