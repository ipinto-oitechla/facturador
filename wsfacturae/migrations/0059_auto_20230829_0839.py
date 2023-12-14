# Generated by Django 3.2.18 on 2023-08-29 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0058_alter_productos_tributo'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='descuExenta',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='factura',
            name='descuGravada',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
    ]
