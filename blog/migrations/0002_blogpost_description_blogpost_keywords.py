# Generated by Django 5.0.1 on 2024-01-20 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='keywords',
            field=models.TextField(blank=True, null=True),
        ),
    ]