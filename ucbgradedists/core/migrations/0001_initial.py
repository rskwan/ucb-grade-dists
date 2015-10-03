# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('letter', models.BooleanField()),
                ('points', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='GradeCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('grade', models.ForeignKey(to='core.Grade')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('instructor', models.CharField(max_length=256)),
                ('ccn', models.CharField(max_length=5, verbose_name=b'CCN')),
                ('course', models.ForeignKey(to='core.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('season', models.IntegerField(choices=[(0, b'Spring'), (1, b'Summer'), (2, b'Fall')])),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='section',
            name='term',
            field=models.ForeignKey(to='core.Term'),
        ),
        migrations.AddField(
            model_name='gradecount',
            name='section',
            field=models.ForeignKey(to='core.Section'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(to='core.Subject'),
        ),
    ]
