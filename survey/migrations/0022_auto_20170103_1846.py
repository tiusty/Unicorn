# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-03 23:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0021_auto_20161231_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='Destinations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('streetAddress', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zip_code', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='initialsurveymodel',
            name='city',
        ),
        migrations.RemoveField(
            model_name='initialsurveymodel',
            name='state',
        ),
        migrations.RemoveField(
            model_name='initialsurveymodel',
            name='streetAddress',
        ),
        migrations.RemoveField(
            model_name='initialsurveymodel',
            name='zip_code',
        ),
        migrations.CreateModel(
            name='BuyingDestinations',
            fields=[
                ('destinations_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='survey.Destinations')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.BuyingSurveyModel')),
            ],
            bases=('survey.destinations',),
        ),
        migrations.CreateModel(
            name='RentingDesintations',
            fields=[
                ('destinations_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='survey.Destinations')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.RentingSurveyModel')),
            ],
            bases=('survey.destinations',),
        ),
    ]
