# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20151129_0723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='grade_average',
            new_name='mean',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='grade_stdev',
            new_name='stdev',
        ),
        migrations.RemoveField(
            model_name='course',
            name='grade_median',
        ),
        migrations.RemoveField(
            model_name='course',
            name='total_grades',
        ),
        migrations.RemoveField(
            model_name='disciplinestats',
            name='median',
        ),
        migrations.RemoveField(
            model_name='disciplinestats',
            name='total_grades',
        ),
        migrations.RemoveField(
            model_name='section',
            name='grade_median',
        ),
        migrations.RemoveField(
            model_name='section',
            name='total_grades',
        ),
        migrations.RemoveField(
            model_name='subjectstats',
            name='median',
        ),
        migrations.RemoveField(
            model_name='subjectstats',
            name='total_grades',
        ),
        migrations.AddField(
            model_name='course',
            name='distribution',
            field=django_extensions.db.fields.json.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='distribution',
            field=django_extensions.db.fields.json.JSONField(null=True),
        ),
    ]
