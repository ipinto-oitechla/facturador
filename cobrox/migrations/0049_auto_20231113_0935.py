# Generated by Django 3.2.18 on 2023-11-13 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cobrox', '0048_delete_medico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalcredito',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='historicalcredito',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalcredito',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='historicalcredito',
            name='user_last_update',
        ),
        migrations.DeleteModel(
            name='credito',
        ),
        migrations.DeleteModel(
            name='Historicalcredito',
        ),
    ]
