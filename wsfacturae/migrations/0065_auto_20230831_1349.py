# Generated by Django 3.2.18 on 2023-08-31 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0064_alter_emisorn_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emisorn',
            name='codActEco',
        ),
        migrations.AddField(
            model_name='emisorn',
            name='actividadeco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='emi_actividadecon', to='wsfacturae.actividadeco'),
        ),
    ]
