# Generated by Django 3.2.18 on 2023-03-12 19:23

import cobrox.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cobrox', '0013_auto_20230312_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credito_archivo',
            name='archivo',
            field=models.FileField(max_length=500, upload_to=cobrox.models.imagecreexp_directory_path_with_uuid),
        ),
    ]