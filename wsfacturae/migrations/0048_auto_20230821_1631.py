# Generated by Django 3.2.18 on 2023-08-21 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0047_auto_20230821_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='fk_Establecimiento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='wsfacturae.establecimiento'),
        ),
        migrations.AddField(
            model_name='factura',
            name='fk_emisor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='wsfacturae.emisorn'),
        ),
    ]