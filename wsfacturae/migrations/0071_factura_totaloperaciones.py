# Generated by Django 3.2.18 on 2023-09-04 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0070_emisorn_natural'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='totalOperaciones',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
    ]