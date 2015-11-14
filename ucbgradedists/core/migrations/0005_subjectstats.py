# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151113_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_grades', models.IntegerField(default=0)),
                ('letter_grades', models.IntegerField(default=0)),
                ('grade_average', models.FloatField(null=True)),
                ('grade_median', models.FloatField(null=True)),
                ('grade_stdev', models.FloatField(null=True)),
                ('division_set', models.ForeignKey(to='core.DivisionSet')),
                ('subject', models.ForeignKey(to='core.Subject')),
            ],
            options={
                'ordering': ['subject__name'],
            },
        ),
    ]
