# Generated by Django 4.2.5 on 2024-03-01 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0077_remove_video_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]