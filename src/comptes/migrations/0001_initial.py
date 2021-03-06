# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-09-13 21:02
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('nom', models.CharField(max_length=255, verbose_name='Nom')),
                ('prenoms', models.CharField(max_length=255, verbose_name='Prenom')),
                ('ref_abonne', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Reference Abonné')),
                ('telephone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Format: '+999999999'. 15 chiffres maximum.", regex='^\\+?1?\\d{9,15}$')])),
                ('is_active', models.BooleanField(default=True)),
                ('client', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailActivation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('key', models.CharField(blank=True, max_length=120, null=True)),
                ('activated', models.BooleanField(default=False)),
                ('forced_expired', models.BooleanField(default=False)),
                ('expires', models.IntegerField(default=7)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
