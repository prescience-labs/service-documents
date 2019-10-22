# Generated by Django 2.2.4 on 2019-09-23 11:10

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('sentiment_analysis', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text="From Meaningcloud's Sentiment Analysis", null=True)),
                ('topic_extraction', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text="From Meaningcloud's Topic Extraction", null=True)),
                ('categorization', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text="From Meaningcloud's Deep Categorization", null=True)),
                ('force_analysis', models.BooleanField(default=False, help_text='Run all analyses during the next analysis job.')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
