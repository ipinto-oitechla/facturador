# Generated by Django 3.2.18 on 2023-07-19 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0017_auto_20230719_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otrosdocasoc',
            name='coddocasociado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_asoc_tipodoc', to='wsfacturae.detallemastercat'),
        ),
    ]
