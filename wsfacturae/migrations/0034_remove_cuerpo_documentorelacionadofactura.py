# Generated by Django 3.2.18 on 2023-07-23 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0033_auto_20230723_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuerpo',
            name='documentorelacionadofactura',
        ),
    ]
