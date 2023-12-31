# Generated by Django 3.2.18 on 2023-08-28 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsfacturae', '0054_rename_tipodte_param_version_dte_ambiente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='param_version_dte',
            name='ambiente',
        ),
        migrations.RemoveField(
            model_name='param_version_dte',
            name='codigo_documento',
        ),
        migrations.RemoveField(
            model_name='param_version_dte',
            name='version',
        ),
        migrations.AddField(
            model_name='param_version_dte',
            name='codigo',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='param_version_dte',
            name='descripcion',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='param_version_dte',
            name='tipoDato',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='param_version_dte',
            name='valor',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
