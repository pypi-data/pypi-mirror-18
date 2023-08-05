# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 10:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seo_description', models.CharField(blank=True, help_text='Short description of the page content', max_length=256, null=True, verbose_name='SEO: description')),
                ('seo_keywords', models.CharField(blank=True, help_text='List of keywords separated by commas', max_length=120, null=True, verbose_name='SEO: keywords')),
                ('url', models.CharField(db_index=True, max_length=180, verbose_name='Url')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('content', models.TextField(blank=True, verbose_name='Content')),
                ('template_name', models.CharField(blank=True, help_text='If no template name is provided "alapage/default.html" will be used.', max_length=120, verbose_name='Template name')),
                ('registration_required', models.BooleanField(default=False, help_text='If this is checked, only logged-in users will be able to view the page.', verbose_name='Registration required')),
                ('edited', models.DateTimeField(auto_now=True, null=True, verbose_name='Edited')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('published', models.BooleanField(default=True, verbose_name='Published')),
                ('staff_only', models.BooleanField(default=False, verbose_name='Staff only')),
                ('superuser_only', models.BooleanField(default=False, verbose_name='Superuser only')),
                ('is_reserved_to_groups', models.BooleanField(default=False, verbose_name='Reserved to groups')),
                ('is_reserved_to_users', models.BooleanField(default=False, verbose_name='Reserved to users')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('editor', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Edited by')),
                ('groups_only', models.ManyToManyField(blank=True, to='auth.Group', verbose_name='Reserved to some groups')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='alapage.Page', verbose_name='Parent page')),
                ('users_only', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Reserved to some users')),
            ],
            options={
                'ordering': ['url'],
                'verbose_name': 'Page',
                'verbose_name_plural': 'Page',
                'permissions': (('can_change_page_permissions', 'Can change page permissions'),),
            },
        ),
    ]
