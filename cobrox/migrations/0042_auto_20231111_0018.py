# Generated by Django 3.2.18 on 2023-11-11 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cobrox', '0041_auto_20231111_0017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagosfactura',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='pagosfactura',
            name='factura',
        ),
        migrations.RemoveField(
            model_name='pagosfactura',
            name='plazo',
        ),
        migrations.RemoveField(
            model_name='pagosfactura',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='pagosfactura',
            name='user_last_update',
        ),
        migrations.DeleteModel(
            name='Historicalpagosfactura',
        ),
        migrations.DeleteModel(
            name='pagosfactura',
        ),
    ]