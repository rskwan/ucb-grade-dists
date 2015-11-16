# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20151116_0505'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectstats',
            name='term_averages',
            field=django_extensions.db.fields.json.JSONField(null=True),
        ),
    ]
