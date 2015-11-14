# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20151024_0914'),
    ]

    operations = [
        migrations.CreateModel(
            name='DivisionSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('data', django_extensions.db.fields.json.JSONField()),
            ],
        ),
        migrations.RemoveField(
            model_name='subject',
            name='grade_average',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='grade_median',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='grade_stdev',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='letter_grades',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='total_grades',
        ),
    ]
