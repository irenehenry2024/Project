# Generated by Django 4.2.5 on 2023-11-12 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0049_userprofile_activity_level_userprofile_bmr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='bmr',
        ),
    ]
