# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-27 01:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0002_artisanaccount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0007_auto_20171022_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('artisan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.ArtisanAccount')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]