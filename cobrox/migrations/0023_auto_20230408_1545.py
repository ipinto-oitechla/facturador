# Generated by Django 3.2.18 on 2023-04-08 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0011_subactividadeco_catactividadeco'),
        ('cobrox', '0022_emisor_historicalemisor_historicalreceptor_receptor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emisor',
            name='codactividad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='emi_codactividad', to='wsfacturae.actividadeco'),
        ),
        migrations.AlterField(
            model_name='historicalemisor',
            name='codactividad',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='wsfacturae.actividadeco'),
        ),
    ]
