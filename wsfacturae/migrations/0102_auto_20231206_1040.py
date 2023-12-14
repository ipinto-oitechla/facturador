# Generated by Django 3.2.18 on 2023-12-06 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0101_hacienda_haciendaclasificacionmensajes_haciendamensajes_smtp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smtp',
            name='host',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='smtp',
            name='password',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='smtp',
            name='port',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='smtp',
            name='use_tls',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='smtp',
            name='username',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
