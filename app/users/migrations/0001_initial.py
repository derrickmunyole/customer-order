# Generated by Django 5.1.3 on 2024-11-12 10:44

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('oidc_id', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=50, unique=True)),
            ],
        ),
    ]
