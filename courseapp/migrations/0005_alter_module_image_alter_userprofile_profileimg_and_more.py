# Generated by Django 5.0.6 on 2024-06-20 04:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseapp', '0004_video_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='image',
            field=models.ImageField(default='module/code bg.webp', upload_to='module/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profileimg',
            field=models.ImageField(default='profiles/me.jpg', upload_to='profiles/'),
        ),
        migrations.AlterField(
            model_name='video',
            name='image',
            field=models.ImageField(default='video/code bg.webp', upload_to='video/'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courseapp.video')),
            ],
        ),
    ]