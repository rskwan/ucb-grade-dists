# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20151130_0122'),
    ]

    operations = [
        migrations.CreateModel(
            name='DivisionStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('letter_grades', models.IntegerField(default=0)),
                ('mean', models.FloatField(null=True)),
                ('stdev', models.FloatField(null=True)),
                ('distribution', django_extensions.db.fields.json.JSONField(null=True)),
                ('my_rank', models.IntegerField(default=0)),
                ('rank_count', models.IntegerField(default=0)),
                ('division_set', models.ForeignKey(to='core.DivisionSet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='discipline',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='disciplinestats',
            name='my_rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='disciplinestats',
            name='rank_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subjectstats',
            name='my_rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subjectstats',
            name='rank_count',
            field=models.IntegerField(default=0),
        ),
    ]
