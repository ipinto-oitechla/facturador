# Generated by Django 3.2.18 on 2023-11-13 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cobrox', '0051_auto_20231113_0952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zona',
            name='filial',
        ),
        migrations.RemoveField(
            model_name='zona',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='zona',
            name='user_last_update',
        ),
        migrations.DeleteModel(
            name='Historicalzona',
        ),
        migrations.DeleteModel(
            name='zona',
        ),
    ]