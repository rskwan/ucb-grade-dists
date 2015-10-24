# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151003_0313'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['subject', 'num_numerical_part', 'number']},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['term', 'number']},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='term',
            options={'ordering': ['year', 'season']},
        ),
        migrations.AddField(
            model_name='course',
            name='division',
            field=models.IntegerField(default=7, choices=[(0, b'Lower Division'), (1, b'Upper Division'), (2, b'Graduate'), (3, b'Teaching'), (4, b'Professional'), (5, b"Master's Exam"), (6, b'Doctoral Exam'), (7, b'Other')]),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_average',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_median',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_stdev',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='letter_grades',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='num_numerical_part',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='total_grades',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='section',
            name='grade_average',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='grade_median',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='grade_stdev',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='letter_grades',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='section',
            name='total_grades',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subject',
            name='grade_average',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='grade_median',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='grade_stdev',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='letter_grades',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subject',
            name='total_grades',
            field=models.IntegerField(default=0),
        ),
    ]
