# Generated by Django 3.2.18 on 2023-09-04 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0071_factura_totaloperaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='subtotalconDescu',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
    ]
