# Generated by Django 3.2.18 on 2023-07-21 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0028_auto_20230721_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctributarioelec',
            name='fk_TribuDocDte',
        ),
        migrations.RemoveField(
            model_name='historicaldoctributarioelec',
            name='fk_TribuDocDte',
        ),
        migrations.DeleteModel(
            name='TribuDocDte',
        ),
    ]