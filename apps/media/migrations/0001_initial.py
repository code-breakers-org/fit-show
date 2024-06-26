# Generated by Django 4.1.13 on 2024-05-11 17:59

import apps.core.utils
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=apps.core.utils.get_file_name)),
                ('alt', models.CharField(blank=True, max_length=250, null=True)),
                ('mime_type', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'media',
                'verbose_name_plural': 'medias',
                'db_table': 'media',
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
            },
        ),
    ]
