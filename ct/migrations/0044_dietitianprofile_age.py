# Generated by Django 4.2.5 on 2023-11-06 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0043_dietitianprofile_available_timings_dietitianbooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='dietitianprofile',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
