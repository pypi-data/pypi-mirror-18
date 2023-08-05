# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-13 06:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields.json
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckExecution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.TextField(unique=True, verbose_name='Check module slug')),
                ('last_run', models.DateTimeField(verbose_name='Last run')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('slug', models.TextField(verbose_name='Module slug')),
                ('identifier', models.CharField(max_length=256, verbose_name='Identifier')),
                ('status', models.IntegerField(choices=[(0, 'Unknown'), (1, 'OK'), (2, 'Warning'), (3, 'Critical')], default=0, verbose_name='Status')),
                ('data', django_extensions.db.fields.json.JSONField(blank=True, default=dict, verbose_name='Data')),
                ('config', django_extensions.db.fields.json.JSONField(blank=True, default=dict, verbose_name='Configuration')),
                ('payload_description', models.TextField(verbose_name='Payload description')),
                ('acknowledged_at', models.DateTimeField(blank=True, null=True, verbose_name='Acknowledged at')),
                ('acknowledged_until', models.DateTimeField(blank=True, null=True, verbose_name='Acknowledged until')),
                ('acknowledged_reason', models.TextField(blank=True, verbose_name='Acknowledge reason')),
                ('acknowledged_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acknowledged_by', to=settings.AUTH_USER_MODEL, verbose_name='Acknowledged by')),
                ('assigned_to_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('assigned_to_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_to_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view', 'Can view results dashboard and details'), ('acknowledge', 'Can acknowledge results'), ('config', 'Can change the configuration for results'), ('refresh', 'Can refresh results')),
            },
        ),
        migrations.AlterUniqueTogether(
            name='result',
            unique_together=set([('slug', 'identifier')]),
        ),
    ]
