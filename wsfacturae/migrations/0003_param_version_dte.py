# Generated by Django 3.2.18 on 2023-03-21 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0002_ws_autenticacion_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='param_version_dte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_documento', models.PositiveIntegerField()),
                ('version', models.PositiveIntegerField()),
                ('tipoDte', models.CharField(max_length=2)),
            ],
        ),
    ]