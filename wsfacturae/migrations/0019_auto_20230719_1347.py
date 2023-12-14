# Generated by Django 3.2.18 on 2023-07-19 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0018_alter_otrosdocasoc_coddocasociado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otrosdocasoc',
            name='medico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='wsfacturae.medico'),
        ),
        migrations.AlterField(
            model_name='otrosdocasoc',
            name='medico_tiposervicio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='docasoc_medtipos', to='wsfacturae.detallemastercat'),
        ),
    ]