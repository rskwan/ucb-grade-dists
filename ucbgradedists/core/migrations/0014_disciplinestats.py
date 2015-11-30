# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20151127_0957'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisciplineStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_grades', models.IntegerField(default=0)),
                ('letter_grades', models.IntegerField(default=0)),
                ('average', models.FloatField(null=True)),
                ('median', models.FloatField(null=True)),
                ('stdev', models.FloatField(null=True)),
                ('distribution', django_extensions.db.fields.json.JSONField(null=True)),
                ('discipline', models.ForeignKey(to='core.Discipline')),
                ('division', models.ForeignKey(to='core.DivisionSet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
