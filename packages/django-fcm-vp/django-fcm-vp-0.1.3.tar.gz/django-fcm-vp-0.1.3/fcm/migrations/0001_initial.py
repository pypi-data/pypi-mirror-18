# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.models import CASCADE
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dev_id', models.CharField(max_length=50, unique=True, verbose_name='Device ID')),
                ('reg_id', models.CharField(max_length=255, unique=True, verbose_name='Registration ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is active?')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE))
            ],
            options={
                'verbose_name_plural': 'Devices',
                'verbose_name': 'Device',
                'abstract': False,
            },
        ),
    ]
