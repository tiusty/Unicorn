# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-23 17:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import houseDatabase.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HousePhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to=houseDatabase.models.house_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='RentDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('air_conditioning', models.BooleanField(default=False)),
                ('wash_dryer_in_home', models.BooleanField(default=False)),
                ('dish_washer', models.BooleanField(default=False)),
                ('bath', models.BooleanField(default=False)),
                ('num_bathrooms', models.IntegerField(default=0)),
                ('num_bedrooms', models.IntegerField(default=0)),
                ('parking_spot', models.BooleanField(default=False)),
                ('washer_dryer_in_building', models.BooleanField(default=False)),
                ('elevator', models.BooleanField(default=False)),
                ('handicap_access', models.BooleanField(default=False)),
                ('pool_hot_tub', models.BooleanField(default=False)),
                ('fitness_center', models.BooleanField(default=False)),
                ('storage_unit', models.BooleanField(default=False)),
                ('address', models.CharField(default='Not set', max_length=200)),
                ('city', models.CharField(default='Not set', max_length=200)),
                ('state', models.CharField(default='Not set', max_length=200)),
                ('zip_code', models.CharField(default='Not set', max_length=200)),
                ('price', models.IntegerField(default=-1)),
                ('home_type', models.CharField(default='Not set', max_length=200)),
                ('move_in_day', models.DateField(default=datetime.date.today)),
                ('lat', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('lon', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ZipCodeDictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ZipCodeDictionaryChild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.CharField(max_length=20)),
                ('commute_time', models.IntegerField(default=-1)),
                ('commute_distance', models.IntegerField(default=-1)),
                ('last_date_updated', models.DateField(default=django.utils.timezone.now)),
                ('commute_type', models.CharField(choices=[('driving', 'Driving'), ('transit', 'Transit'), ('walking', 'Walking'), ('biking', 'Biking')], max_length=15)),
                ('base_zip_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houseDatabase.ZipCodeDictionary')),
            ],
        ),
        migrations.AddField(
            model_name='housephotos',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houseDatabase.RentDatabase'),
        ),
    ]
