# Generated by Django 3.2.18 on 2023-07-21 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0025_auto_20230721_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctributarioelec',
            name='fk_TribuDocDte',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wsfacturae.tribudocdte'),
        ),
    ]