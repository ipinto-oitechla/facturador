# Generated by Django 3.2.18 on 2023-07-24 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restser', '0007_auto_20230724_1740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallefactura',
            name='fk_factura',
        ),
    ]
