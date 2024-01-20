# Generated by Django 5.0.1 on 2024-01-20 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_blogpost_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='post_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.posttype'),
        ),
    ]