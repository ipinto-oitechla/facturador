# Generated by Django 3.2.18 on 2023-11-10 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cobrox', '0033_auto_20230511_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pago',
            name='credito',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='user_last_update',
        ),
        migrations.DeleteModel(
            name='Historicalpago',
        ),
        migrations.DeleteModel(
            name='pago',
        ),
    ]
