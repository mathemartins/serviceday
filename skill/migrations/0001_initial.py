# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-09 08:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import skill.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artisan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuratedSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=120)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Curated Skills',
                'verbose_name': 'Curated Skill',
            },
        ),
        migrations.CreateModel(
            name='MySkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'My Skills',
                'verbose_name': 'My Skills',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=skill.models.download_media_location)),
                ('title', models.CharField(max_length=30)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=1000.0, max_digits=100, null=True)),
                ('sale_active', models.BooleanField(default=False)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, default=1000.0, max_digits=100, null=True)),
                ('artisan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artisan.ArtisanAccount')),
            ],
        ),
        migrations.CreateModel(
            name='SkillRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('skills', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skill.Skill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='myskills',
            name='skills',
            field=models.ManyToManyField(blank=True, to='skill.Skill'),
        ),
        migrations.AddField(
            model_name='myskills',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='curatedskills',
            name='skills',
            field=models.ManyToManyField(blank=True, to='skill.Skill'),
        ),
        migrations.AddField(
            model_name='curatedskills',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]