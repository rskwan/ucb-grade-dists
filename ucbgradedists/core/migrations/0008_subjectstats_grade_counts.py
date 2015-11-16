# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_subjectstats_term_averages'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectstats',
            name='grade_counts',
            field=django_extensions.db.fields.json.JSONField(null=True),
        ),
    ]
