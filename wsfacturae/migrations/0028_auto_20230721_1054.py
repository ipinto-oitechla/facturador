# Generated by Django 3.2.18 on 2023-07-21 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0027_auto_20230721_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctributarioelec',
            name='fk_TribuDocDte',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='wsfacturae.tribudocdte'),
        ),
        migrations.AddField(
            model_name='historicaldoctributarioelec',
            name='fk_TribuDocDte',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='wsfacturae.tribudocdte'),
        ),
        migrations.AlterField(
            model_name='tribudocdte',
            name='codTributo',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='wsfacturae.tributo'),
        ),
    ]