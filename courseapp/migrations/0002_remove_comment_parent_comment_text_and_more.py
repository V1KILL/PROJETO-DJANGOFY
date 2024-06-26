# Generated by Django 5.0.6 on 2024-06-14 20:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.TextField(default='comment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='response',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='courseapp.comment'),
        ),
    ]
