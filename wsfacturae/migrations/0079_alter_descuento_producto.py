# Generated by Django 3.2.18 on 2023-11-14 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0078_descuento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descuento',
            name='producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wsfacturae.productos'),
        ),
    ]