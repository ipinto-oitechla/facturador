# Generated by Django 3.2.18 on 2023-11-13 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cobrox', '0049_auto_20231113_0935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalcliente',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalcliente',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='historicalcliente',
            name='user_last_update',
        ),
        migrations.RemoveField(
            model_name='historicalcliente',
            name='zona',
        ),
        migrations.DeleteModel(
            name='cliente',
        ),
        migrations.DeleteModel(
            name='Historicalcliente',
        ),
    ]
