# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 05:06
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models

import wagtailannotatedimage.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0013_make_rendition_upload_callable'),
        ('wagtailcore', '0028_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('annotations', wagtailannotatedimage.fields.AnnotationsField(blank=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
