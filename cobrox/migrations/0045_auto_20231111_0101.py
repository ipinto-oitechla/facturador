# Generated by Django 3.2.18 on 2023-11-11 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cobrox', '0044_auto_20231111_0047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalemisor',
            name='actividadeco',
        ),
        migrations.RemoveField(
            model_name='historicalemisor',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalemisor',
            name='municipio',
        ),
        migrations.RemoveField(
            model_name='historicalemisor',
            name='tipoestablecimiento',
        ),
        migrations.RemoveField(
            model_name='historicalemisor',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='historicalemisor',
            name='user_last_update',
        ),
        migrations.DeleteModel(
            name='emisor',
        ),
        migrations.DeleteModel(
            name='Historicalemisor',
        ),
    ]
