# Generated by Django 3.2.18 on 2023-12-01 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0095_identificacion_tipooperacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='receptorn',
            name='nombreComercial',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
