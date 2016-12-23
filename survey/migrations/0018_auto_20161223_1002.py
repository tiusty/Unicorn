# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-23 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0017_auto_20161223_0955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='initialsurveymodel',
            name='addresses',
        ),
        migrations.AddField(
            model_name='initialsurveymodel',
            name='city',
            field=models.CharField(default='arlington', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='initialsurveymodel',
            name='state',
            field=models.CharField(default='MA', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='initialsurveymodel',
            name='streetAddress',
            field=models.CharField(default='12 Stoney Brook Rd', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='initialsurveymodel',
            name='zip_code',
            field=models.CharField(default='02476', max_length=200),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='SurveyAddresses',
        ),
    ]
